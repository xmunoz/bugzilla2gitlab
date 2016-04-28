from xml.etree import ElementTree
from datetime import datetime
import dateutil.parser
import os.path
import sys
import re
from pprint import pprint

from config import Config
from helpers import _perform_request

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "config")
config = Config(CONFIG_PATH)

class MigrationClient(object):

    def migrate(self, bug_list):
        for bug in bug_list:
            print("Migrating bug {}".format(bug))
            self.migrate_one(bug)
            break

    def migrate_one(self, bugzilla_bug_id):
        fields = self.get_bugzilla_bug(bugzilla_bug_id)
        it = IssueThread(fields)
        it.save()

    def get_bugzilla_bug(self, bid):
        url = "{}show_bug.cgi?ctype=xml&id={}".format(config.bugzilla_base_url, bid)
        response = _perform_request(url, "get", paginated=False, json=False)
        tree = ElementTree.fromstring(response.content)
        bug_fields = {
            "long_desc" : [],
            "attachment": [],
            "cc": [],
        }
        for bug in tree:
            for fields in bug:
                if fields.tag in ("long_desc", "attachment"):
                    new = {}
                    for data in fields:
                        new[data.tag] = data.text
                    bug_fields[fields.tag].append(new)
                elif fields.tag == "cc":
                    bug_fields[fields.tag].append(fields.text)
                else:
                    bug_fields[fields.tag] = fields.text

        return bug_fields


class IssueThread(object):

    def __init__(self, fields):
        self.parse_fields(fields)

    def parse_fields(self, fields):
        self.reporter = fields.pop("reporter")
        self.issue = Issue()
        self.issue.title = fields.pop("short_desc")
        self.issue.sudo = config.gitlab_users[config.bugzilla_users[self.reporter]]
        self.issue.assignee = config.gitlab_users[config.bugzilla_users[fields.pop("assigned_to")]]
        self.issue.labels = []
        self.issue.labels.append("bugzilla")
        self.issue.labels.append(fields.pop("component"))
        self.issue.labels.append(fields.get("op_sys"))
        self.issue.status = fields.pop("bug_status")

        created_at_dt = dateutil.parser.parse(fields.pop("creation_ts"))
        self.issue.created_at = datetime.isoformat(created_at_dt)
        updated_at_dt = dateutil.parser.parse(fields.pop("delta_ts"))
        self.issue.updated_at = datetime.isoformat(updated_at_dt)

        self.make_description(fields)

        self.comments = []
        for c in fields["long_desc"]:
            comment = Comment()
            comment.sudo = config.gitlab_users[config.bugzilla_users[c.pop("who")]]
            comment.created_at = datetime.isoformat(dateutil.parser.parse(c.pop("bug_when")))
            if c.get("attachid"):
                regex = "^Created attachment (\d*)? (.*)$"
                comment_str = c.pop("thetext")
                matches = re.match(regex, comment_str)
                attach_id = c.pop("attachid")
                if not matches:
                    raise Exception("Failed to match comment string: {}".format(comment_str))
                assert matches.group(1) == attach_id
                filename = matches.group(2)
                attachment_markdown = Attachment(comment.sudo, attach_id, filename).save()
                comment.body = attachment_markdown
            else:
                comment.body = c.pop("thetext")

            self.comments.append(comment)

    def make_description(self, fields):
        ext_description = ""
        self.issue.description = "|||\n"
        self.issue.description += "| --- | --- |\n"

        bug_id = fields.pop("bug_id")
        link = "{}show_bug.cgi?id={}".format(config.bugzilla_base_url, bug_id)
        self.issue.description += "| {} | [{}]({}) |\n".format("Bugzilla Link",
                                                                     bug_id, link)

        self.issue.description += "| {} | {} |\n".format("Version", fields.pop("version"))
        self.issue.description += "| {} | {} |\n".format("OS", fields.pop("op_sys"))
        if fields.get("resolution"):
            self.issue.description += "| {} | {} |\n".format("Resolution", fields.pop("resolution"))
        if self.reporter == fields["long_desc"][0]["who"]:
            ext_description += "\n## Extended Description \n"
            ext_description += fields["long_desc"][0]["thetext"]
            del fields["long_desc"][0]

        attachments = []
        to_delete = []
        for i in range(0, len(fields["long_desc"])):
            comment = fields["long_desc"][i]
            if comment.get("attachid") and comment.get("who") == self.reporter:
                regex = "^Created attachment (\d*)\s(.*)$"
                comment_str = comment.pop("thetext")
                matches = re.match(regex, comment_str)
                attach_id = comment.pop("attachid")
                if not matches:
                    raise Exception("Failed to match comment string: {}".format(comment_str))
                assert matches.group(1) == attach_id
                filename = matches.group(2)
                attachment_markdown = Attachment(self.reporter, attach_id, filename).save()
                attachments.append(attachment_markdown)
                to_delete.append(i)

        for i in to_delete:
            del fields["long_desc"][i]

        if attachments:
            self.issue.description += "| {} | {} |\n".format("Attachments", ", ".join(attachments))

        if ext_description:
            self.issue.description += ext_description

    def save(self):
        self.issue.save()
        for comment in self.comments:
            comment.issue_id = self.issue.id
            comment.save()
        if self.issue.status == "RESOLVED":
            self.issue.close()


