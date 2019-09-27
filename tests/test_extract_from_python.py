import pytest

from cmft.extract_from_python import extract_messages_from_python_file_diff


def test_returns_message_based_on_test_name():
    message = """\
+def testname():
    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["name"] == list(result)


def test_returns_all_possible_messages():
    message = """\
+def testfirst():
    +pass
+
+def testsecond():
    +pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["first", "second"] == list(result)


def test_returns_message_from_test_method():
    message = """\
+class TestExample(TestCase):
+    def testname(self):
+        pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["name"] == list(result)


def test_does_not_include_function_arguments_in_message():
    message = """\
+def testname(self, args1):
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["name"] == list(result)


def test_does_not_output_commented_tests():
    message = """\
+# def testfirst():
+#    pass
+
+def testsecond():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["second"] == list(result)


@pytest.mark.parametrize("word", ["def", "test"])
def test_returns_message_for_tests_that_contain_test_definition_words_in_name(word):
    message = f"""\
+def test{word}():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert [word] == list(result)


def test_returns_message_with_underlines_changed_to_spaces():
    message = f"""\
+def test_snake_case():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["snake case"] == list(result)


def test_returns_message_with_camel_case_converted_to_words():
    message = f"""\
+def testCamelCase():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["camel case"] == list(result)
