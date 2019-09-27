import re

from cmft.utils import snake_to_words, camel_to_snake


KNOWN_FILES = {}


def extract_messages_from_diff(diff):
    files_diffs = _split_diff_into_separate_file_diffs(diff)
    for file_diff in files_diffs:
        for message in _extract_messages_from_file_diff(file_diff):
            yield message


def _split_diff_into_separate_file_diffs(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def _extract_messages_from_file_diff(diff):
    extract = _get_extract_method_for_file_diff(diff)
    return extract(diff)


LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)


def _get_extract_method_for_file_diff(diff):
    match = LANG_EXT.search(diff)
    ext = match.group("ext") if match else None
    return KNOWN_FILES.get(ext, _null_function)


def _null_function(*args, **kwargs):
    return []


PYTHON_TEST_RE = re.compile(r"^\+\s*def test(.*)\(", re.MULTILINE)


def extract_messages_from_python_file_diff(diff):
    matches = PYTHON_TEST_RE.findall(diff)
    return (snake_to_words(camel_to_snake(match)) for match in matches)


KNOWN_FILES["py"] = extract_messages_from_python_file_diff
