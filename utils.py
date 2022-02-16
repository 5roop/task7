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
    pattern2 = """{flags1}: {version1} / {flags2}: {version2} / {flags3}: {version3}"""
    p2 = compile(pattern2)
    pattern3 = """{flags1}: {version1} / {flags2}: {version2} / {flags3}: {version3} / {flags4}: {version4}"""
    p3 = compile(pattern3)
    resulting_dict = dict()
    lines = item.split("\n")
    for line in lines[1:]:
        if "|" in line:
            continue
        if line.startswith("#") or line == "":
            continue
        if line.count("/") == 1:
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
                logging.debug(f"Found error {e} for line:\n\t{line}")
        elif line.count("/") == 2:
            try:
                results = p2.parse(line)
                flags1 = process_flags(results["flags1"])
                flags2 = process_flags(results["flags2"])
                flags3 = process_flags(results["flags3"])
                version1 = results["version1"].replace("_", " ").casefold()
                version2 = results["version2"].replace("_", " ").casefold()
                version3 = results["version3"].replace("_", " ").casefold()

                if "A" in flags1:
                    american = version1
                if "A" in flags2:
                    american = version2
                if "A" in flags3:
                    american = version3
                if "B" in flags1:
                    brittish = version1
                if "B" in flags2:
                    brittish = version2
                if "B" in flags3:
                    brittish = version3
                brittish_ize = ""
                if "Z" in flags1:
                    brittish_ize = version1
                if "Z" in flags2:
                    brittish_ize = version2
                if "Z" in flags3:
                    brittish_ize = version3
                
                if brittish != american:
                    resulting_dict[brittish] = "B"
                    if brittish_ize != american:
                        resulting_dict[american] = "A"
            except Exception as e:
                logging.debug(f"Found error {e} for line:\n\t{line}")
        elif line.count("/") == 0:
            logging.debug("Passing line with no slashes.")
            continue
        elif line.count("/") == 3:
            try:
                results = p2.parse(line)
                flags1 = process_flags(results["flags1"])
                flags2 = process_flags(results["flags2"])
                flags3 = process_flags(results["flags3"])
                flags4 = process_flags(results["flags4"])
                version1 = results["version1"].replace("_", " ").casefold()
                version2 = results["version2"].replace("_", " ").casefold()
                version3 = results["version3"].replace("_", " ").casefold()
                version4 = results["version4"].replace("_", " ").casefold()

                if "A" in flags1:
                    american = version1
                if "A" in flags2:
                    american = version2
                if "A" in flags3:
                    american = version3
                if "A" in flags4:
                    american = version4
                if "B" in flags1:
                    brittish = version1
                if "B" in flags2:
                    brittish = version2
                if "B" in flags3:
                    brittish = version3
                if "B" in flags4:
                    brittish = version4
                brittish_ize = ""
                if "Z" in flags1:
                    brittish_ize = version1
                if "Z" in flags2:
                    brittish_ize = version2
                if "Z" in flags3:
                    brittish_ize = version3
                if "Z" in flags4:
                    brittish_ize = version4
                
                if brittish != american:
                    resulting_dict[brittish] = "B"
                    if brittish_ize != american:
                        resulting_dict[american] = "A"
        else:
            logging.warning(f"Weird formatting with >3 slashes:\n\t{line}")
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