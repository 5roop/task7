from parse import compile
import logging
import pandas as pd
from typing import Set, List, Dict
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


def process_flags(flags: str) -> Set[str]:
    """Processes string of varcon flags.
    We are only interested in ABZ flags with no qualifiers.
    Examples:
        'A Bv Zv' -> {'A'}
        'Av B Z_' -> {'B'}
        'A B Cv' -> {'A', 'B'}

    Args:
        flags (str): flags as they appear in varcon lexicon.

    Returns:
        set: set of strings "A", "B", "Z".
    """
    flags = flags.split(" ")
    flags = [flag for flag in flags if flag in ["A", "B", "Z"]]
    return set(flags)


def preprocess(s: str) -> str:
    """Removes unusual characters and lowercases the string.

    Args:
        s (str): input string.

    Returns:
        str: output string.
    """
    for c in chars_to_remove:
        s = s.replace(c, "")
    s = s.casefold()
    return s


def count_variants(s: str, lex: dict):
    """Counts the variants in the input string based on the lexicon lex.

    Returns tuple (counts, per_token_breakdown).
    Counts look like this:
        {"A":3, "B":0}.
    per_token is a dictionary with all the words detected, their counts and their variant:
        {"word1":
            {"count":3, "variant":"A"}
        }

    Args:
        s (str): Input string.
        lex (dict): Lexicon.

    Returns:
        results (tuple): (counts, per_token).
    """
    counts = dict()
    per_token = dict()
    for word in preprocess(s).split():
        variant = lex.get(word, None)
        if not variant:
            continue
        logging.info(f"Found word {word}, presumed variant: {variant}.")
        counts[variant] = counts.get(variant, 0) + 1
        if word in per_token.keys():
            per_token[word]["count"] += 1
        else:
            per_token[word] = {"variant": variant, "count": 1}
    return counts, per_token


def process_item(item: str) -> Dict:
    """Processes a unit of varcon lexicon and returns the results in dictionary form.

    Args:
        item (str): Multiline string from varcon lexicon.

    Returns:
        Dict: dictionary like {'word1': "B", "word2": "A"}
    """
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
            except Exception as e:
                logging.debug(f"Found error {e} for line:\n\t{line}")
        else:
            logging.warning(f"Weird formatting with >3 slashes:\n\t{line}")
    return resulting_dict


def get_lexicon(min_length: int = 1, only_verified: bool = False) -> dict:
    """Generates lexicon from varcon file.

    Args:
        min_length (int, optional): Only return words longer than min_length. Defaults to 1.
        only_verified (bool, optional): Only include words with <verified> flag. Defaults to False.

    Returns:
        dict: results like {"word1": "A", "word2": "B",...}
    """
    f = "varcon.txt"
    with open(f, "r") as file:
        content = file.read()
    items = content.split("# ")[1:]
    results = {}
    for item in items:
        if only_verified:
            if "<verified>" not in item:
                continue
        results.update(process_item(item))
    results = {key: value for key, value in results.items() if len(key)
               >= min_length}
    return results
