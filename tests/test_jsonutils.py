# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(".."))

import testhelpers
from src.utils import jsonutils


class TestJsonUtilsMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testhelpers.setUpClass()

    @classmethod
    def tearDownClass(cls):
        testhelpers.tearDownClass()

    def test_read_valid_json(self):
        testhelpers.extract_archive(os.path.join(
            testhelpers.TEST_FILES_ROOT_PATH,
            "rock-racers", "rock-racers-valid.zip"),
            os.path.join(testhelpers.TEST_FILES_TEMP_PATH,
                         "rock-racers-valid"), "package.json")

        packageJson = jsonutils.read(os.path.join(
            testhelpers.TEST_FILES_TEMP_PATH,
            "rock-racers-valid", "package.json"))
        self.assertIsNotNone(packageJson)
        assert type(packageJson) == dict

    def test_read_invalid_json(self):
        testhelpers.extract_archive(os.path.join(
            testhelpers.TEST_FILES_ROOT_PATH,
            "rock-racers", "rock-racers-invalid-json.zip"),
            os.path.join(testhelpers.TEST_FILES_TEMP_PATH,
                         "rock-racers-invalid-json"), "package.json")

        packageJson = jsonutils.read(os.path.join(
            testhelpers.TEST_FILES_TEMP_PATH,
            "rock-racers-invalid-json", "package.json"))
        self.assertIsNone(packageJson)

    def test_read_nonexistent_json(self):
        self.assertIsNone(jsonutils.read("package.json"))


if __name__ == "__main__":
    unittest.main()