class Issue(object):
    required_fields = ["sudo", "title", "description", "created_at", "status"]
    data_fields = ["sudo", "title", "description", "created_at", "status", "assignee", "milestone",
                   "labels", "updated_at"]

    def __init__(self):
        self.headers = config.headers

    def validate(self):
        for field in self.required_fields:
            value = getattr(self, field)
            if not value:
                return False
        return True

    def save(self, dry_run=False):
        if not self.validate():
            raise Exception("Validation error")
        url = "{}/projects/{}/issues".format(config.gitlab_base_url, config.gitlab_project_id)
        data = {k:v for k,v in self.__dict__.iteritems() if k in self.data_fields}
        self.headers["sudo"] = self.sudo
        if dry_run:
            pprint(data)
            return 3
        response = _perform_request(url, "post", headers=self.headers, data=data, json=True, paginated=False)
        self.id = response["id"]


    def close(self, dry_run=False):
        url = "{}/projects/{}/issues/{}".format(config.gitlab_base_url, config.gitlab_project_id, self.id)
        data = {
            "state_event" : "close",
            "updated_at": self.updated_at,
        }
        self.headers["sudo"] = self.sudo
        if dry_run:
            pprint(data)
            return
        _perform_request(url, "put", headers=self.headers, data=data)

class Comment(object):

    required_fields = ["sudo", "body", "issue_id", "created_at"]
    data_fields = ["body", "created_at"]

    def __init__(self):
        self.headers = config.headers

    def validate(self):
        for field in self.required_fields:
            value = getattr(self, field)
            if not value:
                print field
                return False
        return True

    def save(self, dry_run=False):
        if not self.validate():
            raise Exception("Validation error")

        self.headers["sudo"] = self.sudo
        url = "{}/projects/{}/issues/{}/notes".format(config.gitlab_base_url, config.gitlab_project_id, self.issue_id)
        data = {k:v for k,v in self.__dict__.iteritems() if k in self.data_fields}
        if dry_run:
            pprint(data)
            return
        _perform_request(url, "post", headers=self.headers, data=data, json=True, paginated=False)


class Attachment(object):
    def __init__(self, user, bugzilla_attachment_id, filename):
        self.id = bugzilla_attachment_id
        self.filename = filename
        self.headers = config.headers

    def save(self):
        url = "{}attachment.cgi?id={}".format(config.bugzilla_base_url, self.id)
        result = _perform_request(url, "get", json=False, paginated=False)

        url = "{}/projects/{}/uploads".format(config.gitlab_base_url, config.gitlab_project_id)
        f = {"file": (self.filename, result.content)}
        attachment = _perform_request(url, "post", headers=self.headers, files=f, json=True,
                                      paginated=False)
        return attachment["markdown"]

def main():
    f = sys.argv[1]
    with open(f, "r") as foo:
        contents = foo.read().splitlines()

    c = MigrationClient()
    c.migrate([34])

if __name__ == "__main__":
    main()
