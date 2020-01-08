# FHIR Lens
Project-Fhir-Lens was created as as my capstone project in my Advanced Software Engineering course.

Targeted audience:
This validator is created with the developers in mind. In the current Health IT space, I have found it difficult to find a quick
solution for making sure that my JSON FHIR resources were in fact valid. With hopes, this validator will provide quick validation

### Installation Instructions
1. Clone this repository and navigate to the base project directory.

2. Update setuptools and wheel:
```python -m pip3 install --user --upgrade setuptools wheel```

2. Install the requirements:
```pip3 install -r requirements.txt```

3. Setup the package for install:
```python setup.py sdist bdist_wheel```

4. Install the package and update Python dependencies:
```pip3 install dist/fhirlens-2.3.dev0-py3-none-any.whl```

### Usage
To import this package into your code, include this import statement:
```from fhirlens import fhirlens```

> For examples of FHIR R4 resources see, under the JSON section, [HL7 FHIR Downloads](https://www.hl7.org/fhir/downloads.html)

## Built With

* [fastjsonschema](https://pypi.org/project/fastjsonschema/) - Validation framework
* [jsonschema](https://pypi.org/project/jsonschema/) - Validation framework
* [HL7 FHIR Specs](http://hl7.org/fhir/) - Research and schemas

## Authors

* **Zane Paksi** - *Research and Development* - [Zpak96](https://github.com/zpak96)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* HL7.org for the incredible documentation and examples to study
* Michigan Health Information Network (MiHIN) - https://mihin.org/
* Interoperability Institute - https://interoperabilityinstitute.org/



