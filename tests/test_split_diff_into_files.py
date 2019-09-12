# returns iterator over file diffs with two items
# recognizes language from diff
# ignores file diff when not supported language

from cmft.split_diff_into_files import split_diff_into_files


def test_returns_empty_iterator_when_no_file_boundary_found():
    diff = "+ no file boundary"

    file_diffs = list(split_diff_into_files(diff))

    assert file_diffs == []


def test_returns_empty_iterator_when_no_empty_diff():
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

    assert len(file_diffs)
    assert file_diffs[0] == diff.replace("diff ", "")
