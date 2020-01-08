#!/usr/bin/env python3

from jsonschema import Draft6Validator
import fastjsonschema
import os
from pathlib import Path
import json
import glob


# TODO: Decide if this method to be removed or utilized.
# TODO: Add folder and output functionality -if kept
def jsonValidate(resource):
    try:
        data = json.loads(resource)
        return data
    except json.JSONDecodeError as e:
        return e
    except TypeError as e:
        if type(resource) == dict:
            return resource
        else:
            return e


def convertFilename(file):
    return str(file).split('/')[-1].split("\\")[-1]


class Validator:
    """ Parent Validator will hold the core validation and error interpreting, while the children
    classes will handle versions of FHIR. __Init__ defaults to R4 schema validation"""

    def __init__(self, schema_path=None):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))

        # This is for handling child schemas
        if schema_path is not None:
            self.schema = schema_path
        else:
            self.schema = self.base + '/fhir.r4.schema.json'

        # Creates JSONSchema validator using our FHIR schema
        self.validator = Draft6Validator(json.loads(open(self.schema, encoding="utf8").read()))
        # TODO: implement fast validate for faster results
        self.fastvalidate = fastjsonschema.compile(json.load(open(self.schema, encoding="utf8")))

    # TODO: Add output option to method
    def validate(self, resource=None, folder=None):
        """ Returns bool for validity of resources"""

        result = {}
        if folder is not None:
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                filename = file
                resource = jsonValidate(open(file, encoding="utf8").read())

                if type(resource) == str:
                    filename = str(file).split('/')[-1].split("\\")[-1]
                    result.update({filename: resource})
                else:
                    try:
                        self.fastvalidate(resource)
                        filename = str(file).split('/')[-1].split("\\")[-1]
                        result.update({filename: True})
                    except fastjsonschema.JsonSchemaException as e:
                        result.update({filename: False})
            return self.__dissect(batch=result)
        else:
            resource = jsonValidate(resource)

            if type(resource) == str:
                return resource
            else:
                try:
                    self.fastvalidate(resource)
                    return True
                except fastjsonschema.JsonSchemaException as e:
                    self.__dissect(resource)

    def __dissect(self, resource=None, batch=None):
        if resource is not None:
            errors = sorted(self.validator.iter_errors(resource), key=lambda e: e.path)
            filename = convertFilename(resource)

            for error in errors:

                parse = [a[0] for a in enumerate([list(x.schema_path)[0] for x in
                                                  sorted(error.context, key=lambda e: e.schema_path)
                                                  if 'resourceType' in list(x.schema_path)]) if a[0] != a[1]]

                for suberror in sorted(error.context, key=lambda e: e.schema_path):
                        if len(parse) < 1:
                            batch.update({filename: 'resourceType: ' + "'" + resource['resourceType'] + "'" + 'was unexpected'})
                            break
                        else:
                            if int(list(suberror.schema_path)[0]) == parse[0]:
                                try:
                                    if batch[filename]:
                                        batch[filename].update({list(suberror.schema_path)[1:][-1]: suberror.message})
                                except KeyError as e:
                                    batch.update({filename: {list(suberror.schema_path)[1:][-1]: suberror.message}})
            return batch

        elif batch is not None:
            errorFiles = [x for x, y in batch.items() if not y]
            for file in errorFiles:
                del batch[file]
                filename = convertFilename(file)
                data = json.loads(open(Path(file), encoding="utf8").read())
                errors = sorted(self.validator.iter_errors(data), key=lambda e: e.path)
                for error in errors:
                    parse = [a[0] for a in enumerate([list(x.schema_path)[0] for x in
                                                      sorted(error.context, key=lambda e: e.schema_path)
                                                      if 'resourceType' in list(x.schema_path)]) if a[0] != a[1]]

                    for suberror in sorted(error.context, key=lambda e: e.schema_path):
                        if len(parse) < 1:
                            batch.update({filename: 'resourceType: ' + "'" + resource['resourceType'] + "'" + 'was unexpected'})
                            break
                        else:
                            if int(list(suberror.schema_path)[0]) == parse[0]:
                                try:
                                    if batch[filename]:
                                        batch[filename].update({list(suberror.schema_path)[1:][-1]: suberror.message})
                                except KeyError as e:
                                    batch.update({filename: {list(suberror.schema_path)[1:][-1]: suberror.message}})
            return batch


class R4(Validator):
    """This module may be redundant in the validators current state. I've set R4 for the default Parent schema.
    In future updates though, the default could change to the latest FHIR version. So i'm keeping this here.
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
# TODO: Return pkg version / utilize validation methods
if __name__ == "__main__":
    pass
