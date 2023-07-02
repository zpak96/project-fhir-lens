#!/usr/bin/env python3

from jsonschema import Draft6Validator
import fastjsonschema
import os
from pathlib import Path
import json
import glob
import re


SUPPORTED_VERSIONS = [
    'r5', 'r4', 'stu3'
]


class Validator:
    """ The core of validation and error interpreting """

    def __init__(self, schema_version: str):
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema_version = schema_version

        if schema_version in SUPPORTED_VERSIONS:
            self.schema = self.base + f'/fhir.{schema_version}.schema.json'
        else:
            raise LookupError(f'Unsupported schema version: {schema_version}')

        self.validator = Draft6Validator(json.loads(open(self.schema, encoding="utf8").read()))
        self.fast_validate = fastjsonschema.compile(json.load(open(self.schema, encoding="utf8")))

    @classmethod
    def r5(cls):
        return cls('r5')

    @classmethod
    def r4(cls):
        return cls('r4')

    @classmethod
    def stu3(cls):
        return cls('stu3')

    def get_fhir_version(self):
        return self.schema_version

    @staticmethod
    def json_validate(resource):
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

    @staticmethod
    def convert_filename(file):
        return re.split('/|\\\\', file)[-1]

    @staticmethod
    def build_path_index(folder):
        path_index = []
        if folder:
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                filename = file
                path_index.append(filename)
        return path_index

    @staticmethod
    def parse_validation_error(error):
        error_location = [a[0] for a in enumerate([list(x.schema_path)[0] for x in
                                                   sorted(error.context, key=lambda e: e.schema_path)
                                                   if 'resourceType' in list(x.schema_path)]) if a[0] != a[1]]
        return error_location

    def resolve_validation_errors(self, bool_results):
        """ replaces invalid resources boolean value with their actual validation errors"""
        invalid_files = [x for x, y in bool_results.items() if not y]
        for file in invalid_files:
            del bool_results[file]
            filename = self.convert_filename(file)
            invalid_resources = json.loads(open(Path(file), encoding="utf8").read())

            errors = sorted(self.validator.iter_errors(invalid_resources), key=lambda e: e.path)
            for error in errors:
                parse = self.parse_validation_error(error)
                for sub_errors in sorted(error.context, key=lambda e: e.schema_path):
                    if len(parse) < 1:
                        bool_results.update({filename: 'resourceType: ' + "'" + invalid_resources[
                            'resourceType'] + "'" + 'was unexpected'})
                    elif int(list(sub_errors.schema_path)[0]) == parse[0]:
                        try:
                            bool_results[filename].update({list(sub_errors.schema_path)[1:][-1]: sub_errors.message})
                        except KeyError as e:
                            bool_results.update({filename: {list(sub_errors.schema_path)[1:][-1]: sub_errors.message}})
        return bool_results

    def fhir_validate(self, resource_location):
        """ fhir_validate creates a dictionary of resources. filename as the key, and the
            boolean depending on if the resource is valid"""
        bool_results = {}
        if Path.is_dir(Path(resource_location)):
            path_index = self.build_path_index(resource_location)

            for resource_location in path_index:
                bool_results = self.update_bool_results(resource_location, bool_results)
        else:
            bool_results = self.update_bool_results(resource_location, bool_results)

        return self.resolve_validation_errors(bool_results)

    def update_bool_results(self, resource_location, bool_results):
        resource_validate = self.json_validate(open(resource_location, encoding="utf8").read())
        filename = self.convert_filename(resource_location)
        if type(resource_validate) == str:
            bool_results.update({filename: resource_validate})
        else:
            try:
                self.fast_validate(resource_validate)
                bool_results.update({filename: True})
            except fastjsonschema.JsonSchemaException as e:
                bool_results.update({resource_location: False})
        return bool_results


if __name__ == "__main__":
    pass
