#!/usr/bin/env python3

from jsonschema import Draft6Validator
import os
from pathlib import Path
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

    def __init__(self, schema_path=None, folder=None):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.fhirBox = folder

        if schema_path is not None:
            self.schema = schema_path
        else:
            self.schema = self.base + '/fhir.r4.schema.json'

        self.validator = Draft6Validator(json.loads(open(self.schema, encoding="utf8").read()))

    def boolValidate(self, resource=None, folder=None):
        """ Returns bool for validity of resources"""
        if folder is not None:
            result = {}
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                resource = json.loads(open(file, encoding="utf8").read())

                filename = str(file).split('/')[-1].split("\\")[-1]
                value = self.validator.is_valid(resource)
                result.update({filename: value})

            return result
        else:
            return self.validator.is_valid(resource)

    def depthValidate(self, resource=None, folder=None, output=False):
        """ Returns schema path to error in file -if file is invalid """
        result = {}
        if folder is not None:
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                resource = json.loads(open(file, encoding="utf8").read())
                filename = str(file).split('/')[-1].split("\\")[-1]

                errors = sorted(self.validator.iter_errors(resource), key=lambda e: e.path)
                for error in errors:
                    parse = [a[0] for a in enumerate([list(x.schema_path)[0] for x in sorted(error.context, key=lambda e: e.schema_path) if 'resourceType' in list(x.schema_path)]) if a[0] != a[1]]

                    for suberror in sorted(error.context, key=lambda e: e.schema_path):
                        if len(parse) < 1:
                            result.update({filename: 'resourceType: ' + "'" + resource['resourceType'] + "'" + 'was unexpected'})
                            break
                        else:
                            if int(list(suberror.schema_path)[0]) == parse[0]:
                                try:
                                    if result[filename]:
                                        result[filename].update({list(suberror.schema_path)[1:][-1]: suberror.message})
                                except KeyError as e:
                                    result.update({filename: {list(suberror.schema_path)[1:][-1]: suberror.message}})
            return result
        else:
            errors = sorted(self.validator.iter_errors(resource), key=lambda e: e.path)
            for error in errors:
                parse = [a[0] for a in enumerate([list(x.schema_path)[0] for x in sorted(error.context, key=lambda e: e.schema_path) if 'resourceType' in list(x.schema_path)]) if a[0] != a[1]]

                for suberror in sorted(error.context, key=lambda e: e.schema_path):
                    if len(parse) < 1:
                        result.update({'resourceType: ' + "'" + resource['resourceType'] + "'" + 'was unexpected'})
                        break
                    else:
                        if int(list(suberror.schema_path)[0]) == parse[0]:
                            result.update({list(suberror.schema_path)[1:][-1]: suberror.message})
            return result


class R4(Validator):
    """This module may be redundant in the validators current state. I've set R4 for the default Parent schema.
    In future updates though, the default could change to the latest FHIR version. So i'm keeping this here.
    Developers can use this module simply for quick schema-version clarity"""

    def __init__(self):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema = self.base + "/fhir.r4.schema.json"
        super().__init__(self.schema)


class STU3(Validator):
    def __init__(self):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema = self.base + "/fhir.stu3.schema.json"
        super().__init__(self.schema)

