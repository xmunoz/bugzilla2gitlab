from .utils import get_bugzilla_bug, validate_list
from .models import IssueThread
from .config import get_config


class Migrator(object):
    def __init__(self, config_path):
        self.conf = get_config(config_path)

    def migrate(self, bug_list):
        '''
        Migrate a list of bug ids from Bugzilla to GitLab.
        '''
        validate_list(bug_list)
        for bug in bug_list:
            self.migrate_one(bug)

    def migrate_one(self, bugzilla_bug_id):
        '''
        Migrate a single bug from Bugzilla to GitLab.
        '''
        print("Migrating bug {}".format(bugzilla_bug_id))
        fields = get_bugzilla_bug(self.conf.bugzilla_base_url, bugzilla_bug_id)
        issue_thread = IssueThread(self.conf, fields)
        issue_thread.save()

