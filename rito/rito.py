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
        """
            Okay, I think this means, for context in the schema path, if resourceType is within that context, isolate it.
            Finding the schema validation for the correct resourceType?
            OR - Its isolating if there is an invalid resourceType error within the context

            **
                Upate!
                https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError.schema
                https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError.context

                Since the fhir schemas are a massive schema containing mutliple schemas we need to iterate the error.context!
                Error.context follows the error relative to the schema (sub-schema) it was thrown in.
                --
                Yes, ive confirmed.
            **

        """

        schema_rt_errors = []
        for error in sorted(error.context, key=lambda e: e.schema_path):
            """
                This is very important. What this does is filter out all the false positives.
                When an error is thrown in the fhir schemas, it throws errors in EVERY sub-schema. 
                Meaning we will always have 145 schemas (at least in r4).
                
                We check how many times 'ResourceType' Occurs in the error context.
                If it occurs equal to the amount of sub-schemas, then 'resourceType' is invalid!
            """

            # TODO: Once  I get this more cleaned up - stop converting error_context to list, use it as the deque obj!!
            error_context = list(error.schema_path)
            if 'resourceType' in error_context:
                # This appends the schema error index (which schema the error occurred)
                schema_rt_errors.append(error_context[0])

        """
            Expanding second list comp
            I see i enumerated 'schemas'. Specifically to extract the index.
            
            ****
                
                On the other hand, if index and the schema error index are off, this means two things.
                    1. The resourceType is valid
                    2. There will be ONE schema that does not throw a resourceType Error.
                        That is the resource that we need to find.
                    
            ****
        """

        # This will hold the indexes of schemas that threw resourceType errors.
        # Index needed to reference in error context
        schemas_containing_rt_errors = []

        # Here we identify the resource that did NOT throw an rt error.
        # by comparing the index, also sorted and starting from 0, when a mismatch of index, to schema_index occurs
        # The index of the first mismatch will be the schema_index we want to use for validation.
        for index, schema_rt_error in enumerate(schema_rt_errors):
            if index != schema_rt_error:
                schemas_containing_rt_errors.append(index)

        return schemas_containing_rt_errors

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
                        bool_results.update({filename: f"Unexpected resourceType: {invalid_resources['resourceType']}"})
                    # Here is where the check occurs to determine the correct resource, and what error(s) occurred
                    elif int(list(sub_errors.schema_path)[0]) == parse[0]:
                        print()
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
