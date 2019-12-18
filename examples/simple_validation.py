from fhirlens import fhirlens
import json
from datetime import datetime


# Here's a quick example of utilizing the validator and outputting the result to a txt file

def main():
    # Instantiate a validator -> fhirlens.Validator() defaults to latest FHIR version: R4
    validator = fhirlens.Validator()
    # Other options include:
    ##### fhirlens.R4() -> Specifically utilizes R4 schema
    ##### fhirlens.STU3() -> Specifically utilizes STU3 schema

    # Choose a method of validation. Methods will return output as dict -> {file/resource_name : Validation_result}
    #### boolValidate: returns dict with boolean values
    #### depthValidate: returns dict with exact errors in resource -> {file/resource_name: {error_message: schema_location}}

    # output = validator.depthValidate(folder="validate/")
    output = validator.boolValidate(folder="validate/")
    
    filename = "Output" + datetime.now().strftime("%m%d-%H%M-%S") + ".txt"

    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
        file.close()


main()
