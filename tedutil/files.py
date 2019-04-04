"""File functions"""


import hashlib
import os
import zipfile
import urllib.request as ur
BUF_SIZE = 65536


def fsha1(filepath):
    """Check sha1 of the file

    :param filepath: file path
    :return: sha1 string
    """
    sha1 = hashlib.sha1()
    with open(filepath, 'rb') as fil:
        while True:
            data = fil.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def download_file(url, directory=None):
    """Download file url from internet

    :param url:
    :param directory:
    :return:
    """
    if not directory:
        directory = os.path.dirname(__file__)
    filename = url.split('/')[-1]
    *front, last = filename.split('.')
    oldfront = '.'.join(front) + '.' + 'old'
    oldfilename = '.'.join([oldfront, last])
    olddirfile = os.path.join(directory, oldfilename)
    dirfile = os.path.join(directory, filename)
    if os.path.exists(dirfile):
        os.rename(dirfile, olddirfile)
        print(fsha1(olddirfile))
    ur.urlretrieve(url, dirfile)
    print(fsha1(dirfile))
    return dirfile


def zipfile_data(zipfilename, filename, encod='CP1253'):
    """

    :param zipfilename: zip file name
    :param filename: file name inside zip file
    :param encod: encoding
    :return: text lines
    """
    with zipfile.ZipFile(zipfilename) as zfile:
        with zfile.open(filename) as fname:
            fdata = fname.read().decode(encod)
    return fdata.split('\n')

