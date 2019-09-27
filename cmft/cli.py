import re
from subprocess import CalledProcessError, run

import click

from cmft.extract_message import extract_messages_from_python_file_diff


@click.command()
def main():
    diff = _get_diff_output()
    messages = _extract_messages_from_diff(diff)
    click.echo("\n".join(messages), nl=False)


def _get_diff_output():
    try:
        return run(
            "git diff HEAD",
            shell=True,
            check=True,
            capture_output=True,
            encoding="utf8",
        ).stdout
    except CalledProcessError:
        return ""


def _extract_messages_from_diff(diff):
    files_diffs = split_diff_into_separate_file_diffs(diff)
    for file_diff in files_diffs:
        for message in extract_messages_from_file_diff(file_diff):
            yield message


def split_diff_into_separate_file_diffs(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]


def extract_messages_from_file_diff(diff):
    extract = get_extract_method_for_file_diff(diff)
    return extract(diff)


LANG_EXT = re.compile(r"^\+\+\+ .*\.(?P<ext>.*)$", re.MULTILINE)
KNOWN_FILES = {"py": extract_messages_from_python_file_diff}


def get_extract_method_for_file_diff(diff):
    match = LANG_EXT.search(diff)
    ext = match.group("ext") if match else None
    return KNOWN_FILES.get(ext, null_function)


def null_function(*args, **kwargs):
    return []


if __name__ == "__main__":
    main()
