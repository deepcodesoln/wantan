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

# Get everything; we recommend you print diagnostics since this takes some time.
./wantan.py fetch --log-level info --out ./out <you> all
```

# Importing to Anki

When importing CSV files created by wantan, configure Anki to use a comma as a
field separator and to allow HTML in fields.

## Note Types

Use notes with the following fields to import all data for the corresponding item.

Each item features a field called `sort_field`. This member is used for sorting
in Anki. It is formatted as `<level>_(0|1|2)`, where `level` is the item's
corresponding WaniKani level, 0 indicates a radical, 1 indicates kanji, and 2
indicates vocabulary. With this schema, we can group all items of the same level
and prioritize radicals, then kanji, and then vocabulary in Anki as is done on
WaniKani. `sort_field` is not meant to be rendered in cards.

**Kanji**:

1. Characters
1. Level
1. Sort Field
1. Meanings
1. Readings Onyomi
1. Readings Kunyomi
1. Readings Nanori
1. Meaning Mnemonic
1. Meaning Hint
1. Reading Mnemonic
1. Reading Hint

**Radicals**:

1. Characters
1. Character SVG
1. Level
1. Sort Field
1. Meanings
1. Meaning Mnemonic

**Vocabulary**:

1. Characters
1. Level
1. Sort Field
1. Meanings
1. Rreadings
1. Parts of Speech
1. Meaning Mnemonic
1. Reading Mnemonic
1. Context Sentences

## Card Types

Not all radicals have printable characters, but all have renderable SVGs.
Without additional styling, the SVGs will scale to the size of the card.
Consider adding something like the following to your radical card type to
constrain the size of the SVG.

```css
svg {
  width: 100px;
  height: 100px;
}
```

If you want to hide the text characters if you render SVGs in the same card, you
can conditionally render the characters based on the SVG presence as follows:

```
{{^Character SVG}}{{Characters}}{{/Character SVG}}
```
