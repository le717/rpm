# -*- coding: utf-8 -*-
import os
import sys
import unittest
from zipfile import ZipFile

sys.path.insert(0, os.path.abspath(".."))

from src.validator import validator
from src.utils import jsonutils


class TestValidatorMethods(unittest.TestCase):

    TEST_FILES_ROOT_PATH = os.path.join(os.getcwd(), "files")
    TEST_FILES_TEMP_PATH = os.path.join(TEST_FILES_ROOT_PATH, "temp")

    @classmethod
    def delete_temp_files(self):
        """Taken from Python docs.
        https://docs.python.org/3/library/os.html#os.walk
        """
        for root, dirs, files in os.walk(self.TEST_FILES_TEMP_PATH,
                                         topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def list_archive_files(self, zip):
        with ZipFile(zip, "r") as z:
            return z.namelist()

    def extract_archive(self, zip, path, file="all"):
        packageFiles = self.list_archive_files(zip)
        with ZipFile(zip, "r") as z:
            if file == "all":
                z.extractall(path, packageFiles)
                return True
            else:
                if file not in packageFiles:
                    return False
                else:
                    z.extract(file, path)
                    return True

    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(cls.TEST_FILES_TEMP_PATH):
            os.makedirs(cls.TEST_FILES_TEMP_PATH)
        else:
            cls.delete_temp_files()

    @classmethod
    def tearDownClass(cls):
        cls.delete_temp_files()

    def test_valid_name(self):
        r = validator.validateName("rock-racers")
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "rock-racers")
        self.assertIsNone(r["message"])

    def test_valid_name_length(self):
        r = validator.validateName("a" * validator.PACKAGE_NAME_MAX_LENGTH)
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "a" * validator.PACKAGE_NAME_MAX_LENGTH)
        self.assertIsNone(r["message"])

    def test_invalid_name_leading_dot(self):
        r = validator.validateName(".rock-racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], ".rock-racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_leading_us(self):
        r = validator.validateName("_rock-racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "_rock-racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_spaces(self):
        r = validator.validateName("rock racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "rock racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_length(self):
        r = validator.validateName("a" * (
            validator.PACKAGE_NAME_MAX_LENGTH + 1))
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "a" * (
            validator.PACKAGE_NAME_MAX_LENGTH + 1))
        self.assertIn("cannot", r["message"])

    def test_invalid_name_uppercase(self):
        r = validator.validateName("Rock-Racers")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "Rock-Racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_name_not_allowed(self):
        r = validator.validateName("aux")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "aux")
        self.assertIn("not allowed", r["message"])

    def test_invalid_name_char_not_allowed(self):
        r = validator.validateName(":")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], ":")
        self.assertIn("not allowed", r["message"])

    def test_valid_version(self):
        r = validator.validateVersion("1.0.0")
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "1.0.0")
        self.assertIsNone(r["message"])

    def test_valid_version_double_digit(self):
        r = validator.validateVersion("1.10.0")
        self.assertIsNone(r["result"])
        self.assertEqual(r["value"], "1.10.0")
        self.assertIsNone(r["message"])

    def test_invalid_version_leading_v(self):
        r = validator.validateVersion("v1.0.0")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "v1.0.0")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_missing_dot(self):
        r = validator.validateVersion("1.00")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.00")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_too_short(self):
        r = validator.validateVersion("1.0")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.0")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_too_long(self):
        r = validator.validateVersion("1.9.0.2")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.9.0.2")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_has_letter(self):
        r = validator.validateVersion("1.9.0d")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "1.9.0d")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_not_valid_format(self):
        r = validator.validateVersion("MyVersion")
        self.assertEqual(r["result"], "error")
        self.assertEqual(r["value"], "MyVersion")
        self.assertIn("Invalid", r["message"])

    def test_package_contains_package_json(self):
        packageZip = os.path.join(self.TEST_FILES_ROOT_PATH,
                                  "rock-racers",
                                  "rock-racers-valid.zip")

        packageFiles = self.list_archive_files(packageZip)
        self.assertTrue(validator.hasPackageJson(packageFiles))

    def test_package_lacks_package_json(self):
        packageZip = os.path.join(self.TEST_FILES_ROOT_PATH,
                                  "rock-racers",
                                  "rock-racers-missing-json.zip")

        packageFiles = self.list_archive_files(packageZip)
        self.assertFalse(validator.hasPackageJson(packageFiles))

    def test_package_is_not_missing_keys(self):
        self.extract_archive(os.path.join(self.TEST_FILES_ROOT_PATH,
                             "rock-racers", "rock-racers-valid.zip"),
                             os.path.join(self.TEST_FILES_TEMP_PATH,
                                          "rock-racers-valid"),
                             "package.json")

        packageJson = jsonutils.read(os.path.join(self.TEST_FILES_TEMP_PATH,
                                                  "rock-racers-valid",
                                                  "package.json"
                                                  ))
        self.assertFalse(validator.isMissingKeys(packageJson))

    def test_package_is_missing_keys(self):
        self.extract_archive(os.path.join(self.TEST_FILES_ROOT_PATH,
                             "rock-racers", "rock-racers-missing-keys.zip"),
                             os.path.join(self.TEST_FILES_TEMP_PATH,
                                          "rock-racers-missing-keys"),
                             "package.json")

        packageJson = jsonutils.read(os.path.join(self.TEST_FILES_TEMP_PATH,
                                                  "rock-racers-missing-keys",
                                                  "package.json"
                                                  ))
        result = validator.isMissingKeys(packageJson)
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
