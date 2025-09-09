#!/usr/bin/env python
"""
@file : core.py

mendeleevspellingbee
"""

import sys
import argparse
from mendeleevspellingbee import __version__
from mendeleevspellingbee.symbols import SYMBOL_SETS
from mendeleevspellingbee.utils import parse_dictionary, find_element_words
from mendeleevspellingbee.utils import filter_by_pos, load_symbols_from_csv

def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Decode words using chemical element symbols"
    )
    ap.add_argument("-d", "--dictionary", required=True,
                    help="Comma-separated words or path to dictionary file")
    ap.add_argument("-s", "--symbol-list",
                    help="Comma-delimited symbols or built-in set name")
    ap.add_argument("-c", "--symbol-csv",
                    help="Path to CSV file containing custom symbol list")
    ap.add_argument("-p", "--part-of-speech",
                    choices=["noun", "verb", "adjective", "adverb"],
                    help="Filter words by part of speech (English only)")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args(argv)

    symbols = load_symbols(args)
    words = parse_dictionary(args.dictionary)

    if args.part_of_speech:
        words = filter_by_pos(words, args.part_of_speech)

    matches = find_element_words(words, symbols)
    for word, path in matches:
        print(f"{word} => {'|'.join(path)}")


def load_symbols(args):
    """
    Load symbol list based on CLI arguments.
    Priority:
    1. External CSV file (--symbol-csv)
    2. Named built-in set (--symbol-list = latin|cyrillic)
    3. Raw comma-delimited string (--symbol-list = H,He,Li,...)
    """
    if args.symbol_csv:
        try:
            symbols = load_symbols_from_csv(args.symbol_csv)
            if not symbols:
                raise ValueError("CSV loaded but no symbols found.")
            return symbols
        except Exception as e:
            print(f"[ERROR] Failed to load symbols from CSV: {e}")
            exit(1)

    if args.symbol_list:
        key = args.symbol_list.lower()
        if key in SYMBOL_SETS:
            return SYMBOL_SETS[key]
        else:
            return [s.strip() for s in args.symbol_list.split(",") if s.strip()]

    print("[ERROR] No symbol source provided. Use --symbol-list or --symbol-csv.")
    exit(1)


if __name__ == "__main__":
    sys.exit(main())

