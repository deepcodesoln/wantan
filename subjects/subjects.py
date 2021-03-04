import sys
from collections import namedtuple

class KanjiIterator:
    def __init__(self, kanji):
        self._values = iter(vars(kanji).values())

    def __iter__(self):
        return self

    def __next__(self):
        v = next(self._values)
        if type(v) == list:
            return ", ".join(v)
        return v

class Kanji:
    def __init__(self):
        self.characters = ""
        self.level = 0
        self.meanings = [] # List of str.
        self.readings_onyomi = [] # List of str.
        self.readings_kunyomi = [] # List of str.
        self.readings_nanori = [] # List of str.
        self.meaning_mnemonic = ""
        self.meaning_hint = ""
        self.reading_mnemonic = ""
        self.reading_hint = ""

    def csv_iter(self):
        return KanjiIterator(self)

    @classmethod
    def from_wanikani(cls, json):
        """json is the r["data"][n]["data"] of a response from WaniKani."""
        c = cls()
        c.characters = json["characters"]
        c.level = json["level"]
        c.meanings = [m["meaning"] for m in json["meanings"]]
        c.readings_onyomi = [r["reading"] for r in json["readings"] if r["type"] == "onyomi"]
        c.readings_kunyomi = [r["reading"] for r in json["readings"] if r["type"] == "kunyomi"]
        c.readings_nanori = [r["reading"] for r in json["readings"] if r["type"] == "nanori"]
        c.meaning_mnemonic = json["meaning_mnemonic"]
        c.meaning_hint = json["meaning_hint"]
        c.reading_mnemonic = json["reading_mnemonic"]
        c.reading_hint = json["reading_hint"]
        return c

    def __str__(self):
        return f"{self.characters}\n" +\
               f"{self.level}\n" +\
               f"{self.meanings}\n" +\
               f"{self.readings_onyomi}\n" +\
               f"{self.readings_kunyomi}\n" +\
               f"{self.readings_nanori}\n" +\
               f"{self.meaning_mnemonic}\n" +\
               f"{self.meaning_hint}\n" +\
               f"{self.reading_mnemonic}\n" +\
               f"{self.reading_hint}"

class RadicalIterator:
    def __init__(self, radical):
        self._values = iter(vars(radical).values())

    def __iter__(self):
        return self

    def __next__(self):
        r = next(self._values)
        if type(r) == list:
            return ", ".join(r)
        return r

class Radical:
    def __init__(self):
        self.characters = ""
        self.character_svg = ""
        self.level = 0
        self.meanings = [] # List of str.
        self.meaning_mnemonic = ""

    def csv_iter(self):
        return RadicalIterator(self)

    @classmethod
    def from_wanikani(cls, json):
        """json is the r["data"][n]["data"] of a response from WaniKani."""
        c = cls()
        c.characters = json["characters"]
        for i in json["character_images"]:
            if i["content_type"] == "image/svg+xml" and i["metadata"].get("inline_styles", False):
                c.character_svg = i["url"]
                break
        if c.character_svg == "":
            print(f"Radical with slug '{json['slug']}' has no svg", file=sys.stderr)
        if c.characters is None or c.characters == "":
            print(f"Radical with slug '{json['slug']}' has no characters", file=sys.stderr)
        c.level = json["level"]
        c.meanings = [m["meaning"] for m in json["meanings"]]
        c.meaning_mnemonic = json["meaning_mnemonic"]
        return c

    def __str__(self):
        return f"{self.characters}\n" +\
               f"{self.character_svg}\n" +\
               f"{self.level}\n" +\
               f"{self.meanings}\n" +\
               f"{self.meaning_mnemonic}"

SentencePair = namedtuple("SentencePair", ["en", "jp"])

class Vocabulary:
    def __init__(self):
        self.characters = ""
        self.level = 0
        self.meanings = [] # List of str.
        self.readings = [] # List of str.
        self.parts_of_speech = [] # List of str.
        self.meaning_mnemonic = ""
        self.reading_mnemonic = ""
        self.context_sentences = [] # List of SentencePair.

    @classmethod
    def from_wanikani(cls, json):
        c = cls()
        c.characters = json["characters"]
        c.level = json["level"]
        c.meanings = [m["meaning"] for m in json["meanings"]]
        c.readings = [r["reading"] for r in json["readings"]]
        c.parts_of_speech = json["parts_of_speech"]
        c.meaning_mnemonic = json["meaning_mnemonic"]
        c.reading_mnemonic = json["reading_mnemonic"]
        for cs in json["context_sentences"]:
            c.context_sentences.append(SentencePair(cs["en"], cs["ja"]))
        return c

    def __str__(self):
        return f"{self.characters}\n" +\
               f"{self.level}\n" +\
               f"{self.meanings}\n" +\
               f"{self.readings}\n" +\
               f"{self.parts_of_speech}\n" +\
               f"{self.meaning_mnemonic}\n" +\
               f"{self.reading_mnemonic}\n" +\
               f"{[[cs.en, cs.jp] for cs in self.context_sentences]}"
