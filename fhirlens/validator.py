#!/usr/bin/env python3

from jsonschema import Draft6Validator
import json
import glob
import sys

r4_schema = "bin/schemas/R4/fhir.r4.schema.json"
stu3_schema = "bin/schemas/STU3/fhir.stu3.schema.json"


class Validator:
    """ Validator will hold the core validation and error interpreting, while the children
    classes will handle versions of FHIR the initialize function has a default schema set for R4 validation"""

    def __init__(self, schema_path=r4_schema, folder="bin/validate/"):
        self.validator = Draft6Validator(json.loads(open(schema_path, encoding="utf8").read()))
        self.fhirBox = folder

    def jsonValidate(self, resource):
        try:
            json.loads(resource)
            return True
        except Exception as e:
            # Printing error of JSON error immediately by default
            print(resource + ':', e)
            return False

    def boolValidate(self, resource, output=False):
        """ Returns bool for validity of resources"""

        if self.jsonValidate(resource):
            # returns bool about resource
            return self.validator.is_valid(resource)
        else:
            # Invalid JSON return
            return False

    def depthValidate(self, resource, output=False):
        """ Returns schema path to error in file -if file is invalid """

        if self.jsonValidate(resource):

            # Error interpretation
            errors = sorted(self.validator.iter_errors(resource), key=lambda e: e.path)

            for error in errors:
                # list comprehension of sub-errors
                result = [list(x.schema_path) for x in sorted(error.context, key=lambda e: e.schema_path)]
                parse = [y for y in result if 'resourceType' in y]
                parse_two = [z[0] for z in parse]
                parse_three = [a[0] for a in enumerate(parse_two) if a[0] != a[1]]

                for suberror in sorted(error.context, key=lambda e: e.schema_path):
                    if len(parse_three) < 1:
                        print(resource, ':', 'Invalid resourceType:', resource['resourceType'], 'was unexpected')
                        break
                    else:
                        if int(list(suberror.schema_path)[0]) == parse_three[0]:
                            print(resource, ':', list(suberror.schema_path)[1:], suberror.message)

        else:
            # Invalid JSON return
            return False


class R4(Validator):
    """This module may be redundant in the validators current state. I've set R4 for the default Parent schema.
    In future updates though, the default could change to the latest FHIR version. So i'm keeping this here.
    Developers can use this module simply for quick schema-version clarity"""

    def __init__(self):
        self.schema = r4_schema
        super().__init__(self.schema)


class STU3(Validator):
    def __init__(self):
        self.schema = stu3_schema
        super().__init__(self.schema)



#######################################################################################################################
# Next need to figure out where glob fits into this all. Then build out __init__.py to initialize all the junk above!


def check_compliance(j_data, filename, expand):
    k = Draft6Validator(json.loads(r4_schema))

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
