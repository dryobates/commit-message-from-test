from cmft.extract_from_shell import extract_messages_from_shell_file_diff


def test_returns_message_based_on_test_name():
    message = """\
+testname() {
+    assertTrue 1
+}"""

    result = extract_messages_from_shell_file_diff(message)

    assert ["name"] == list(result)

# def test_returns_message_based_on_test_name_declared_with_function_keyword():
# def test_returns_all_possible_messages():
# def test_does_not_output_commented_tests():
# def test_returns_message_for_tests_that_contain_test_definition_words_in_name():
# def test_returns_message_with_underlines_changed_to_spaces():
# def test_returns_message_with_camel_case_converted_to_words():
