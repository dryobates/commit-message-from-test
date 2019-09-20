import re

LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)
KNOWN_FILES = {"py"}


def split_diff_into_files(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def recognize_lang(diff):
    match = LANG_EXT.search(diff)
    if match:
        ext = match.group("ext")
        if ext in KNOWN_FILES:
            return ext
    return None
