import re
import requests
from argparse import ArgumentTypeError

from collections import namedtuple

AuthPair = namedtuple("AuthPair", ["user", "key"])

InclusiveRange = namedtuple("InclusiveRange", ["begin", "end"])

ITEM_TYPES = ["kanji", "radical", "vocab"]

def level_range(s):
    level_re = "(?P<begin>[0-9]+)(-(?P<end>[0-9]+))?"
    m = re.match(level_re, s)
    if not m:
        raise ArgumentTypeError(
                "--level must be provided a level as '#' or '#-#'; " +\
                "for example '2' or '47-60'")
    md = m.groupdict()
    r = InclusiveRange(int(md["begin"]), int(md["end"] if md["end"] else md["begin"]))
    if not (0 <= r.begin <= 60) or not (0 <= r.end <= 60):
        raise ArgumentTypeError("Levels must be between 0 and 60 inclusive")
    if r.end < r.begin:
        raise ArgumentTypeError("End level must be greater than or equal to begin level")
    return r

def setup_args(args):
    """Add our args to a subgroup of the main script's."""
    args.add_argument("--type", choices=ITEM_TYPES + ["all"], nargs="+",
            required=True,
            help="The type of content to fetch; 'all' fetches every type")
    args.add_argument("--level", type=level_range)
    args.set_defaults(func=main)

def main(args):
    pass
