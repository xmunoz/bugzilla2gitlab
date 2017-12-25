import os.path
import random

from bugzilla2gitlab import Migrator
import bugzilla2gitlab.config
import bugzilla2gitlab.utils

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "test_data")


def test_config(monkeypatch):

    def mockreturn(username, gitlab_url, headers):
        return random.randint(0, 100)

    def mockmilestones(project_id, gitlab_url, headers):
        return {"gitlab_milestones": {"Foo": 1}}

    # monkeypatch config method that performs API calls to return a random int instead
    monkeypatch.setattr(bugzilla2gitlab.config, '_get_user_id', mockreturn)
    monkeypatch.setattr(bugzilla2gitlab.config, '_load_milestone_id_cache', mockmilestones)
    conf = bugzilla2gitlab.config.get_config(os.path.join(TEST_DATA_PATH, "config"))
    assert isinstance(conf, bugzilla2gitlab.config.Config)
    '''
    test all config keys to ensure the correct type and value
    '''
    # conf.dry_run is a boolean value
    assert isinstance(conf.dry_run, bool)

    # conf.bugzilla users is dictionary of bugzilla username => gitlab username
    assert isinstance(conf.bugzilla_users, dict)

    # conf.gitlab_users is a dictionary of gitlab username => gitlab user id
    assert isinstance(conf.gitlab_users, dict)

    # sanity check
    assert sorted(conf.bugzilla_users.values()) == sorted(conf.gitlab_users.keys())

    # conf.default_gitlab_labels is a list
    assert isinstance(conf.default_gitlab_labels, list)

    # conf.default_headers are the default headers to use when making gitlab api calls
    assert isinstance(conf.default_headers, dict)
    assert "private-token" in conf.default_headers

    # conf.compnent mappings is a dictionary
    assert isinstance(conf.component_mappings, dict)

    # conf.map_operating_system is a boolean value
    assert isinstance(conf.map_operating_system, bool)

    # conf.map_keywords is a boolean value
    assert isinstance(conf.map_keywords, bool)

    # conf.keywords_to_skip is a dictionary
    assert isinstance(conf.keywords_to_skip, list)

    # conf.map_milestones is a boolean value
    assert isinstance(conf.map_milestones, bool)

    # conf.milestones_to_skip is a list
    assert isinstance(conf.milestones_to_skip, list)

    # conf.gitlab_milestones is a dictionary
    assert isinstance(conf.gitlab_milestones, dict)


def test_Migrator(monkeypatch):
    bug_id = 103

    def mock_getuserid(username, gitlab_url, headers):
        return random.randint(0, 100)

    def mock_loadmilestoneidcache(project_id, gitlab_url, headers):
        return {"gitlab_milestones": {"Foo": 1}}

    def mock_fetchbugcontent(url, bug_id):
        bug_file = "bug-{}.xml".format(bug_id)
        with open(os.path.join(TEST_DATA_PATH, bug_file), "r") as f:
            content = f.read()
        return content

    # monkeypatch config method that performs API calls to return a random int instead
    monkeypatch.setattr(bugzilla2gitlab.config, '_get_user_id', mock_getuserid)
    monkeypatch.setattr(bugzilla2gitlab.config, '_load_milestone_id_cache',
                        mock_loadmilestoneidcache)
    monkeypatch.setattr(bugzilla2gitlab.utils, '_fetch_bug_content', mock_fetchbugcontent)

    # just test that it works without throwing any exceptions
    client = Migrator(os.path.join(TEST_DATA_PATH, "config"))
    client.migrate([bug_id])
