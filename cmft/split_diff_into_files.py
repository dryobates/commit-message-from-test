import re


def split_diff_into_files(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def recognize_lang(diff):
    match = re.search(r"^\+\+\+ .*\.(?P<ext>.*)$", diff, re.MULTILINE)
    if match:
        if match.group("ext") == "py":
            return "py"
    return None
