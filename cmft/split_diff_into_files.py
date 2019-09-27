import re

from cmft.extract_message import extract_message_from_python_file_diff

LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)
KNOWN_FILES = {"py": extract_message_from_python_file_diff}


def extract_messages_from_diff(diff):
    files_diffs = split_diff_into_separate_file_diffs(diff)
    messages = []
    for file_diff in files_diffs:
        messages.extend(extract_message_from_file_diff(file_diff))
    return messages


def split_diff_into_separate_file_diffs(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def extract_message_from_file_diff(diff):
    extract = get_extract_method_for_file_diff(diff)
    return extract(diff)


def get_extract_method_for_file_diff(diff):
    match = LANG_EXT.search(diff)
    ext = match.group("ext") if match else None
    return KNOWN_FILES.get(ext, null_function)


def null_function(*args, **kwargs):
    return []
