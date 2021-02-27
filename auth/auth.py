import getpass
import keyring

KEYRING_SERVICE = "wantan"

def setup_args(args):
    """Add our args to a subgroup of the main script's."""
    auth_verbs = args.add_mutually_exclusive_group(required=True)
    auth_verbs.add_argument("--dump", action="store_true",
            help="Dump the API key associated with a username")
    auth_verbs.add_argument("--store", action="store_true",
            help="Store an API key associated with a username")
    args.add_argument("--user", required=True,
            help="The username associated with the API key")
    args.add_argument("--key", help="The API key to store")
    args.set_defaults(func=main)

def get_key(user):
    return keyring.get_password(KEYRING_SERVICE, user)

def main(args):
    if args.dump:
        print(f"{get_key(args.user)}")
    elif args.store:
        key = args.key
        if not key:
            key = getpass.getpass(prompt="API key: ")
        keyring.set_password(KEYRING_SERVICE, args.user, key)
