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


def split_strip(txt, separator='|'):
    """Split and strip a txt

    :param txtline:
    :param separator:
    :return:
    """
    return [j.strip() for j in txt.strip().split(separator)]
