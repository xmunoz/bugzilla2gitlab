import yaml
import requests
import os
from helpers import _perform_request

class Config(object):
    def __init__(self, path):
        with open(os.path.join(path, "defaults.yml")) as f:
            config = yaml.load(f)

        for key in config:
            setattr(self, key, config[key])

        with open(os.path.join(path, "user_mappings.yml")) as f:
            user_mapping = yaml.load(f)

        self._load_default_headers()
        self._load_user_id_cache(user_mapping)

    def _load_default_headers(self):
        setattr(self, "headers", {"private-token": self.gitlab_private_token})

    def _load_user_id_cache(self, user_mapping):
        '''
        Load cache of gitlab usernames and ids
        '''
        print("Loading user cache...")
        bugzilla_users = user_mapping
        gitlab_users = {}
        for user in user_mapping:
            gitlab_username = user_mapping[user]
            uid = self._get_user_id(gitlab_username)
            gitlab_users[gitlab_username] = uid

        self.bugzilla_users = bugzilla_users
        self.gitlab_users = gitlab_users

    def _get_user_id(self, username):
        url = "{}/users?username={}".format(self.gitlab_base_url, username)
        print("get {}".format(url))
        result = _perform_request(url, "get", headers=self.headers)
        if result and isinstance(result, list):
            return result[0]["id"]
        else:
            raise Exception("No gitlab account found for user {}".format(username))

