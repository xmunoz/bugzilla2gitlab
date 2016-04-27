from xml.etree import ElementTree
import argparse
from datetime import datetime
import os.path
import yaml
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

    def migrate_one(self, bugzilla_bug_id):
        a = Comment("cristina", "hi")

    def _get_bugzilla_bug(self, bug_id):
        full_url = "{}{}{}".format(self.bugzilla_url, "show_bug.cgi?ctype=xml&id=", bug_id)
        response = requests.get(full_url)
        tree = ElementTree.fromstring(response.content)
        bug_fields = {}
        for bug in root:
            for fields in bug:
                if fields.tag == "long_desc":
                    bug_fields["comment"] = field.attrib
                else:
                    bug_fields[field.tag] = field.attrib

        print(bug_fields)


class IssueThread(object):

    def save(self):
        issue_id = self.issue.save()
        for comment in self.comments:
            commment.save(self.issue.id)
        if self.issue.status == "closed":
            self.issue.close()


class Issue(object):
    def __init__(self, reporter, title, description, assignee=None, milestone=None, labels=[],
                create_date=None, status="open", close_date=None):
        self.user_id = reporter
        self.title = title
        self.description = description
        self.assignee = assignee
        self.milestone = milestone
        self.labels = labels
        self.status = status
        self.created_at= create_date
        self.updated_at = close_date

        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().isoformat()

    def save(self):
        url = "{}/projects/{}/issues".format(config.base_url, config.project_id)
        self.headers["sudo"] = self.user_id
        data = self.__dict__
        self.id = _perform_request(url, "post", headers=self.headers, data=data)


    def close(self):
        url = "{}/projects/{}/issues/{}".format(config.base_url, config.project_id, self.issue_id)
        data = {
            "state_event" : "close",
            "updated_at": self.issue.close_date,
        }
        _perform_request(url, "put", headers=self.headers, data=data)

class Comment(object):
    def __init__(self, user, body, created_at=None):
        self.user_id = user
        self.body = body
        self.created_at = created_at

    def save(self, issue_id):
        self.headers["sudo"] = self.user_id
        url = "{}/projects/{}/issues/{}/notes".format(config.base_url, config.project_id, issue_id)
        data = self.__dict__
        comment_id = _perform_request(url, "post", headers=self.headers, data=data)


class Attachment(object):
    def __init__(self, id, filename):
        self.id = id
        self.filename = filename

    def save(self):
        url = "{}/projects/{}/uploads".format(config.base_url, config.project_id)
        data = self.__dict__
        attachment = _perform_request(url, "post", headers=self.headers, data=data)
        return attachment

