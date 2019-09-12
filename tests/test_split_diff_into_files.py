# returns iterator over file diffs
# recognizes language from diff
# ignores file diff when not supported language
# returns empty iterator when empty diff


def test_returns_empty_iterator_when_no_file_boundary_found():
    diff = "+ no file boundary"

    file_diffs = list(split_diff_into_files(diff))

    assert file_diffs == []
