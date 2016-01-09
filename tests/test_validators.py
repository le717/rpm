# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(".."))

from src.validator import validator


class TestValidatorMethods(unittest.TestCase):

    def test_valid_name(self):
        r = validator.validateName("rock-racers")
        self.assertTrue(r["result"])
        self.assertEqual(r["value"], "rock-racers")
        self.assertIsNone(r["message"])

    def test_valid_name_length(self):
        r = validator.validateName("a" * validator.PACKAGE_NAME_MAX_LENGTH)
        self.assertTrue(r["result"])
        self.assertEqual(r["value"], "a" * validator.PACKAGE_NAME_MAX_LENGTH)
        self.assertIsNone(r["message"])

    def test_invalid_name_leading_dot(self):
        r = validator.validateName(".rock-racers")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], ".rock-racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_leading_us(self):
        r = validator.validateName("_rock-racers")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "_rock-racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_spaces(self):
        r = validator.validateName("rock racers")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "rock racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_length(self):
        r = validator.validateName("a" * (
            validator.PACKAGE_NAME_MAX_LENGTH + 1))
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "a" * (
            validator.PACKAGE_NAME_MAX_LENGTH + 1))
        self.assertIn("cannot", r["message"])

    def test_invalid_name_uppercase(self):
        r = validator.validateName("Rock-Racers")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "Rock-Racers")
        self.assertIn("cannot", r["message"])

    def test_invalid_name_name_not_allowed(self):
        r = validator.validateName("aux")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "aux")
        self.assertIn("not allowed", r["message"])

    def test_invalid_name_char_not_allowed(self):
        r = validator.validateName(":")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], ":")
        self.assertIn("not allowed", r["message"])

    def test_valid_version(self):
        r = validator.validateVersion("1.0.0")
        self.assertTrue(r["result"])
        self.assertEqual(r["value"], "1.0.0")
        self.assertIsNone(r["message"])

    def test_valid_version_double_digit(self):
        r = validator.validateVersion("1.10.0")
        self.assertTrue(r["result"])
        self.assertEqual(r["value"], "1.10.0")
        self.assertIsNone(r["message"])

    def test_invalid_version_leading_v(self):
        r = validator.validateVersion("v1.0.0")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "v1.0.0")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_missing_dot(self):
        r = validator.validateVersion("1.00")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "1.00")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_too_short(self):
        r = validator.validateVersion("1.0")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "1.0")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_too_long(self):
        r = validator.validateVersion("1.9.0.2")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "1.9.0.2")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_has_letter(self):
        r = validator.validateVersion("1.9.0d")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "1.9.0d")
        self.assertIn("Invalid", r["message"])

    def test_invalid_version_not_valid_format(self):
        r = validator.validateVersion("MyVersion")
        self.assertFalse(r["result"])
        self.assertEqual(r["value"], "MyVersion")
        self.assertIn("Invalid", r["message"])


if __name__ == "__main__":
    unittest.main()
