from cmft.extract_message import extract_messages_from_diff


def test_returns_no_messages_when_not_correct_diff():
    diff = "+ no file boundary"

    messages = extract_messages_from_diff(diff)

    assert [] == list(messages)


def test_returns_no_messages_when_empty_diff():
    diff = ""

    messages = extract_messages_from_diff(diff)

    assert [] == list(messages)


def test_returns_no_messages_when_no_known_file_types():
    diff = """\
diff --git a/file.txt b/file.txt
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+# test"""

    messages = extract_messages_from_diff(diff)

    assert [] == list(messages)


def test_returns_message_for_known_file_type():
    diff = """\
diff --git a/file.py b/file.py
new file mode 100644
index 0000000..0d6170b
--- /dev/null
+++ b/file.py
@@ -0,0 +1 @@
+def test_abc():
    pass"""

    messages = extract_messages_from_diff(diff)

    assert ["abc"] == list(messages)


def test_returns_messages_for_all_known_file_types_from_diff():
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

    assert ["def", "abc"] == list(messages)
