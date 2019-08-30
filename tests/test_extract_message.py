from cmft.extract_message import extract_message

DEFAULT_MESSAGE = "some message"


def test_returns_default_message_when_no_tests_found():
    message = extract_message("+#", DEFAULT_MESSAGE)

    assert DEFAULT_MESSAGE == message


def test_returns_message_based_on_test_name_when_one_test_found():
    message = """\
+def testname():
    pass"""

    result = extract_message(message, DEFAULT_MESSAGE)

    assert "name" == result


def test_returns_message_based_on_first_found_test_name_when_many_tests_found():
    message = """\
+def testfirst():
    +pass
+
+def testsecond():
    +pass"""

    result = extract_message(message, DEFAULT_MESSAGE)

    assert "first" == result


def test_returns_message_from_test_method():
    message = """\
+class TestExample(TestCase):
+    def testname(self):
+        pass"""

    result = extract_message(message, DEFAULT_MESSAGE)

    assert "name" == result
