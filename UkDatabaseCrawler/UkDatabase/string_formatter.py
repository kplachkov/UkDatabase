"""In case you see strange symbols in the crawled information!
When opened with MS Excel or other editors, some of the unicode
characters are displayed wrong. It could be fixed directly with the editor,
otherwise use these functions to replace the problematic characters
with close representation in ASCII."""


def format_string(string: str) -> str:
    """Replace specific unicode characters with ASCII ones.
    Args:
        string: Unicode string.
    Returns:
        ASCII string.
    """
    string \
        .replace("\u2013", "-") \
        .replace("\u00a0", " ") \
        .replace("\u2018", "'") \
        .replace("\u2019", "'") \
        .replace("\u201c", '"') \
        .replace("\u201d", '"') \
        .replace("\u00ed", 'i')
    return string


def format_list(list_of_strings: list) -> list:
    """Replace specific unicode characters with ASCII ones.
    Args:
        list_of_strings: List of unicode strings.
    Returns:
        List of ASCII strings.
    """
    return [format_string(string) for string in list_of_strings]
