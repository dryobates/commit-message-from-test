import re

from cmft.extract_message import extract_message

LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)
KNOWN_FILES = {"py": extract_message}


def extract_messages_from_diff(diff):
    files_diffs = split_diff_into_separate_file_diffs(diff)
    messages = (extract_message_from_file_diff(file_diff) for file_diff in files_diffs)
    return [message for message in messages if message]


def split_diff_into_separate_file_diffs(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def extract_message_from_file_diff(diff):
    extract = get_extract_method_for_file_diff(diff)
    return extract(diff, "")


def get_extract_method_for_file_diff(diff):
    match = LANG_EXT.search(diff)
    ext = match.group("ext") if match else None
    return KNOWN_FILES.get(ext, null_function)


def null_function(*args, **kwargs):
    return None
