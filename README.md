# Wantan

The **Wan**iKani **T**o **An**ki tool. This tool fetches WaniKani
content and prepares it for use in Anki.

# Dependencies

- Active WaniKani API key
- Python 3.7+ (for guaranteed insertion-ordered dicts)
- (Python) keyring

# Usage

Managing your API key:

```sh
# Non-interactive
./wantan.py auth --store --user <you> --key <your_key>
# Interactive
./wantan.py auth --store --user <you>

./wantan.py auth --dump --user <you>
```

Fetching content:

```sh
# Get all kanji for level 1
./wantan.py fetch --out ./out --level 1 <you> kanji

# Get all radicals for levels 5-10
./wantan.py fetch --out ./out --level 5-10 <you> radical

# Get everything for level 20
./wantan.py fetch --out ./out --level 20 <you> all
```

# Importing to Anki

When importing CSV files created by wantan, configure Anki to use a comma as a
field separator and to allow HTML in fields.

## Note Types

Use notes with the following fields to import all data for the corresponding item.

**Kanji**:

1. Characters
1. Level
1. Meanings
1. Readings Onyomi
1. Readings Kunyomi
1. Readings Nanori
1. Meaning Mnemonic
1. Meaning Hint
1. Reading Mnemonic
1. Reading Hint
