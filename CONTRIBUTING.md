# Contributing

This project adheres to the [Contributor Covenant Code of Conduct](http://contributor-covenant.org/version/1/4/). By participating, you are expected to honor this code.

## Getting started

The best way to start developing this project is to set up a virtualenv and install the requirements.

    git clone <my remote url/bugzilla2gitlab.git>
    cd bugzilla2gitlab 
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

Run tests to confirm that everything is set up properly.

    pytest

## Submitting a pull request

1. Fork this repository
2. Create a branch: `git checkout -b my_feature`
3. Make changes
4. Run the commands in the [build file](.travis.yml) locally to ensure a passing build
5. Commit: `git commit -am "Great new feature that closes #3"`. Reference any related issues in the first line of the commit message.
6. Push: `git push origin my_feature`
7. Open a pull request in Github
8. Pat yourself on the back for making an open source contribution :)

## Other considerations

- Please review the open issues before opening a PR.
- Significant changes or new features should be documented in [`README.md`](https://github.com/xmunoz/bugzilla2gitlab/blob/master/README.md).
- Writing tests is never a bad idea. Make sure all tests are passing before opening a PR.
