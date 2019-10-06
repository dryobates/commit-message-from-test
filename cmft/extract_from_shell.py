import re

SHELL_TEST_RE = re.compile(r"^\+\s*(?:test(.*)\(|function\s*test([^\s]*))", re.MULTILINE)


def extract_messages_from_shell_file_diff(diff):
    matches = SHELL_TEST_RE.findall(diff)
    return (m1 or m2 for m1, m2 in matches)
