def split_diff_into_files(diff):
    chunks = ("\n" + diff).split("\ndiff ")
    return chunks[1:]
