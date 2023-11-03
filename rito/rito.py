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

    # THIS METHOD'S PURPOSE IS TO LOCATE THE CORRECT SCHEMA
    # TODO: simplify this resource to return -> int instead of -> list[int]
    # TODO: rename for clarity
    @staticmethod
    def parse_validation_error(error):
        # rt is a shortened reference to 'resourceType'
        schema_with_rt_errors = []
        for error in sorted(error.context, key=lambda e: e.schema_path):
            # TODO: Once  I get this more cleaned up - stop converting error_context to list, use it as the deque obj!!
            error_context = list(error.schema_path)
            if 'resourceType' in error_context:
                # This appends the schema index (which schema the error occurred)
                schema_with_rt_errors.append(error_context[0])

        # This will hold the indexes of schemas did NOT throw resourceType errors.
        # Index needed to reference in error context
        schemas_without_rt_errors = []

        for expected_schema_index, schema_index in enumerate(schema_with_rt_errors):
            if expected_schema_index != schema_index:
                schemas_without_rt_errors.append(expected_schema_index)

        return schemas_without_rt_errors

    def resolve_validation_errors(self, bool_results):
        """
            replaces invalid resources boolean value with their actual validation errors
            bool_results is in the form {filename: boolean} where the boolean is the validity of the file
        """

        invalid_files = []

        # getting the key (filename) by checking the value
        for filename, valid in bool_results.items():
            if not valid:
                invalid_files.append(filename)

        for file in invalid_files:
            del bool_results[file]
            filename = self.convert_filename(file)
            invalid_resources = json.loads(open(Path(file), encoding="utf8").read())

            errors = sorted(self.validator.iter_errors(invalid_resources), key=lambda e: e.path)

            for error in errors:
                schema_indexes = self.parse_validation_error(error)

                for sub_error in sorted(error.context, key=lambda e: e.schema_path):
                    error_key = list(sub_error.schema_path)[1:][-1]

                    if len(schema_indexes) < 1:
                        bool_results.update({filename: f"Unexpected resourceType: {invalid_resources['resourceType']}"})
                    # Here is where the check occurs to determine the correct resource, and what error(s) occurred
                    elif list(sub_error.schema_path)[0] == schema_indexes[0]:
                        if filename in bool_results:
                            bool_results[filename].update({error_key: sub_error.message})
                        else:
                            bool_results.update({filename: {error_key: sub_error.message}})
        return bool_results

    def fhir_validate(self, resource_location):
        """
            fhir_validate creates a dictionary of resources. filename as the key, and the
            boolean depending on if the resource is valid
        """
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
