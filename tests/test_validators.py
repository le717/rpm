# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(".."))

import testhelpers
from src.validator import validator
from src.utils import jsonutils


class TestValidatorMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testhelpers.setUpClass()

    @classmethod
    def tearDownClass(cls):
        testhelpers.tearDownClass()

    def test_valid_name(self):
        r = validator.validate_name("rock-racers")
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "rock-racers")
        self.assertIsNone(r["message"])

    def test_valid_name_length(self):
        r = validator.validate_name("a" * validator.PACKAGE_NAME_MAX_LENGTH)
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "a" * validator.PACKAGE_NAME_MAX_LENGTH)
        self.assertIsNone(r["message"])

    def test_invalid_name_leading_dot(self):
        r = validator.validate_name(".rock-racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], ".rock-racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_leading_us(self):
        r = validator.validate_name("_rock-racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "_rock-racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_spaces(self):
        r = validator.validate_name("rock racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "rock racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_length(self):
        r = validator.validate_name("a" * (
            validator.PACKAGE_NAME_MAX_LENGTH + 1))
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "a" * (
            validator.PACKAGE_NAME_MAX_LENGTH + 1))
        self.assertIn("cannot", r["message"])

    def test_invalid_name_uppercase(self):
        r = validator.validate_name("Rock-Racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "Rock-Racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_name_not_allowed(self):
        r = validator.validate_name("aux")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "aux")
        self.assertIn("not allowed", r["message"])

    def test_invalid_name_char_not_allowed(self):
        r = validator.validate_name(":")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], ":")
        self.assertIn("not allowed", r["message"])

    def test_valid_version(self):
        r = validator.validate_version("1.0.0")
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "1.0.0")
        self.assertIsNone(r["message"])

    def test_valid_version_double_digit(self):
        r = validator.validate_version("1.10.0")
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "1.10.0")
        self.assertIsNone(r["message"])

    def test_invalid_version_leading_v(self):
        r = validator.validate_version("v1.0.0")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "v1.0.0")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_missing_dot(self):
        r = validator.validate_version("1.00")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.00")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_too_short(self):
        r = validator.validate_version("1.0")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.0")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_too_long(self):
        r = validator.validate_version("1.9.0.2")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.9.0.2")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_has_letter(self):
        r = validator.validate_version("1.9.0d")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.9.0d")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_not_valid_format(self):
        r = validator.validate_version("MyVersion")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "MyVersion")
        self.assertIn("Invalid", r["message"])

    def test_package_contains_package_json(self):
        packageZip = os.path.join(testhelpers.TEST_FILES_ROOT_PATH,
                                  "rock-racers",
                                  "rock-racers-valid.zip")

        packageFiles = testhelpers.list_archive_files(packageZip)
        self.assertTrue(validator.has_package_json(packageFiles))

    def test_package_lacks_package_json(self):
        packageZip = os.path.join(testhelpers.TEST_FILES_ROOT_PATH,
                                  "rock-racers",
                                  "rock-racers-missing-json.zip")

        packageFiles = testhelpers.list_archive_files(packageZip)
        self.assertFalse(validator.has_package_json(packageFiles))

    def test_package_is_not_missing_keys(self):
        testhelpers.extract_archive(os.path.join(
            testhelpers.TEST_FILES_ROOT_PATH,
            "rock-racers", "rock-racers-valid.zip"),
            os.path.join(testhelpers.TEST_FILES_TEMP_PATH,
                         "rock-racers-valid"), "package.json")

        packageJson = jsonutils.read(os.path.join(
            testhelpers.TEST_FILES_TEMP_PATH,
            "rock-racers-valid", "package.json"))
        self.assertFalse(validator.is_missing_keys(packageJson))

    def test_package_is_missing_keys(self):
        testhelpers.extract_archive(os.path.join(
            testhelpers.TEST_FILES_ROOT_PATH,
            "rock-racers", "rock-racers-missing-keys.zip"),
            os.path.join(testhelpers.TEST_FILES_TEMP_PATH,
                         "rock-racers-missing-keys"), "package.json")

        packageJson = jsonutils.read(os.path.join(
            testhelpers.TEST_FILES_TEMP_PATH,
            "rock-racers-missing-keys",  "package.json"))
        result = validator.is_missing_keys(packageJson)
        expected = [
            {
                'message': 'missing key "version"',
                'result': 'error',
                'value': 'version'
            },
            {
                'message': 'missing key "homepage"',
                'result': 'warning',
                'value': 'homepage'
            }
        ]
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
