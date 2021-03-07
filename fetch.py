import csv
import logging
import re
import requests
from argparse import ArgumentTypeError
from collections import namedtuple
from os import getcwd, makedirs, path

import auth
from subjects.subjects import Kanji, Radical, Vocabulary

AuthPair = namedtuple("AuthPair", ["user", "key"])

InclusiveRange = namedtuple("InclusiveRange", ["begin", "end"])

BASE_URL = "https://api.wanikani.com/v2/"
AUTH_HEADER = "Authorization: Bearer {}"
ITEM_TYPES = ["kanji", "radical", "vocabulary"]
LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
}

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
            help="A level ('#') or an inclusive range ('#-#')s; default: '1-60'")
    args.add_argument("--out", default="./",
            help="The output directory to write files in; default: './'")
    args.add_argument("--log-level", default="warning",
            choices=[k for k in LOG_LEVELS.keys()],
            help="The verbosity of this tool; default: warning")
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

def write_csv_file(filename, csv_iterable):
    with open(filename, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, dialect="unix")
        for i in csv_iterable:
            csv_writer.writerow(i.csv_iter())

def main(args):
    logging.basicConfig(level=LOG_LEVELS[args.log_level])

    outdir = path.join(getcwd(), args.out)
    makedirs(outdir, exist_ok=True)

    bearer_auth = BearerAuthentication(auth.get_key(args.user))
    params = {"levels": format_levels(args.level), "types": format_types(args.type)}
    r = requests.get(BASE_URL + "subjects", params=params, auth=bearer_auth)

    kanji = list()
    radicals = list()
    vocabulary = list()
    total_count = 0
    while True:
        new_ammount = r.json()["total_count"]
        logging.info(f"Processing next {new_ammount} items ({total_count} so far)")
        total_count += new_ammount

        for s in r.json()["data"]:
            if s["object"] == "kanji":
                kanji.append(Kanji.from_wanikani(s["data"]))
            elif s["object"] == "radical":
                radical = Radical.from_wanikani(s["data"])
                if radical.character_svg:
                    radical.character_svg = requests.get(radical.character_svg).text
                radicals.append(radical)
            elif s["object"] == "vocabulary":
                vocabulary.append(Vocabulary.from_wanikani(s["data"]))


        next_url = r.json()["pages"]["next_url"]
        if not next_url:
            break
        r = requests.get(next_url, auth=bearer_auth)

    if "all" in args.type or "kanji" in args.type:
        write_csv_file(path.join(outdir, "kanji.csv"), kanji)
    if "all" in args.type or "radical" in args.type:
        write_csv_file(path.join(outdir, "radicals.csv"), radicals)
    if "all" in args.type or "vocabulary" in args.type:
        write_csv_file(path.join(outdir, "vocabulary.csv"), vocabulary)
