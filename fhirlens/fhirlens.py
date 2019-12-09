#!/usr/bin/env python3

from jsonschema import Draft6Validator
import json
import glob


def jsonValidate(resource):
    try:
        json.loads(resource)
        return True
    except Exception as e:
        # Printing error of JSON error immediately by default
        print(resource + ':', e)
        return False


class Validator:
    """ Validator will hold the core validation and error interpreting, while the children
    classes will handle versions of FHIR the initialize function has a default schema set for R4 validation"""

    def __init__(self, schema_path=open("../bin/schemas/R4/fhir.r4.schema.json", encoding="utf8").read(), folder="bin/validate/"):
        self.schema_name = schema_path.split('/')[-1]
        self.validator = Draft6Validator(json.loads(schema_path))
        self.fhirBox = folder

    def boolValidate(self, resource=None, folder=None, output=False):
        """ Returns bool for validity of resources"""
        if folder is not None:
            result = {}
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                resource = json.loads(open(file, encoding="utf8").read())

                filename = str(file).split('/')[-1].split("\\")[-1]
                value = self.validator.is_valid(resource)
                result.update({filename : value})
            return json.dumps(result, indent=4, sort_keys=True)
            result.clear()
        else:
            return self.validator.is_valid(resource)

    def depthValidate(self, resource=None, folder=None, output=False):
        """ Returns schema path to error in file -if file is invalid """
        errors = sorted(self.validator.iter_errors(resource), key=lambda e: e.path)

        for error in errors:
            # list comprehension of sub-errors
            result = [list(x.schema_path) for x in sorted(error.context, key=lambda e: e.schema_path)]
            parse = [y for y in result if 'resourceType' in y]
            parse_two = [z[0] for z in parse]
            parse_three = [a[0] for a in enumerate(parse_two) if a[0] != a[1]]

            for suberror in sorted(error.context, key=lambda e: e.schema_path):
                if len(parse_three) < 1:
                    print('Invalid resourceType:', "'" + resource['resourceType'] + "'", 'was unexpected')
                    break
                else:
                    if int(list(suberror.schema_path)[0]) == parse_three[0]:
                        print(list(suberror.schema_path)[1:], suberror.message)


class R4(Validator):
    """This module may be redundant in the validators current state. I've set R4 for the default Parent schema.
    In future updates though, the default could change to the latest FHIR version. So i'm keeping this here.
    Developers can use this module simply for quick schema-version clarity"""

    def __init__(self):
        self.schema = open("../bin/schemas/R4/fhir.r4.schema.json", encoding="utf8").read()
        super().__init__(self.schema)


class STU3(Validator):
    def __init__(self):
        self.schema = open("../bin/schemas/STU3/fhir.stu3.schema.json", encoding="utf8").read()
        super().__init__(self.schema)

