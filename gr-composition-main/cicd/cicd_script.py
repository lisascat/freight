from datetime import datetime
import json
import os
import sys

import boto3

from aws_deploy import *
from utils import format_gitlab_date
"""
COMENTAR ESSE QUANDO FOR PARA A FRETEBRAS

boto3_session = boto3.Session(
    aws_access_key_id = os.environ['CARGOX_MLOPS_AWS_SERVER_PUBLIC_KEY'],
    aws_secret_access_key = os.environ['CARGOX_MLOPS_AWS_SERVER_SECRET_KEY'],
    region_name="us-east-1"
)
"""

#CONEXÃO FRETEBRAS

boto3_session = boto3.Session(
    aws_access_key_id = os.environ['FRETEBRAS_MLOPS_AWS_SERVER_PUBLIC_KEY'],
    aws_secret_access_key = os.environ['FRETEBRAS_MLOPS_AWS_SERVER_SECRET_KEY'],
    region_name="us-east-1"
)

EC2_REGISTRY = os.environ['REGISTRY'] 
GIT_REPO = os.environ['CI_PROJECT_NAME']
IMAGE_TAG = os.environ['CI_COMMIT_SHORT_SHA']
PIPELINE_CREATED_AT = os.environ['CI_PIPELINE_CREATED_AT']
BRANCH_NAME = os.environ['CI_COMMIT_REF_NAME']
#BUCKET_NAME = os.environ['BUCKET_NAME_CARGOX']
BUCKET_NAME = os.environ['BUCKET_NAME_FRETEBRAS']
MODEL_ARTIFACT_PATH = os.environ['MODEL_ARTIFACT_PATH']


MODEL_NAME = os.environ['MODEL_NAME']
# AWS_ROLE =  os.environ['CARGOX_AWS_ROLE']
AWS_ROLE =  os.environ['FRETEBRAS_AWS_ROLE']

model_image_uri= f"{EC2_REGISTRY}/{GIT_REPO}:{IMAGE_TAG}"

version_suffix = f"{IMAGE_TAG}-{format_gitlab_date(PIPELINE_CREATED_AT)}"


versioned_model_name = f"{MODEL_NAME}-{BRANCH_NAME}"


if sys.argv[-1] == "deploy":

    # UPLOAD MODEL TO S3

    bucket_file_name = f"{MODEL_NAME}/{BRANCH_NAME}/models_artifact/{MODEL_NAME}.tar.gz"
    model_s3_uri = f"s3://{BUCKET_NAME}/{bucket_file_name}"

    upload_to_s3(boto3_session, BUCKET_NAME, bucket_file_name, MODEL_ARTIFACT_PATH)
    
    # UPLOAD CONTRATO DE DADOS
    bucket_key_contrato = f"{MODEL_NAME}/{BRANCH_NAME}/contract/contrato_dados.json"
    CONTRACT_PATH = f"./deployment/contract/contrato_dados.json"
    #upload_json_to_s3(boto3_session, BUCKET_NAME, bucket_key_contrato, CONTRACT_PATH)
    
    # UPLOAD AQUISICAO DE DADOS, SE TIVER
    #print(os.listdir('./deployment/query/'))
    try:
        bucket_key_aquisicao = f"{MODEL_NAME}/{BRANCH_NAME}/query/aquisicao_dados.json"
        AQUISICAO_PATH = f"./deployment/query/aquisicao_dados.json"
        if 'aquisicao_dados.json' in os.listdir('./deployment/query/'):
            upload_json_to_s3(boto3_session, BUCKET_NAME, bucket_key_aquisicao, AQUISICAO_PATH)
    except:
        pass
    # ---------------------------------------------------------------
    print('Nome da BRANCH: ', BRANCH_NAME)
    # CREATE SAGEMAKER MODEL AND CONTAINER DEF
    create_sagemaker_model(boto3_session, model_image_uri, model_s3_uri, versioned_model_name, AWS_ROLE)

    # ----------------------------------------------------------------

elif sys.argv[-1] == "endpoint":
    # Caminho para salvar os logs de input e output do modelo
    bucket_path_data_capture = f"{MODEL_NAME}/{BRANCH_NAME}/datacapture/"
    data_captura_s3_uri = f"s3://{BUCKET_NAME}/{bucket_path_data_capture}"
    # ENDPOINT CONFIG
    create_sagemaker_endpoint_config(boto3_session, versioned_model_name, data_captura_s3_uri)
    # ENDPOINT
    create_sagemaker_endpoint(boto3_session, MODEL_NAME, versioned_model_name)


elif sys.argv[-1] == "test_environment":
    # Caminho para salvar os logs de input e output do modelo
    bucket_path_data_capture = f"{MODEL_NAME}/{BRANCH_NAME}/datacapture/"
    data_captura_s3_uri = f"s3://{BUCKET_NAME}/{bucket_path_data_capture}"
    # ENDPOINT CONFIG
    create_sagemaker_endpoint_config(boto3_session, versioned_model_name, data_captura_s3_uri, 'teste')
    # ENDPOINT
    create_sagemaker_endpoint(boto3_session, MODEL_NAME, versioned_model_name, 'teste')

elif sys.argv[-1] == "destroy_test_env":
    destroy_environment_test(boto3_session, versioned_model_name)

elif sys.argv[-1] == "destroy":
    
    destroy_environment(boto3_session, versioned_model_name)
