import sys

from cmft.extract_message import extract_messages_from_diff


def main():
    diff = sys.stdin.read()
    messages = extract_messages_from_diff(diff)
    sys.stdout.write("\n".join(messages))


if __name__ == "__main__":
    main()
