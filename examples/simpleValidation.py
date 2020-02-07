from fhirlens import fhirlens
import json
from datetime import datetime


# Here's a quick example of utilizing the validator and outputting the result to a txt file

def main():

    validator = fhirlens.Validator()
    # /path/to/your/resource/
    output = validator.fhirValidate("/path/to/your/resource/")
    
    filename = "Output" + datetime.now().strftime("%m%d-%H%M-%S") + ".txt"

    with open(filename, "w") as file:
        json.dump(output, file, indent=4)
        file.close()


main()
