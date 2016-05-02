import yaml
import os
from helpers import _perform_request

class Config(object):
    def __init__(self, path):
        self.path = path
        self._load_defaults()
        self._load_closed_statuses()
        self._load_user_id_cache()
        self._load_component_mappings()

    def _load_defaults(self):
        with open(os.path.join(self.path, "defaults.yml")) as f:
            config = yaml.load(f)

        for key in config:
            setattr(self, key, config[key])

        self._load_default_headers()

    def _load_default_headers(self):
        setattr(self, "headers", {"private-token": self.gitlab_private_token})

    def _load_closed_statuses(self):
        with open(os.path.join(self.path, "closed_statuses.yml")) as f:
            statuses = yaml.load(f)
        self.closed_statuses = statuses

    def _load_user_id_cache(self):
        '''
        Load cache of gitlab usernames and ids
        '''
        print("Loading user cache...")
        with open(os.path.join(self.path, "user_mappings.yml")) as f:
            bugzilla_mapping = yaml.load(f)

        gitlab_users = {}
        for user in bugzilla_mapping:
            gitlab_username = bugzilla_mapping[user]
            uid = self._get_user_id(gitlab_username)
            gitlab_users[gitlab_username] = uid

        # bugzilla_username: gitlab_username
        self.bugzilla_users = bugzilla_mapping
        # gitlab_username: gitlab_userid
        self.gitlab_users = gitlab_users

    def _get_user_id(self, username):
        url = "{}/users?username={}".format(self.gitlab_base_url, username)
        print("get {}".format(url))
        result = _perform_request(url, "get", headers=self.headers)
        if result and isinstance(result, list):
            return result[0]["id"]
        else:
            raise Exception("No gitlab account found for user {}".format(username))

    def _load_component_mappings(self):
        with open(os.path.join(self.path, "component_mappings.yml")) as f:
            component_mappings = yaml.load(f)

        self.component_mappings = component_mappings

