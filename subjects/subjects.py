import logging
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
        self.sort_field = ""
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
        c.sort_field = f"{c.level:02}" + "_1"
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
        v = next(self._values)
        if type(v) == list:
            return ", ".join(v)
        return v

class Radical:
    def __init__(self):
        self.slug = ""
        self.characters = ""
        self.character_svg = ""
        self.level = 0
        self.sort_field = ""
        self.meanings = [] # List of str.
        self.meaning_mnemonic = ""

    def csv_iter(self):
        return RadicalIterator(self)

    @classmethod
    def from_wanikani(cls, json):
        """json is the r["data"][n]["data"] of a response from WaniKani."""
        c = cls()
        c.slug = json["slug"]
        c.characters = json["characters"]
        for i in json["character_images"]:
            if i["content_type"] == "image/svg+xml" and\
               "inline_styles" in i["metadata"] and\
               i["metadata"]["inline_styles"] == False:
                c.character_svg = i["url"]
                break
        if c.character_svg == "":
            logging.warning(f"Radical with slug '{json['slug']}' has no svg")
        if c.characters is None or c.characters == "":
            logging.warning(f"Radical with slug '{json['slug']}' has no characters")
        c.level = json["level"]
        c.sort_field = f"{c.level:02}" + "_0"
        c.meanings = [m["meaning"] for m in json["meanings"]]
        c.meaning_mnemonic = json["meaning_mnemonic"]
        return c

    def __str__(self):
        return f"{self.characters}\n" +\
               f"{self.character_svg}\n" +\
               f"{self.level}\n" +\
               f"{self.meanings}\n" +\
               f"{self.meaning_mnemonic}"

class VocabularyIterator:
    def __init__(self, vocabulary):
        self._values = iter(vars(vocabulary).values())

    def __iter__(self):
        return self

    def __next__(self):
        v = next(self._values)
        if type(v) == list:
            if type(v[0]) == SentencePair:
                div_en = '<div class="context-sentence-en">'
                div_jp = '<div class="context-sentence-jp">'
                div_end = "</div>"
                string = ""
                for pair in v:
                    string += div_en + pair.en + div_end + div_jp + pair.jp + div_end
                return string
            else:
                return ", ".join(v)
        return v

SentencePair = namedtuple("SentencePair", ["en", "jp"])

class Vocabulary:
    def __init__(self):
        self.characters = ""
        self.level = 0
        self.sort_field = ""
        self.meanings = [] # List of str.
        self.readings = [] # List of str.
        self.parts_of_speech = [] # List of str.
        self.meaning_mnemonic = ""
        self.reading_mnemonic = ""
        self.context_sentences = [] # List of SentencePair.

    def csv_iter(self):
        return VocabularyIterator(self)

    @classmethod
    def from_wanikani(cls, json):
        c = cls()
        c.characters = json["characters"]
        c.level = json["level"]
        c.sort_field = f"{c.level:02}" + "_2"
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
