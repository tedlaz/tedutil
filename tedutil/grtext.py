"""Greek text manipulation functions"""


def grup(txtval):
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
    return ''.join(ftxt)


def split_strip(text_line, separator='|'):
    """Split and strip a txt

    :param text_line:
    :param separator:
    :return:
    """
    return [j.strip() for j in text_line.strip().split(separator)]
