from bugzilla2gitlab.models import *
from bugzilla2gitlab.config import Config, _get_user_id
import random


def test_math():
    assert 1 != 2

'''
def test_Migrator(monkeypatch):
    def mockreturn(one, two, three):
        return random.randint(0,100)
    monkeypatch.setattr(bugzilla2gitlab.config, '_get_user_id', mockreturn)
    issue_thread = IssueThread()
'''
