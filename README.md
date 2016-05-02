# bugzilla2gitlab

## Usage

Information about run options:

```
python bin/run_migrator.py -h
```

Ensure that the configuration for the source and target instances is set correctly in `bugzilla2gitlab/config/defaults.yml`.

## Rationale

Currently, our source code is hosted with the GitLab front-end. In an effort bring our bugs and the code closer together, the idea to migrate away from Bugzilla to the GitLab issues was prosed by members of the MOM group. The first phase of this project was a new bug reporting form on [scip.zib.de](http://scip.zib.de/bugs.php) that automatically creates [issues in the SCIP repository](https://git.zib.de/integer/scip/issue). The second phase is moving all of our bugs from Bugzilla into Gitlab Issues with this script.

## Bug list

The list of bug_ids to be migrated can be found in `bugs.txt`. This file contains the values in `range(2,944)` with these exclusions: 2,3,4,5,6,7,8,20,58,59,79,81,82,83,84,85,86,87,88,573,736,758,759. The excluded bugzilla bugs are "test" issues, unrelated to SCIP or SoPlex. There are some issues in bugzilla that relate to SoPlex. They will be nonetheless migrated to the SCIP repository.

## Mappings

Please see `config/users_mappings.yml` for the mappings between bugzilla and gitlab users. Users with the designation "ghost" are no longer with ZIB or simply machine users (e.g. scipweb user), and will leave comments under a generic "ghost" account.

Components are also mapped to gitlab issue labels in `config/component_mappings.yml`.


## Tools

### GitLab

Gitlab has a comprehensive and extensively documented API. Here are the main endpoints that this library makes use of.
    - [Creating new issues](http://doc.gitlab.com/ce/api/issues.html#new-issue)
    - [Adding comments to issues](http://doc.gitlab.com/ce/api/notes.html)
    - [Uploading files](http://doc.gitlab.com/ce/api/projects.html#upload-a-file)
    - [Changing an issue status](http://doc.gitlab.com/ce/api/issues.html#edit-issue)
    - [Getting user ids](http://doc.gitlab.com/ce/api/users.html#for-admins)


Calls to the Gitlab API must be made with an administrator private token in order to [impersonate other users](http://doc.gitlab.com/ce/api/#sudo).`

### Bugzilla

The bugzilla installation that we make use of doesn't have [any](https://www.edom.mi.uni-erlangen.de/bugzilla3/xmlrpc.cgi) [RPC](https://www.edom.mi.uni-erlangen.de/bugzilla3/jsonrpc.cgi) webclients installed, so the bugs were simply migrated by `GET`-ing the bug url with an extra query string (`ctype=xml`) appended to the url to render the bug content as xml.

## Caveats

Every comment or merge request in Gitlab typically sends a notification. This is true even for comments/issues created programatically. To avoid users inboxes being flooded with meaningless email notifications and avoid overwhelming your SMTP servers, users should disable all email notifications (global and group-specific) just prior to the running of this script. This can be done through the [gitlab UI](https://git.zib.de/profile/notifications).
