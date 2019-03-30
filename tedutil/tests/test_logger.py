from unittest import TestCase
from tedutil import logger


class TestLogger(TestCase):
    def test_logger1(self):
        logger.logger.info('testing')
