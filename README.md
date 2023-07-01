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