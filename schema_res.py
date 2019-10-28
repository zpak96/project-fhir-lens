#!/usr/bin/env python3


from jsonschema import *
from jsonschema.validators import _id_of
import requests
import json
import glob
import sys


schema = open("assets/schemas/R4/fhir.schema.json", encoding="utf8")
# schema = json.loads(schema)
print(_id_of(schema))

# print(k)
