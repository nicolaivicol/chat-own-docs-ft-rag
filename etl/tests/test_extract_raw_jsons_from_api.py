import unittest

from etl.extract_raw_jsons_from_api import get_service


class TestAll(unittest.TestCase):

    def test_get_service(self):
        code_service = '005000102'
        s = get_service(code_service, save_to_disk=True)
        print(s)
