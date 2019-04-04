"""Logger module"""

""" Logger levels
CRITICAL	50
ERROR	    40
WARNING	30
INFO	    20
DEBUG	    10
"""
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = '%(asctime)s|%(filename)s:%(lineno)d(%(levelname)s)> %(message)s'
formatter = logging.Formatter(fmt)
file_handler = logging.FileHandler('minoracc.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

stream_handler=logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.ERROR)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
