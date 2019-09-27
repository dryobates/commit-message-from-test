import re

TEST_RE = re.compile(r"^\+\s*def test(.*)\(", re.MULTILINE)
UNDERLINES_RE = re.compile("_+")
FIRST_CAP_RE = re.compile(r"(.)([A-Z][a-z]+)")
ALL_CAP_RE = re.compile("([a-z0-9])([A-Z])")


def extract_message_from_python_file_diff(diff):
    matches = TEST_RE.findall(diff)
    return [snake_to_words(camel_to_snake(match)) for match in matches]


def camel_to_snake(message):
    message = FIRST_CAP_RE.sub(r"\1_\2", message)
    return ALL_CAP_RE.sub(r"\1_\2", message).lower()


def snake_to_words(message):
    return UNDERLINES_RE.sub(" ", message).strip()
