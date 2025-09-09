#!/usr/bin/env python
"""
@ file utils.py
"""

from nltk import pos_tag
import csv

POS_MAP = {
    "noun": ["NN", "NNS", "NNP", "NNPS"],
    "verb": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"],
    "adjective": ["JJ", "JJR", "JJS"],
    "adverb": ["RB", "RBR", "RBS"]
}


def parse_dictionary(source):
    if source.endswith(".txt"):
        with open(source, encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    else:
        return [word.strip().lower() for word in source.split(",")]


def find_element_words(words, symbols):
    matches = []
    for word in words:
        paths = []
        def dfs(subword, path):
            if not subword:
                paths.append(path[:])
                return
            for sym in symbols:
                if subword.startswith(sym.lower()):
                    path.append(sym)
                    dfs(subword[len(sym):], path)
                    path.pop()
        dfs(word, [])
        if paths:
            matches.append((word, paths[0]))
    return matches


def filter_by_pos(words, target_pos):
    tagged = pos_tag(words)
    allowed_tags = POS_MAP.get(target_pos, [])
    return [word for word, tag in tagged if tag in allowed_tags]


def load_symbols_from_csv(path, column="Cyrillic Symbol"):
    symbols = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = row.get(column)
            if symbol:
                symbols.append(symbol.strip())
    return symbols

