import re


def split_diff_into_files(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


KNOWN_FILES = {"py"}


def recognize_lang(diff):
    match = re.search(r"^\+\+\+ .*\.(?P<ext>.*)$", diff, re.MULTILINE)
    if match:
        ext = match.group("ext")
        if ext in KNOWN_FILES:
            return ext
    return None
