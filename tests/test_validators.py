# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(".."))

from src.validator import validator


class TestValidatorMethods(unittest.TestCase):

    def test_valid_name(self):
        r = validator.validateName("rock-racers")
        assert r["result"] and r["value"] == "rock-racers" and r["message"] is None

    def test_valid_name_length(self):
        r = validator.validateName("a" * 214)
        assert r["result"] and r["value"] == "a" * 214 and r["message"] is None

    def test_invalid_name_leading_dot(self):
        r = validator.validateName(".rock-racers")
        assert not r["result"] and r["value"] == ".rock-racers" and "cannot" in r["message"]

    def test_invalid_name_leading_us(self):
        r = validator.validateName("_rock-racers")
        assert not r["result"] and r["value"] == "_rock-racers" and "cannot" in r["message"]

    def test_invalid_name_spaces(self):
        r = validator.validateName("rock racers")
        assert not r["result"] and r["value"] == "rock racers" and "cannot" in r["message"]

    def test_invalid_name_length(self):
        r = validator.validateName("a" * 215)
        assert not r["result"] and r["value"] == "a" * 215 and "cannot" in r["message"]

    def test_invalid_name_uppercase(self):
        r = validator.validateName("Rock-Racers")
        assert not r["result"] and r["value"] == "Rock-Racers" and "cannot" in r["message"]

    def test_invalid_name_name_not_allowed(self):
        r = validator.validateName("aux")
        assert not r["result"] and r["value"] == "aux" and "not allowed" in r["message"]

    def test_invalid_name_char_not_allowed(self):
        r = validator.validateName(":")
        assert not r["result"] and r["value"] == ":" and "not allowed" in r["message"]

    def test_valid_version(self):
        r = validator.validateVersion("1.0.0")
        assert r["result"] and r["value"] == "1.0.0" and r["message"] is None

    def test_valid_name_double_digit(self):
        r = validator.validateVersion("1.10.0")
        assert r["result"] and r["value"] == "1.10.0" and r["message"] is None

    def test_invalid_version_leading_v(self):
        r = validator.validateVersion("v1.0.0")
        assert not r["result"] and r["value"] == "v1.0.0" and "Invalid" in r["message"]

    def test_invalid_version_missing_dot(self):
        r = validator.validateVersion("1.00")
        assert not r["result"] and r["value"] == "1.00" and "Invalid" in r["message"]

    def test_invalid_version_too_short(self):
        r = validator.validateVersion("1.0")
        assert not r["result"] and r["value"] == "1.0" and "Invalid" in r["message"]

    def test_invalid_version_too_long(self):
        r = validator.validateVersion("1.9.0.2")
        assert not r["result"] and r["value"] == "1.9.0.2" and "Invalid" in r["message"]

    def test_invalid_version_has_letter(self):
        r = validator.validateVersion("1.9.0d")
        assert not r["result"] and r["value"] == "1.9.0d" and "Invalid" in r["message"]

    def test_invalid_version_not_valid_format(self):
        r = validator.validateVersion("MyVersion")
        assert not r["result"] and r["value"] == "MyVersion" and "Invalid" in r["message"]


if __name__ == "__main__":
    unittest.main()
