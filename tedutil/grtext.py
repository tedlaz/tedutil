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
