import sys
from bugzilla2gitlab import Migrator

def main():
    bug_ids = []
    bugzilla_url = "https://www.edom.mi.uni-erlangen.de/bugzilla3/"
    gitlab_url = "https://git.zib.de"
    gitlab_group= "integer"
    gitlab_project = "SCIP"
    client = Migrator(bugzilla=bugzilla_url, gitlab=gitlab_url, gitlab_group=gitlab_group, gitlab_project=gitlab_project, default_user="")
    print("Starting migration...")
    for bid in bug_ids:
        client.move_bug(bid)
    print("Migration complete!")

if __name__ == "__main__":
    main()
