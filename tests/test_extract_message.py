import pytest

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


def test_does_not_include_function_arguments_in_message():
    message = """\
+def testname(self, args1):
+    pass"""

    result = extract_message(message, DEFAULT_MESSAGE)

    assert "name" == result


def test_does_not_output_commented_tests():
    message = """\
+# def testfirst():
+#    pass
+
+def testsecond():
+    pass"""

    result = extract_message(message, DEFAULT_MESSAGE)

    assert "second" == result


@pytest.mark.parametrize("word", ["def", "test"])
def test_contains_test_definition_words_in_name(word):
    message = f"""\
+def test{word}():
+    pass"""

    result = extract_message(message, DEFAULT_MESSAGE)

    assert word == result
