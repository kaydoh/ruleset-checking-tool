import json
import jsonschema
# from jsonschema import RefResolver
# from jsonschema.validators import validator_for
import os

SCHEMA_PATH = os.path.join('rct229', 'schema', 'ashrae-229.schema.json')
SCHEMA_KEY = 'ASHRAE229.schema.json'
SCHEMA_ENUM_PATH = os.path.join('rct229', 'schema', 'Enumerations2019ASHRAE901.schema.json')
SCHEMA_ENUM_KEY = 'Enumerations2019ASHRAE901.schema.json'

def _schema_validate(rmr_obj):
    """Validates an RMR against the schema

    This code follows the outline given in
    https://stackoverflow.com/questions/53968770/how-to-set-up-local-file-references-in-python-jsonschema-document
    """

    # Load the schema files
    with open(SCHEMA_PATH) as json_file:
        schema = json.load(json_file)
    with open(SCHEMA_ENUM_PATH) as json_file:
        schema_enum = json.load(json_file)

    # Create a resolver which maps schema references to schema objects
    schema_store = {
        SCHEMA_KEY: schema,
        SCHEMA_ENUM_KEY: schema_enum
    }
    resolver = jsonschema.RefResolver.from_schema(schema, store = schema_store)

    # Create a validator
    Validator = jsonschema.validators.validator_for(schema)
    validator = Validator(schema, resolver = resolver)

    try:
        # Throws ValidationError on failure
        validator.validate(rmr_obj)
        return {
            "passed": True,
            "error": None
        }
    except jsonschema.exceptions.ValidationError as err:
        return {
            "passed": False,
            "error": "schema invalid: " + err.message
        }


def _non_schema_validate(rmr_obj):
    """Provides non-schema validation for an RMR"""
    # TODO: Add check for unique names, etc.
    return {"passed": True, "error": None}



def validate_rmr(rmr_obj):
    """Validate an RMR against the schema and other high-level checks"""
    # Validate against the schema
    result = _schema_validate(rmr_obj)

    if result['passed']:
        # Provide non-schema validation
        result = _non_schema_validate(rmr_obj)

    return result
