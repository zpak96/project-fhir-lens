#!/usr/bin/env python3


from jsonschema import Draft6Validator
import json
import glob
import sys

r4_schema = open("bin/schemas/R4/fhir.r4.schema.json", encoding="utf8").read()
r3_schema = open("bin/schemas/STU3/fhir.stu3.schema.json", encoding="utf8").read()


def check_compliance(j_data, filename, expand):
    k = Draft6Validator(json.loads(r3_schema))

    if k.is_valid(j_data):
        print(filename + ':', 'Valid')

    elif expand:
        errors = sorted(k.iter_errors(j_data), key=lambda e: e.path)

        for error in errors:
            # list comprehension of sub-errors
            result = [list(x.schema_path) for x in sorted(error.context, key=lambda e: e.schema_path)]
            parse = [y for y in result if 'resourceType' in y]
            parse_two = [z[0] for z in parse]
            parse_three = [a[0] for a in enumerate(parse_two) if a[0] != a[1]]

            for suberror in sorted(error.context, key=lambda e: e.schema_path):
                if len(parse_three) < 1:
                    print(filename, ':', 'Invalid resourceType:', j_data['resourceType'], 'was unexpected')
                    break
                else:
                    if int(list(suberror.schema_path)[0]) == parse_three[0]:
                        print(filename, ':', list(suberror.schema_path)[1:], suberror.message)
    else:
        print(filename, ':', 'Invalid')


def main():
    expand = False

    print(sys.argv)
    if sys.argv:
        if sys.argv[-1] == "expand":
            expand = True

    for file in glob.iglob("bin/validate/**/*.json", recursive=True):

        data = open(file, encoding="utf8").read()

        filename = str(file).split('/')[-1].replace('validate\\', '')

        try:
            j_data = json.loads(data)
            check_compliance(j_data, filename, expand)
        except Exception as e:
            print(filename + ': ' + 'Invalid JSON: %s' % e)


main()
