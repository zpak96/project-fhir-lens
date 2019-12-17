from fhirlens import fhirlens
import json

check = fhirlens.Validator()

k = {'resourceType': 'Encounter'}

# print(check.boolValidate(k))
print(check.depthValidate(k))
