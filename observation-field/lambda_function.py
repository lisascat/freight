import boto3
import json
import os
import sys
import subprocess
import logging
import uuid
from datetime import datetime
import time
import base64
import io
from hashlib import sha256
import asyncio
from botocore.exceptions import ClientError
import codecs

from preprocess import text_preprocess
import prompt

sys.path.insert(1, '/tmp/')

from schema_validation import validate_schema, load_schema
from observation_processing import process_observations
import requests
from kafka import KafkaProducer

#Instanciando client kafka
KAFKA_SERVER = os.getenv('KAFKA_BROKERS')

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

topic_success = 'observation-field.sucess.events'
topic_dlq = 'observation-field.dlq'

headers_dlq = [
    ("TraceId", bytes(str(uuid.uuid4()), 'utf-8')),
    ("Source", bytes("", 'utf-8')),
    ("SchemaVersion", bytes("1.1.11", 'utf-8')),
    ("Timestamp", bytes(f"{datetime.utcnow().replace(microsecond=0).isoformat()}Z", 'utf-8')),
    ("EventType", bytes("ObservationFieldErrorDLQ", 'utf-8')),
]

headers_success = [
      ("TraceId", bytes(str(uuid.uuid4()), 'utf-8')),
      ("Source", bytes("", 'utf-8')),
      ("SchemaVersion", bytes("1.1.11", 'utf-8')),
      ("Timestamp", bytes(f"{datetime.utcnow().replace(microsecond=0).isoformat()}Z", 'utf-8')),
      ("EventType", bytes("ObservationField", 'utf-8')),
    ]

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Schema para validação do contrato de dados
schema_payload = load_schema('contrato-dados.json')

# Instanciando client do s3
s3_client = boto3.client('s3')
bucket_name = 'fb-ds-sagemaker'
object_path = 'observation-field/inferences/'

async def async_handler(event_data, s3_client, bucket_name, object_path):
    # Função auxiliar para processamentos assíncronos
    features = None
    found_in_s3 = False
    
    selected_event_data = {
        'data': {
            'cargo': event_data['data']['cargo'],
            'vehicles': event_data['data']['vehicles'],
            'identifiers': event_data['data']['identifiers'],
            'observations': event_data['data']['observations']
        }
    }
    
    logger.info(f'Selected data: {selected_event_data}')

    try:
        validate_schema(selected_event_data, schema_payload)
    except Exception as e:
        error_message = f"Schema validation failed: {e}"
        logger.error(error_message)
        logger.info(f'Sending event to DLQ')
        producer.send(topic_dlq, key=bytes(error_message, 'utf-8'), value=bytes('Schema validation failed', 'utf-8'), headers=headers_dlq)
        producer.flush()
        return features, found_in_s3
    
    observations = selected_event_data['data']['observations']
    if not observations:
        logger.info("No observations provided, returning None for features.")
        return features, found_in_s3

    features, preprocessed_data, found_in_s3 = await process_observations(s3_client, selected_event_data, bucket_name, object_path)
    logger.info('Features processed')
    if not features:
        logger.info("No features identified from text.")
        return features, found_in_s3
    else:
        logger.info(f"Processed features: {features}")
        result = {'identifiers': event_data['data']['identifiers'], 
                  'preprocessed_obs': preprocessed_data['data']['observations'],
                  'features': features}
        encoded_data = bytes(json.dumps(result), 'utf-8')
        logger.info("Sending event to success topic")
        producer.send(topic_success, encoded_data, headers=headers_success)
        producer.flush()

    return features, found_in_s3

def lambda_handler(event, context):
    start_time = time.time()
    first_topic_key = next(iter(event['records']))
    first_record = event['records'][first_topic_key][0]
    decoded_value = base64.b64decode(first_record['value']).decode('utf-8')
    
    encoded_event_type = next((header.get('EventType', None) for header in first_record['headers'] if 'EventType' in header), None)
    decoded_event_type = codecs.decode(bytes(encoded_event_type), 'utf-8')
    
    if decoded_event_type not in ('freight.created', 'freight.activated'):
        return 1
    
    features = None
    found_in_s3 = False
    
    try:
        event_data = json.loads(decoded_value)
        logger.info(f'Evento recebido: {event_data}')
        
        # Check for required fields in the event data
        required_fields = ['cargo', 'vehicles', 'identifiers', 'observations']
        missing_fields = [field for field in required_fields if field not in event_data['data']]
        if missing_fields:
            error_message = f"Missing required data fields: {', '.join(missing_fields)}"
            logger.error(error_message)
            logger.info(f'Sending event to DLQ')
            producer.send(topic_dlq, key=bytes("missing_field", 'utf-8'), value=bytes(error_message, 'utf-8'), headers=headers_dlq)
            producer.flush()
            return 1

        # Process data asynchronously
        features, found_in_s3 = asyncio.run(async_handler(event_data, s3_client, bucket_name, object_path))
        return 1

    except json.JSONDecodeError as e:
        error_message = f"JSON decoding error: {e}"
        logger.error(error_message)
        logger.info(f'Sending event to DLQ')
        producer.send(topic_dlq, key=bytes(error_message, 'utf-8'), value=bytes('JSON decode error', 'utf-8'), headers=headers_dlq)
        producer.flush()
        return 1

    except Exception as e:
        error_message = f'Error processing event: {e}'
        logger.error(error_message)
        logger.info(f'Sending event to DLQ')
        producer.send(topic_dlq, key=bytes(error_message, 'utf-8'), value=bytes('Error processing event', 'utf-8'), headers=headers_dlq)
        producer.flush()
        return 1

    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution time for general statistics. Execution time: {execution_time:.3f} seconds")
        if not features:
            logger.info(f"No features found. Execution time: {execution_time:.3f} seconds")
        else:
            if found_in_s3:
                logger.info(f"Object retrieved from S3. Execution time: {execution_time:.3f} seconds")
            else:
                logger.info(f"Processed by OpenAI. Execution time: {execution_time:.3f} seconds")
