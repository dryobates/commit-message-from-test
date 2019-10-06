import re

SHELL_TEST_RE = re.compile(
    r"""
    ^\+\s*(?:
        test(.*)\(                  # function defined with "()": test_some_name() {
        | function\s*test(.*)\b   # function defined with "function": function test_some_name {
    )
""",
    re.MULTILINE | re.VERBOSE,
)


def extract_messages_from_shell_file_diff(diff):
    matches = SHELL_TEST_RE.findall(diff)
    return (
        parens_function or keyword_function
        for parens_function, keyword_function in matches
    )
