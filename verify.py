#!/usr/bin/env python3


from jsonschema import Draft6Validator
from jsonschema.exceptions import best_match
from jsonschema.exceptions import ErrorTree
import json
import glob
import sys

schema = open("assets/schemas/R4/fhir.schema.json", encoding="utf8").read()


def check_compliance(j_data, filename, expand):
    k = Draft6Validator(json.loads(schema))

    if k.is_valid(j_data):
        pass
        # print(filename[-1], ':', 'Valid')
    elif expand:
        errors = sorted(k.iter_errors(j_data), key=lambda e: e.path)

        for error in errors:

            for suberror in sorted(error.context, key=lambda e: e.schema_path):

                if int(list(suberror.schema_path)[0]) in range(0, 20):
                    print(list(suberror.schema_path))

                    # print(filename[-1], ':', list(suberror.schema_path), suberror.message)


    else:
        print(filename[-1], ':', 'Invalid')


def main():
    expand = False

    print(sys.argv)
    if sys.argv:
        if sys.argv[-1] == "expand":
            expand = True

    for file in glob.iglob("assets/validate/**/*.json", recursive=True):

        data = open(file, encoding="utf8").read()

        filename = str(file).split('/')

        try:
            j_data = json.loads(data)
            check_compliance(j_data, filename, expand)
        except Exception as e:
            print(filename[-1] + ': ' + 'Invalid JSON: %s' % e)


main()
