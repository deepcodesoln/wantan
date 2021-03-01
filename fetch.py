import re
import requests
from argparse import ArgumentTypeError
from collections import namedtuple

import auth
from subjects.subjects import Kanji, Radical, Vocabulary

AuthPair = namedtuple("AuthPair", ["user", "key"])

InclusiveRange = namedtuple("InclusiveRange", ["begin", "end"])

BASE_URL = "https://api.wanikani.com/v2/"
AUTH_HEADER = "Authorization: Bearer {}"
ITEM_TYPES = ["kanji", "radical", "vocabulary"]

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
    args.add_argument("--level", type=level_range, default="1-60",
            help="A level or a range of levels, inclusive, as '#-#'")
    args.add_argument("user", help="The WaniKani user to transact as")
    args.add_argument("type", choices=ITEM_TYPES + ["all"], nargs="+",
            help="The type of content to fetch; 'all' fetches every type")
    args.set_defaults(func=main)

def format_levels(levels):
    return ",".join(map(str, list(range(levels.begin, levels.end + 1))))

def format_types(types):
    if "all" in types:
        return ",".join(map(str, ITEM_TYPES))
    else:
        return ",".join(map(str, list(set(types)))) # Remove duplicates.

class BearerAuthentication(requests.auth.AuthBase):
    def __init__(self, key):
        self._key = key
    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self._key}"
        return r

def main(args):
    bearer_auth = BearerAuthentication(auth.get_key(args.user))
    params = {"levels": format_levels(args.level), "types": format_types(args.type)}
    r = requests.get(BASE_URL + "subjects", params=params, auth=bearer_auth)

    kanji = list()
    radicals = list()
    vocabulary = list()
    while True:
        for s in r.json()["data"]:
            if s["object"] == "kanji":
                kanji.append(Kanji.from_wanikani(s["data"]))
            elif s["object"] == "radical":
                radicals.append(Radical.from_wanikani(s["data"]))
            elif s["object"] == "vocabulary":
                vocabulary.append(Vocabulary.from_wanikani(s["data"]))
        next_url = r.json()["pages"]["next_url"]
        if not next_url:
            break
        r = requests.get(next_url, auth=bearer_auth)

    print(f"Num kanji: {len(kanji)}")
    print(f"Num radicals: {len(radicals)}")
    print(f"Num vocabulary: {len(vocabulary)}")
