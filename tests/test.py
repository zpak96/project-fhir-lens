from fhirlens import fhirlens
import json


check = fhirlens.Validator()
checkR4 = fhirlens.R4()
checkSTU3 = fhirlens.STU3()

# print("Default Schema:", check.getSchemaName())
# print("R4 Schema:", checkR4.getSchemaName())
# print("STU3 Schema:", checkSTU3.getSchemaName())

testfile = open("7094139ER.json", encoding="utf8").read()

k = json.loads(testfile)

print(checkR4.boolValidate(folder="../bin/validate/SarahThompson_resources_2019-11-26/"))

