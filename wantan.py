#!/usr/bin/python3 -B

import argparse

import auth
import fetch

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="sub-command help")

    auth_group = subparsers.add_parser("auth", help="WaniKani API key management")
    auth.setup_args(auth_group)

    fetch_group = subparsers.add_parser("fetch", help="Fetch WaniKani content")
    fetch.setup_args(fetch_group)

    return parser.parse_args()

def main():
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
