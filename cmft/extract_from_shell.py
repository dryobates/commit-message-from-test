import re

SHELL_TEST_RE = re.compile(r"^\+\s*test(.*)\(", re.MULTILINE)


def extract_messages_from_shell_file_diff(diff):
    matches = SHELL_TEST_RE.findall(diff)
    return (match for match in matches)
