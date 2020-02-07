import unittest
from fhirlens import fhirlens
import os
from pathlib import Path


class TestJSONValidate(unittest.TestCase):

    def test_ValidJSON(self):
        validator = fhirlens.Validator()
        self.assertEqual(validator.jsonValidate({1: 'iamvalid'}), {1: 'iamvalid'})

    def test_JSONDecodeError(self):
        validator = fhirlens.Validator()
        self.assertEqual(validator.jsonValidate("{'hello': iamNOTvalid'}"), "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)")

    def test_TypeError(self):
        validator = fhirlens.Validator()
        self.assertEqual(validator.jsonValidate(1996), "the JSON object must be str, bytes or bytearray, not int")


class TestInitValidators(unittest.TestCase):

    def test_NoneTypeBeforeInit(self):
        validator = fhirlens.Validator()
        self.assertEqual(validator.validator, None)
        self.assertEqual(validator.fastvalidator, None)

    # def test_NoneTypeAfterClose(self):
    #     validator = fhirlens.Validator()
    #     validator.initValidators()
    #     validator.closeValidators()
    #     self.assertEqual(validator.validator, None)
    #     self.assertEqual(validator.fastvalidator, None)

class TestConvertToFileName(unittest.TestCase):

    def test_ValidUnixFilePath(self):
        validator = fhirlens.Validator()
        self.assertEqual(validator.convertToFileName("/hello/darkness/my/old/friend.json"), "friend.json")

    def test_ValidWindowsFilePath(self):
        validator = fhirlens.Validator()
        self.assertEqual(validator.convertToFileName("\\hello\\darkness\\my\\old\\friend.json"), "friend.json")


class TestBuildPathIndex(unittest.TestCase):

    def test_IndexPackageSchemas(self):
        validator = fhirlens.Validator()
        targetDir = str(Path('../fhirlens/schemas/'))
        self.assertEqual(validator.buildPathIndex(targetDir),
                         ['../fhirlens/schemas/fhir.stu3.schema.json', '../fhirlens/schemas/fhir.r4.schema.json'])


if __name__ == '__main__':
    unittest.main()
