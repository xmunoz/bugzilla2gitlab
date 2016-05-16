import yaml
import os
from collections import namedtuple
import random

from .utils import _perform_request

Config = namedtuple('Config', ["gitlab_base_url", "gitlab_project_id",
                               "bugzilla_base_url", "bugzilla_auto_reporter",
                               "default_headers", "component_mappings",
                               "bugzilla_users", "gitlab_users", "bugzilla_misc_user",
                               "default_gitlab_labels", "datetime_format_string",
                               "dry_run"])

def get_config(path):
    configuration = {}
    configuration.update(_load_defaults(path))
    configuration.update(_load_user_id_cache(path, configuration["gitlab_base_url"],
                                             configuration["default_headers"]))
    configuration.update(_load_component_mappings(path))
    return Config(**configuration)


def _load_defaults(path):
    with open(os.path.join(path, "defaults.yml")) as f:
        config = yaml.load(f)

    defaults = {}

    for key in config:
        if key == "gitlab_private_token":
            defaults["default_headers"] =  {"private-token": config[key]}
        else:
            defaults[key] = config[key]

    return defaults


def _load_user_id_cache(path, gitlab_url, gitlab_headers):
    '''
    Load cache of GitLab usernames and ids
    '''
    print("Loading user cache...")
    with open(os.path.join(path, "user_mappings.yml")) as f:
        bugzilla_mapping = yaml.load(f)

    gitlab_users = {}
    for user in bugzilla_mapping:
        gitlab_username = bugzilla_mapping[user]
        uid = _get_user_id(gitlab_username, gitlab_url, gitlab_headers)
        gitlab_users[gitlab_username] = uid

    mappings = {}
    # bugzilla_username: gitlab_username
    mappings["bugzilla_users"] = bugzilla_mapping

    # gitlab_username: gitlab_userid
    mappings["gitlab_users"] = gitlab_users

    return mappings


def _get_user_id(username, gitlab_url, headers):
    url = "{}/users?username={}".format(gitlab_url, username)
    result = _perform_request(url, "get", headers=headers, dry_run=True)
    if result and isinstance(result, list):
        return result[0]["id"]
    else:
        raise Exception("No gitlab account found for user {}".format(username))


def _load_component_mappings(path):
    with open(os.path.join(path, "component_mappings.yml")) as f:
        component_mappings = yaml.load(f)

    return {"component_mappings": component_mappings}

