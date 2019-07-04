#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("bugzilla2gitlab/version.py") as f:
    exec(f.read())

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

kwargs = {
    "name": "bugzilla2gitlab",
    "version": str(__version__),
    "packages": ["bugzilla2gitlab"],
    "description": "An opinionated Bugzilla to Gitlab Issues bug migration tool",
    "long_description": long_description,
    "long_description_content_type": 'text/markdown',
    "author": "Cristina Muñoz",
    "maintainer": "Cristina Muñoz",
    "author_email": "hi@xmunoz.com",
    "maintainer_email": "hi@xmunoz.com",
    "license": "MIT",
    "install_requires": required,
    "url": "https://github.com/xmunoz/bugzilla2gitlab",
    "download_url": "https://github.com/xmunoz/bugzilla2gitlab/archive/master.tar.gz",
    "keywords": "bugzilla gitlab bugtracking workflow",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**kwargs)
