import sys
from setuptools import setup


if sys.hexversion < 0x3040000:
    msg = "Python version %s is unsupported, >= 3.4.0 is needed"
    print(msg % (".".join(map(str, sys.version_info[:3]))))
    exit(1)


setup(name='tedutil',
      version='0.8.4',
      description='Various utility functions',
      long_description='Various utility functions',
      url='https://github.com/tedlaz/tedutil',
      keywords=["util", "Greek"],
      author='Ted Lazaros',
      author_email='tedlaz@gmail.com',
      license='GPLv3',
      packages=['tedutil'],
      classifiers=["Development Status :: 4 - Beta",
                   "Environment :: Console",
                   "Intended Audience :: Developers",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3 :: Only",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Topic :: Software Development :: Build Tools"]
      )
