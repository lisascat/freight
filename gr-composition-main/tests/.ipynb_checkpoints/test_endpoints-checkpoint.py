# import requests
# import pytest
# import boto3
# import json
# import os
# from pytest import mark
# from pytest_lazyfixture import lazy_fixture

# MODEL_NAME = os.environ.get('MODEL_NAME')
# BRANCH_NAME = os.environ.get('CI_COMMIT_REF_NAME')
# versioned_model_name = f"{MODEL_NAME}-{BRANCH_NAME}"

# @pytest.mark.endpoint
# @pytest.mark.parametrize(
#     "input, output, response_code",
#     [
#         (lazy_fixture("inputValidation1"), lazy_fixture("outputValidation1"), 200),
#         (lazy_fixture("inputValidation2"), lazy_fixture("outputValidation2"), 200),
#         (lazy_fixture("inputValidation3"), lazy_fixture("outputValidation3"), 200),
#         (lazy_fixture("inputValidation4"), lazy_fixture("outputValidation4"), 200),
#         (lazy_fixture("inputValidation5"), lazy_fixture("outputValidation5"), 200),
#         (lazy_fixture("inputValidation6"), lazy_fixture("outputValidation6"), 200),
#         (lazy_fixture("inputValidation7"), lazy_fixture("outputValidation7"), 200),
#         (lazy_fixture("inputValidation8"), lazy_fixture("outputValidation8"), 412),
#         (lazy_fixture("inputValidation9"), lazy_fixture("outputValidation9"), 500)
#     ]
# )
# def test_endpoint_invocations(input, output, response_code):
#     endpoint_address = f"test-endpoint-{versioned_model_name}"
#     runtime = boto3.Session().client(
#         'sagemaker-runtime',
#         aws_access_key_id = os.environ['FRETEBRAS_MLOPS_AWS_SERVER_PUBLIC_KEY'],
#         aws_secret_access_key = os.environ['FRETEBRAS_MLOPS_AWS_SERVER_SECRET_KEY'],
#         region_name="us-east-1"
#     ) 
#     payload = json.dumps(input)

#     try:
#         response = runtime.invoke_endpoint(EndpointName=endpoint_address, ContentType='application/json', Body=payload)
#         resposta_json = json.loads(response['Body'].read().decode())
#         request_status_code = response['ResponseMetadata']['HTTPStatusCode']
#     except runtime.exceptions.ModelError as e:
#         request_status_code = e.response['OriginalStatusCode']
#         resposta_json = json.loads(e.response['OriginalMessage'])

#     assert resposta_json == output and request_status_code == response_code