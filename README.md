# Wantan

The **Wan**iKani **T**o **An**ki tool. This tool fetches WaniKani
content and prepares it for use in Anki.

# Dependencies

- Active WaniKani API key
- Python3
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
./wantan.py fetch --level 1 <you> kanji

# Get all radicals for levels 5-10
./wantan.py fetch --level 5-10 <you> radical

# Get everything for level 20
./wantan.py fetch --level 20 <you> all
```
