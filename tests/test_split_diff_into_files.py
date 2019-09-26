from cmft.extract_message import extract_message_from_python_file_diff
from cmft.split_diff_into_files import (
    extract_message_from_file_diff,
    extract_messages_from_diff,
    get_extract_method_for_file_diff,
    null_function,
    split_diff_into_separate_file_diffs,
)


def test_returns_empty_iterable_when_no_file_boundary_found():
    diff = "+ no file boundary"

    file_diffs = list(split_diff_into_separate_file_diffs(diff))

    assert file_diffs == []


def test_returns_empty_iterable_when_no_empty_diff():
    diff = ""

    file_diffs = list(split_diff_into_separate_file_diffs(diff))

    assert file_diffs == []


def test_returns_iterable_with_one_element_when_diff_with_one_file():
    diff = """\
diff --git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test"""

    file_diffs = list(split_diff_into_separate_file_diffs(diff))

    assert len(file_diffs) == 1
    assert file_diffs[0] == diff.replace("diff ", "")


def test_returns_iterable_with_two_elements_when_diff_with_two_files():
    diff = """\
diff --git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test
diff --git a/other.txt b/other.txt
new file mode 100644
index 0000000..0d6170b
--- a/other.txt
+++ b/other.txt
@@ -0,0 +1 @@
+# test"""

    file_diffs = list(split_diff_into_separate_file_diffs(diff))

    assert len(file_diffs) == 2


def test_returns_null_function_when_unknown_file_type():
    diff = """\
--git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test"""

    method = get_extract_method_for_file_diff(diff)

    assert method is null_function


def test_returns_extract_method_for_known_file_type():
    diff = """\
--git a/file.py b/file.py
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.py
@@ -0,0 +1 @@
+# test"""

    method = get_extract_method_for_file_diff(diff)

    assert method is extract_message_from_python_file_diff


def test_returns_none_when_unknown_language():
    diff = """\
--git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test"""

    message = extract_message_from_file_diff(diff)

    assert message is None


def test_returns_message_when_known_language():
    diff = """\
--git a/file.py b/file.py
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.py
@@ -0,0 +1 @@
+def test_abc():
    pass"""

    message = extract_message_from_file_diff(diff)

    assert message == "abc"


def test_returns_messages_for_known_files_from_diff():
    diff = """\
diff --git a/file.py b/file.py
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.py
@@ -0,0 +1 @@
+def test_def():
    pass
diff --git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test
diff --git a/file.py b/file.py
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.py
@@ -0,0 +1 @@
+def test_abc():
    pass"""

    messages = extract_messages_from_diff(diff)

    assert messages == ["def", "abc"]
