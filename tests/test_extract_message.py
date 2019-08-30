from cmft.extract_message import extract_message

DEFAULT_MESSAGE = "some message"


def test_returns_default_message_when_no_tests_found():
    message = extract_message("#", DEFAULT_MESSAGE)

    assert DEFAULT_MESSAGE == message
