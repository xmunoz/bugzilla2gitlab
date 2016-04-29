# Rationale
Bugzilla is a bug tracking system used at SCIP. Currently, our source code is hosted with the GitLab front-end. In an effort bring our bugs and the code closer together, the idea to migrate from Bugzilla to the GitLab issues has been introduced.

# Bug list
The list of bug_ids to be migrated can be found in `bugs.txt`. This file contains the values in `range(2,944)` with these exclusions: 2,3,4,5,6,7,8,20,58,59,79,81,82,83,84,85,86,87,88,573,736,758,759. The excluded bugzilla bugs are "test" issues, unrelated to SCIP or SoPlex.

# Mappings

Please see `config/users_mappings.yml` for the mappings between bugzilla and gitlab users. Users with the designation "ghost" are no longer with ZIB or simply machine users (e.g. scipweb user), and will leave comments under a generic "ghost" account.

Components are also mapped to gitlab issue labels in `config/component_mappings.yml`.


# Tools

- GitLab API Documentation
    - [Creating new issues](http://doc.gitlab.com/ce/api/issues.html#new-issue)
    - [Adding comments to issues](http://doc.gitlab.com/ce/api/notes.html)
- Bugzilla XML documentation
    -  [WebClient](https://www.bugzilla.org/docs/4.4/en/html/api/Bugzilla/WebService.html)

Calls to the Gitlab API must be made with an administrator private token in order to [impersonate other users](http://doc.gitlab.com/ce/api/#sudo).`

# Open Questions

1. If we go the approach of preserving the users who opened the issues/comments, then I will need access to the administrator private token.
    - Spammy inboxes
    - People that are no longer employed within ZIB/old accounts will be posted by a ghost user.

2. Referencing users in comments: @ or simply plaintext name?
    - spammy inboxes are again a concern

3. The metadata section. I envision this will be just a text section that the top with a couple of predefined key-value pairs.
