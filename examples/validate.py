from datetime import datetime
from rito import rito
import json


# Here's a quick example of utilizing the validator and outputting the result to a txt file
def main():
    validator = rito.Validator('r4')
    output = validator.fhir_validate("../test/data/invalid_r4_patient.json")

    filename = "output" + datetime.now().strftime("%m%d-%H%M-%S") + ".txt"
    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
        file.close()


main()
