# FHIR Lens
Project-Fhir-Lens was created as as my capstone project in my Advanced Software Engineering course.

Targeted audience:
This validator is created with the developers in mind. In the current Health IT space, I have found it difficult to find a quick
solution for making sure that my JSON FHIR resources were in fact valid. With hopes, this validator will provide quick validation

### Prerequisites

Please refer to the "requirements.txt" for installing needed packages

Python 3+
JSONSchema

```
pip3 install -r "requirements.txt"
```

### Installing

Clone or download this project into your working directory

```
/home/user/development$ git clone https://github.com/zpak96/project-fhir-lens.git
```

Navigate into the project-fhir-lens/ -> From here, place resources, or folders of resources, you would like validated
in the "assets/validate/" directory.

### Getting Started

Running verify.py will print out boolean values of the FHIR R4 validity.

```
python verify.py
```

For invalid files, you can then run verify.py with the "expand" argument to find the errors in each file.

```
python verify.py expand
```

## Built With

* [jsonschema](https://pypi.org/project/jsonschema/) - The framework in which I utilize validation
* [HL7 FHIR Specs](http://hl7.org/fhir/) - Research and schemas

## Authors

* **Zane Paksi** - *Research and Development* - [Zpak96](https://github.com/zpak96)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* HL7.org for the incredible documentation and examples to study
* Michigan Health Information Network (MiHIN) - https://mihin.org/
* Interoperability Institute - https://interoperabilityinstitute.org/

* MiHIN and Interoperability Institute helped me cultivate a great interest in HL7 FHIR and the importance of making
* health data more accessible and easier to send/receive.



