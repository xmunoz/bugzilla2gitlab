import argparse

def main():
    parser = argparse.ArgumentParser(description='Migrate bugs from bugzilla to gitlab.')
    parser.add_argument('bug_list', metavar="[FILE]",
                        help="A file containing a list of bugzilla bug numbers to migrate,"
                        " one per line.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't perform any PUT or POST requests.")
    args = parser.parse_args()

    with open(args.bug_list, "r") as f:
        bugs = f.read().splitlines()

    from bugzilla2gitlab import MigrationClient
    client = MigrationClient()
    client.migrate(bugs, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
