import pytest

from cmft.extract_message import extract_messages_from_python_file_diff


def test_returns_message_based_on_test_name_when_one_test_found():
    message = """\
+def testname():
    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["name"] == list(result)


def test_returns_all_possible_messages_based_on_tests_names():
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
def test_contains_test_definition_words_in_name(word):
    message = f"""\
+def test{word}():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert [word] == list(result)


@pytest.mark.parametrize(
    "test_name", ["snake_case", "snake__case", "_snake_case", "snake_case_"]
)
def test_changes_underlines_to_spaces_in_message(test_name):
    message = f"""\
+def test{test_name}():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["snake case"] == list(result)


@pytest.mark.parametrize("test_name", ["CamelCase", "camelCase"])
def test_changes_camel_case_to_words(test_name):
    message = f"""\
+def test{test_name}():
+    pass"""

    result = extract_messages_from_python_file_diff(message)

    assert ["camel case"] == list(result)
