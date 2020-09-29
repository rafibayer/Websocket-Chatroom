import unittest
import os
import sys
#import test_helper
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../server')))
from response import Response, Origin
from utils import log, log_message


class TestResponse(unittest.TestCase):

    def test_create_response(self):
        resp = Response("data")
        self.assertEqual(resp.data["body"], "data")
        self.assertEqual(resp.data["origin"], Origin.DEFAULT.value)

    def test_create_response_origin(self):
        resp = Response("data", Origin.SERVER)
        self.assertEqual(resp.data["body"], "data")
        self.assertEqual(resp.data["origin"], Origin.SERVER.value)


if __name__ == "__main__":
    unittest.main()
