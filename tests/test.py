from fhirlens import validator

check = validator.Validator()
checkR4 = validator.R4()
checkSTU3 = validator.STU3()

print("Default Schema:", check.getSchemaName())
print("R4 Schema:", checkR4.getSchemaName())
print("STU3 Schema:", checkSTU3.getSchemaName())
