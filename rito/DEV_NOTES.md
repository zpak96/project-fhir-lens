
~~ line 75 in rito.py: method (parse_validation_error)

    Okay, I think this means, for context in the schema path, if resourceType is within that context, isolate it.
    Finding the schema validation for the correct resourceType?
    OR - Its isolating if there is an invalid resourceType error within the context

    **
        Upate!
        https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError.schema
        https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError.context

        Since the fhir schemas are a massive schema containing mutliple schemas we need to iterate the error.context!
        Error.context follows the error relative to the schema (sub-schema) it was thrown in.
        --
        Yes, ive confirmed.
    **

~~ line 96 in rito.py

    This is very important. What this does is filter out all the false positives.
    When an error is thrown in the fhir schemas, it throws errors in EVERY sub-schema. 
    Meaning we will always have 145 schemas (at least in r4).
    We check how many times 'ResourceType' Occurs in the error context.
    If it occurs equal to the amount of sub-schemas, then 'resourceType' is invalid!

~~ line 102 in rito.py

    Expanding second list comp
    I see i enumerated 'schemas'. Specifically to extract the index.
        
    On the other hand, if index and the schema error index are off, this means two things.
        1. The resourceType is valid
        2. There will be ONE schema that does not throw a resourceType Error. 
            (that is why the index and the schema index will mismatch)
            That is the resource that we need to find.
        


