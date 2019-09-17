#!/usr/bin/env python3


from jsonschema import Draft6Validator
from jsonschema.exceptions import best_match
from jsonschema.exceptions import ErrorTree
import json
import glob
import sys

schema = open("assets/schemas/R4/fhir.schema.json", encoding="utf8").read()


def check_compliance(j_data, file):
    k = Draft6Validator(json.loads(schema))

    if k.is_valid(j_data):
        print(file, ':', 'Valid')
    else:
        tree = ErrorTree(k.iter_errors(j_data))
        print(file, ':', 'Invalid R4: %s' % sorted(tree.errors))

        # for error in sorted(k.iter_errors(j_data), key=str):
        #     pass


def main():
    for file in glob.glob("assets/validate/*.json"):

        data = open(file, encoding="utf8").read()

        try:
            j_data = json.loads(data)
            check_compliance(j_data, str(file))
        except Exception as e:
            print('Invalid JSON: %s' % e)


main()
