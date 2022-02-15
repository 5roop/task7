from parse import compile
import logging
import pandas as pd
from typing import Set, List
from transliterate import translit
chars_to_remove = {
    '!',
    '"',
    '#',
    '%',
    '&',
    "'",
    '(',
    ')',
    '*',
    '+',
    ',',
    '-',
    '.',
    '/',
    ':',
    ';',
    '<',
    '=',
    '>',
    '?',
    '[',
    ']',
    '_',
    '`',
    '«',
    '°',
    '²',
    '³',
    'µ',
    '·',
    '»',
    '½',
    '‑',
    '–',
    '‘',
    '’',
    '“',
    '”',
    '„',
    '•',
    '…',
    '‰',
    '″',
    '₂',
    '₃',
    '€',
    '™',
    '→',
    '−',
    '∕',
    '😀',
    '😉',
    '🙁',
    '🙂'

}

def process_flags(flags:str) -> set:
    flags = flags.split(" ")
    flags = [flag for flag in flags if flag in ["A", "B", "Z"]]
    return set(flags)

def process_item(item:str) -> dict:
    pattern = """{flags1}: {version1} / {flags2}: {version2}"""
    p = compile(pattern)
    resulting_dict = dict()
    lines = item.split("\n")
    for line in lines[1:]:
        line = line.split(" | ")[0]
        if line.startswith("#") or line == "":
            continue
        try:
            results = p.parse(line)

            flags1 = process_flags(results["flags1"])
            flags2 = process_flags(results["flags2"])

            version1 = results["version1"].replace("_", " ").casefold()
            version2 = results["version2"].replace("_", " ").casefold()
            
            if (flags1, flags2) == ({"A"}, {"B"}):
                resulting_dict[version1] = "A"
                resulting_dict[version2] = "B"
            if (flags1, flags2) == ({"A", "Z"}, {"B"}):
                resulting_dict[version2] = "B"
        except Exception as e:
            logging.debug(f"Found error {e} for line:")
            logging.debug(line)

    return resulting_dict

def get_lexicon():
    f = "varcon.txt"
    with open(f, "r") as file:
        content = file.read()
    items = content.split("# ")[1:]
    results = {}
    for item in items:
        results.update(process_item(item))

    return results