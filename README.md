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
./wantan auth --store --user <you> --key <your_key>
# Interactive
./wantan auth --store --user <you>

./wantan auth --dump --user <you>
```
