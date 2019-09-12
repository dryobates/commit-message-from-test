def split_diff_into_files(diff):
    chunks = ("\n" + diff).split("\ndiff")
    if len(chunks) > 1:
        return chunks
    return []
