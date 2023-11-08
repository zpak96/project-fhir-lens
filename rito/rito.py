#!/usr/bin/env python3

from jsonschema.exceptions import ValidationError
from jsonschema import Draft6Validator
from typing import Union
from pathlib import Path
import fastjsonschema
import json
import glob
import os
import re


SUPPORTED_VERSIONS = [
    'r5', 'r4', 'stu3'
]


class Validator:
    """ The core of validation and error interpreting """

    def __init__(self, schema_version: str) -> None:
        self.base = os.path.join(os.path.dirname(__file__), Path('schemas/'))
        self.schema_version = schema_version

        if schema_version in SUPPORTED_VERSIONS:
            self.schema = self.base + f'/fhir.{schema_version}.schema.json'
        else:
            raise LookupError(f'Unsupported schema version: {schema_version}')

        self.validator = Draft6Validator(json.loads(open(self.schema, encoding="utf8").read()))
        self.fast_validate = fastjsonschema.compile(json.load(open(self.schema, encoding="utf8")))

    @classmethod
    def r5(cls) -> 'Validator':
        return cls('r5')

    @classmethod
    def r4(cls) -> 'Validator':
        return cls('r4')

    @classmethod
    def stu3(cls) -> 'Validator':
        return cls('stu3')

    def get_fhir_version(self) -> str:
        return self.schema_version

    @staticmethod
    def json_validate(resource: str) -> Union[dict, str]:
        # TODO: This method is a bit overloaded. It can return dict or str
        # for this type hint python versions >= 3.10 Union can be replaced with a pipe '|'
        try:
            data = json.loads(resource)
            return data
        except json.JSONDecodeError as e:
            return str(e)
        except TypeError as e:
            if isinstance(resource, dict):
                return resource
            else:
                return str(e)

    @staticmethod
    def normalize_filename(filename: str) -> str:
        return re.split('/|\\\\', filename)[-1]

    @staticmethod
    def build_path_index(folder: str) -> list:
        path_index = []
        if folder:
            for file in glob.iglob(folder + "**/*.json", recursive=True):
                filename = file
                path_index.append(filename)
        return path_index

    @staticmethod
    def locate_schema(schema_error: ValidationError) -> list:
        """
            'rt' is short for resourceType

            Since every sub-schema is validated against, if the fhir resourceType is valid,
            then there will be a single schema where a resourceType error does not occur.

            Below is an incrementing range from 0-n, n == the number of sub_schemas.
            rt_error_count will increment parallel to schema_index, until the schema
            index skips the index of the schema that did NOT throw a resourceType error.
            That is the schema_index we want. Luckily rt_error_count will reflect the
            schema index number we need.

            If all sub-schemas throw a resourceType error, the resourceType attribute is invalid.
            We return empty list.
        """

        located_schema = []
        rt_error_count = 0

        for schema_error in sorted(schema_error.context, key=lambda e: e.schema_path):
            sub_schema_error = schema_error.schema_path
            schema_index = sub_schema_error[0]

            if 'resourceType' in sub_schema_error and not located_schema:
                if rt_error_count < schema_index:
                    located_schema.append(rt_error_count)
                else:
                    rt_error_count += 1

        return located_schema

    def resolve_validation_errors(self, results: dict) -> dict:
        """ replaces the boolean values of invalid data in results with schema errors"""

        invalid_files = [filename for filename, valid in results.items() if not valid]

        for file in invalid_files:
            del results[file]
            filename = self.normalize_filename(file)
            invalid_resource = json.loads(open(Path(file), encoding="utf8").read())

            errors = sorted(self.validator.iter_errors(invalid_resource), key=lambda e: e.path)

            for error in errors:
                schema = self.locate_schema(error)

                for sub_error in sorted(error.context, key=lambda e: e.schema_path):
                    error_index = sub_error.schema_path[0]
                    error_key = sub_error.schema_path[-1]

                    if not schema:
                        results.update(
                            {filename: f"Unexpected resourceType: {invalid_resource['resourceType']}"}
                        )
                    # Here is where we check what error(s) occurred
                    elif error_index == schema[0]:
                        if filename in results:
                            results[filename].update({error_key: sub_error.message})
                        else:
                            results.update({filename: {error_key: sub_error.message}})
        return results

    def fhir_validate(self, resource_path: str) -> dict:
        """
            fhir_validate creates a dictionary of data. filename as the key, and the
            boolean depending on if the resource is valid
        """
        results = {}
        if Path.is_dir(Path(resource_path)):
            path_index = self.build_path_index(resource_path)

            for path in path_index:
                results = self.update_results(path, results)
        else:
            results = self.update_results(resource_path, results)

        return self.resolve_validation_errors(results)

    def update_results(self, resource_location: str, results: dict) -> dict:
        resource_validate = self.json_validate(open(resource_location, encoding="utf8").read())
        filename = self.normalize_filename(resource_location)
        if isinstance(resource_validate, str):
            results.update({filename: resource_validate})
        else:
            try:
                self.fast_validate(resource_validate)
                results.update({filename: True})
            except fastjsonschema.JsonSchemaException:
                results.update({resource_location: False})
        return results


if __name__ == "__main__":
    pass
