"""Greek text manipulation functions"""
import re


def grup(txtval: str) -> str:
    """Trasforms a string to uppercase special for Greek comparison

    :param txtval:
    :return:
    """
    ar1 = "ΆΈΉΐΊΌΰΎΏ"
    ar2 = "ΑΕΗΪΙΟΫΥΩ"
    ftxt = list(str(txtval).upper())
    for i, letter in enumerate(ftxt):
        if letter in ar1:
            ftxt[i] = ar2[ar1.index(letter)]
    return "".join(ftxt)


def split_strip(text_line: str, separator="|") -> list:
    """Split and strip a txt

    :param text_line:
    :param separator:
    :return:
    """
    return [j.strip() for j in text_line.strip().split(separator)]


def split_text_number(val: str) -> tuple:
    """Split val to (text, number) tuple

    Args:
        val (str): The value to split

    Returns:
        tuple: (text, number) or (text,)
    """
    match = re.match(r"([A-ZΑ-Ω]+)\s*([0-9]+)", val, re.I)
    items = (val,)
    if match:
        items = tuple(match.groups())
    return items
