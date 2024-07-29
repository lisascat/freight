import json
from jsonschema import validate, ValidationError
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def load_schema(filepath):
    with open(filepath, 'r') as schema_file:
        return json.load(schema_file)

def validate_schema(data, schema):
    try:
        validate(instance=data, schema=schema)
        logger.info('Payload validated according to data contract.')
        return True
    except ValidationError as error:
        logger.error('Invalid payload!')
        raise  # Isso vai propagar o erro para quem chamou a função
    except json.JSONDecodeError as error:
        logger.error("Failed to decode JSON:", str(error))
        raise
    except Exception as error:
        logger.error('Internal Server Error:', str(error))
        raise
