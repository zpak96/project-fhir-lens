#!/usr/bin/env python3

from jsonschema import Draft6Validator
import fastjsonschema
import os
from pathlib import Path
import json
import glob
import re


class Validator:
    """ Parent Validator will hold the core validation and error interpreting, while the children
    classes will handle versions of FHIR. __Init__ defaults to latest FHIR schema"""

    def __init__(self, schema_path=None):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))

        # This is for handling child schemas
        if schema_path is not None:
            self.schema = schema_path
        else:
            self.schema = self.base + '/fhir.r4.schema.json'

        self.validator = Draft6Validator(json.loads(open(self.schema, encoding="utf8").read()))
        self.fastvalidate = fastjsonschema.compile(json.load(open(self.schema, encoding="utf8")))

    def jsonValidate(self, resource):
        try:
            data = json.loads(resource)
            return data
        except json.JSONDecodeError as e:
            return str(e)
        except TypeError as e:
            if type(resource) == dict:
                return resource
            else:
                return str(e)

    def convertFilename(self, file):
        return re.split('/|\\\\', file)[-1]

    def buildPathIndex(self, folder):
        pathIndex = []
        if folder is not None:
            # TODO: Some sort of path checking. Had erorr where missing trailing '/' caused many issues
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                filename = file
                pathIndex.append(filename)
        return pathIndex

    def parseValidationError(self, error):
        errorLocation = [a[0] for a in enumerate([list(x.schema_path)[0] for x in
                        sorted(error.context, key=lambda e: e.schema_path)
                        if 'resourceType' in list(x.schema_path)]) if a[0] != a[1]]
        return errorLocation

    def resolveValidationErrors(self, boolResults):
        """ replaces invalid resources boolean value with their actual validation errors"""
        invalidFiles = [x for x, y in boolResults.items() if not y]
        for file in invalidFiles:
            del boolResults[file]
            filename = self.convertFilename(file)
            invalidResource = json.loads(open(Path(file), encoding="utf8").read())

            errors = sorted(self.validator.iter_errors(invalidResource), key=lambda e: e.path)
            for error in errors:
                parse = self.parseValidationError(error)
                for suberror in sorted(error.context, key=lambda e: e.schema_path):
                    if len(parse) < 1:
                        boolResults.update({filename: 'resourceType: ' + "'" + invalidResource['resourceType'] + "'" + 'was unexpected'})
                    elif int(list(suberror.schema_path)[0]) == parse[0]:
                        try:
                            boolResults[filename].update({list(suberror.schema_path)[1:][-1]: suberror.message})
                        except KeyError as e:
                            boolResults.update({filename: {list(suberror.schema_path)[1:][-1]: suberror.message}})
        return boolResults

    def fhirValidate(self, resourceLocation):
        """ fhirValidate creates a dictionary of resources. filename as the key, and the
            boolean depending on if the resource is valid"""
        boolResults = {}
        if Path.is_dir(Path(resourceLocation)):
            pathIndex = self.buildPathIndex(resourceLocation)

            for resourceLocation in pathIndex:
                resourceValidate = self.jsonValidate(open(resourceLocation, encoding="utf8").read())
                filename = self.convertFilename(resourceLocation)

                # if string, error was excepted in jsonValidate()
                if type(resourceValidate) == str:
                    boolResults.update({filename: resourceValidate})
                else:
                    try:
                        self.fastvalidate(resourceValidate)
                        boolResults.update({filename: True})
                    except fastjsonschema.JsonSchemaException as e:
                        boolResults.update({resourceLocation: False})
        else:
            resourceValidate = self.jsonValidate(resourceLocation)

            if type(resourceValidate) == str:
                boolResults.update({resourceLocation: resourceValidate})
            else:
                try:
                    self.fastvalidate(resourceLocation)
                    boolResults.update({resourceLocation: True})
                except fastjsonschema.JsonSchemaException as e:
                    boolResults.update({resourceLocation: False})

        return self.resolveValidationErrors(boolResults)

class R4(Validator):
    """This module may be redundant in the package's current state. I've set R4 for the default Parent schema.
    In future updates though, the latest FHIR version will be the parent. So i'm keeping this here.
    Developers can use this module for quick, schema-version, clarity"""

    def __init__(self):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema = self.base + "/fhir.r4.schema.json"
        super().__init__(self.schema)


class STU3(Validator):
    """This module utilizes the FHIR STU3 schema for validation"""

    def __init__(self):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema = self.base + "/fhir.stu3.schema.json"
        super().__init__(self.schema)


# TODO: Add functionality to cmd execution of package
#       Return pkg version / utilize validation methods
if __name__ == "__main__":
    pass
