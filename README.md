## The Path Forward
Rito is a fork of my college capstone, Project Fhir Lens, a first iteration at validating FHIR R4 and R3.
Rito is a large refactor of the project to reflect the skills I’ve gained in the industry. Before moving forward It's neccessary to 
make the codebase easy to implement upon. Testing, testing, testing. That will be the focus for now. Next steps include:

-DSTU2 / R5 / R6 Validation

## Fast FHIR Validation

This Python package provides the tools needed to ensure the validity of Fast Healthcare Interoperability resources (FHIR)

### Usage
To import this package into your code, include this import statement:  
```from rito import rito```

For examples of FHIR R4 resources see, under the JSON section, [HL7 FHIR Downloads](https://www.hl7.org/fhir/downloads.html)

### Limitations

If working with FHIR Servers, some may validate if a codeable concept 'system' url resolves.  
This module does not validate that far. Meaning, false positives for validity are still possible.

### Built With

* [Python3](https://www.python.org/)
* [fastjsonschema](https://pypi.org/project/fastjsonschema/) - Validation framework
* [jsonschema](https://pypi.org/project/jsonschema/) - Validation framework
* [HL7 FHIR Specs](http://hl7.org/fhir/directory.html) - Documentation and schemas

### Acknowledgments

* HL7 (Documentation and examples) - https://www.hl7.org/
