from cmft.split_diff_into_files import split_diff_into_files, recognize_lang


def test_returns_empty_iterable_when_no_file_boundary_found():
    diff = "+ no file boundary"

    file_diffs = list(split_diff_into_files(diff))

    assert file_diffs == []


def test_returns_empty_iterable_when_no_empty_diff():
    diff = ""

    file_diffs = list(split_diff_into_files(diff))

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

    file_diffs = list(split_diff_into_files(diff))

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

    file_diffs = list(split_diff_into_files(diff))

    assert len(file_diffs) == 2


# recognizes language from diff


def test_returns_none_when_unknown_file_type():
    diff = """\
--git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test"""

    lang = recognize_lang(diff)

    assert lang is None
