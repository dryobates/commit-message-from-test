import re
from cmft.extract_message import extract_message

LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)
KNOWN_FILES = {"py": extract_message}


def split_diff_into_files(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def extract_message_from_file_diff(diff):
    extract = get_language_extract_method(diff)
    if extract is not None:
        return extract(diff, "")
    else:
        return None


def get_language_extract_method(diff):
    match = LANG_EXT.search(diff)
    if match:
        ext = match.group("ext")
        return KNOWN_FILES.get(ext, None)
    return None
