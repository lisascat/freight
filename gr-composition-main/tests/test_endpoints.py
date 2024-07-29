# import pytest
# import boto3
# import json
# import os
# from pytest import mark
# from pytest_lazyfixture import lazy_fixture

# MODEL_NAME = os.environ.get('MODEL_NAME')
# BRANCH_NAME = os.environ.get('CI_COMMIT_REF_NAME')
# versioned_model_name = f"{MODEL_NAME}-{BRANCH_NAME}"

# # TODO: Definir entradas e saidas de exemplo (podem ser as mesmas dos testes de predicao)
# @pytest.mark.endpoint
# @mark.parametrize(
#     "input,output,status_code",
#     [
#         (lazy_fixture('entrada_inferencia_exemplo1'), lazy_fixture('saida_exemplo1'), 200)
#     ]
# )
# def test_endpoint_invocations(uncompress_model, input, output, status_code):
#     """
#     Testes de endepoints.

#     Esses testes serao rodados apenas com a API publicada no sagemaker e fazendo
#     requisicoes diretamente a API publicada.
#     """

#     endpoint_address = f"test-endpoint-{versioned_model_name}"
#     #Fazendo a requisicao
#     runtime = boto3.Session().client(
#         'sagemaker-runtime',
#         aws_access_key_id = os.environ['CARGOX_MLOPS_AWS_SERVER_PUBLIC_KEY'],
#         aws_secret_access_key = os.environ['CARGOX_MLOPS_AWS_SERVER_SECRET_KEY'],
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

#     resposta = (request_status_code, resposta_json)
#     resposta_esperada = (status_code, output)
#     assert (resposta == resposta_esperada)