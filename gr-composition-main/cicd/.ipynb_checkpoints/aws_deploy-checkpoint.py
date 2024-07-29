import sagemaker
import time
import json
import os


def upload_json_to_s3(boto3_session, bucket_name, bucket_file_name, path):
    print("Fazendo upload do arquivo json para o S3")
    print(f"Endereço: s3://{bucket_name}/{bucket_file_name}")
    s3 = boto3_session.resource("s3")
    print(path)
    json_file = json.load(open(path, 'r'))
    print(json_file)
    bucket_ds = 'sagemaker-ds-fb'
    response = s3.Object(bucket_ds, bucket_file_name).put(Body=json.dumps(json_file, indent=4))
    
    return response

def upload_to_s3(boto3_session, bucket_name, bucket_file_name, local_model_path):
    # upload model artifact to S3 bucket

    print("Fazendo upload do modelo para o S3 S3")
    print(f"Endereço: s3://{bucket_name}/{bucket_file_name}")
    s3 = boto3_session.client("s3")
    return s3.upload_file(local_model_path, bucket_name, bucket_file_name)

def check_exist_model(sagemaker_client, model_name):
    response = sagemaker_client.list_models(
        SortBy='CreationTime',
        SortOrder='Descending',
        MaxResults=100,
        NameContains=model_name
    )
    print(response)
    if len(response['Models']) > 0 and response['Models'][0]["ModelName"] == model_name:
        return True
    
    return False

def delete_model(sagemaker_client, model_name):
    response = sagemaker_client.delete_model(
        ModelName=model_name
    )
    print('Modelo {} apagado'.format(model_name))

def create_sagemaker_model(boto3_session, model_image_uri, model_s3_uri, model_name, aws_role):
    # Create a sagemaker model  

    print("Criando modelo no sagemaker")
    print(f"Modelo: {model_name}")
    sagemaker_client = boto3_session.client("sagemaker")

    if check_exist_model(sagemaker_client, model_name):
        delete_model(sagemaker_client, model_name)

    sagemaker_session = sagemaker.Session(boto_session=boto3_session)
                                    
    container_definition = sagemaker.container_def(image_uri=model_image_uri, model_data_url=model_s3_uri)
    print(f'ROLE UTILIZADA: {aws_role}')
    sagemaker_session.create_model(name=model_name,
                                role=aws_role,
                                container_defs=[container_definition])


def check_exist_endpoint(sagemaker_client, endpoint_name):
    response = sagemaker_client.list_endpoints(
        MaxResults=100,
        NameContains=endpoint_name,
        StatusEquals='InService'
    )
    print(response)
    if len(response['Endpoints']) > 0 and response['Endpoints'][0]["EndpointName"] == endpoint_name:
        return True
    
    return False


def check_exist_endpoint_config(sagemaker_client, endpoint_config_name):
    response = sagemaker_client.list_endpoint_configs(
        SortBy='CreationTime',
        SortOrder='Descending',
        MaxResults=100,
        NameContains=endpoint_config_name
    )
    print(response)
    if len(response['EndpointConfigs']) > 0 and response['EndpointConfigs'][0]["EndpointConfigName"] == endpoint_config_name:
        return True
    
    return False

def delete_endpoint_config(sagemaker_client, endpoint_config_name):
    response = sagemaker_client.delete_endpoint_config(
        EndpointConfigName=endpoint_config_name
    )
    print('Endpoint config {} apagado'.format(endpoint_config_name))

def create_sagemaker_endpoint_config(boto3_session, versioned_model_name, data_captura_s3_uri, test=None):

    sagemaker_client = boto3_session.client("sagemaker")
    #Declarando os valores do parâmetros
    if test == None:
        endpoint_config_name = f"ecfg-{versioned_model_name}"
    else:
        endpoint_config_name = f"test-ecfg-{versioned_model_name}"
    capture_modes = [ "Input",  "Output" ] 
    #Configuração dos parâmetros de variantes do model
    configs_path                            = './deployment/config.json'
    configs                                 = json.load(open(configs_path, 'r'))
    production_variants                     = configs['deploy']['variantes']
    production_variants[0]['ModelName']     = versioned_model_name
    production_variants[0]['VariantName']   = os.environ['CI_COMMIT_REF_NAME']
    #Configuração para controlar como o SageMaker captura dados de inferência.
    data_capture_config = {
        'EnableCapture': True,
        'InitialSamplingPercentage': 100,
        'DestinationS3Uri': data_captura_s3_uri,
        'CaptureOptions': [{"CaptureMode" : capture_mode} for capture_mode in capture_modes]
    }

    endpoint_config = {
        "EndpointConfigName": endpoint_config_name,
        "ProductionVariants": production_variants,
        # "DataCaptureConfig": data_capture_config
    }
    if check_exist_endpoint_config(sagemaker_client, endpoint_config_name):
        delete_endpoint_config(sagemaker_client, endpoint_config_name)

    print(f"Criando endpoint config: {endpoint_config_name}")
    endpoint_conf_res = sagemaker_client.create_endpoint_config(**endpoint_config)

def create_sagemaker_endpoint(boto3_session, model_name, versioned_model_name, test=None):

    sagemaker_client = boto3_session.client("sagemaker")
    if test==None:
        endpoint_name = f"endpoint-{versioned_model_name}"
        endpoint_config_name = f"ecfg-{versioned_model_name}"
    else:
        endpoint_name = f"test-endpoint-{versioned_model_name}"
        endpoint_config_name = f"test-ecfg-{versioned_model_name}"

    print(f"Verificando se o endpoint {endpoint_name} existe")
    if check_exist_endpoint(sagemaker_client, endpoint_name):
        print("Endpoint existente, atualizando")
        endpoint_res = sagemaker_client.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
    else:
        print("Endpoint não encontrando, criando")
        endpoint_res = sagemaker_client.create_endpoint(
            EndpointName=endpoint_name, 
            EndpointConfigName=endpoint_config_name,
            Tags=[
                {
                    'Key': 'data_science_resource',
                    'Value': 'Endpoint'
                },
                {
                    'Key': 'EndpointName',
                    'Value': endpoint_name
                }
            ]
        )
    #Validar se o endpoint foi criado corretamente
    resp = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
    status = resp['EndpointStatus']
    print("Status: " + status)
    time.sleep(30)
    while status=='Creating' or status=='Updating':
        time.sleep(30)
        resp = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
        status = resp['EndpointStatus']
        print("Status: " + status)

    if status == "InService":
        return 0
    else:
        sagemaker_client.delete_endpoint(
            EndpointName=endpoint_name
        )
        print('retorna falha')
        return 1
def delete_endpoint(sagemaker_client, endpoint_name):
    
    response = response = sagemaker_client.delete_endpoint(
        EndpointName=endpoint_name
    )
    print('Endpoint {} apagado'.format(endpoint_name))

def destroy_environment_test(boto3_session, versioned_model_name):
    
    sagemaker_client = boto3_session.client("sagemaker")
    endpoint_name = f"test-endpoint-{versioned_model_name}"
    endpoint_config_name = f"test-ecfg-{versioned_model_name}"

    print('Deletando o endpoint_config: ', endpoint_config_name)
    delete_endpoint_config(sagemaker_client, endpoint_config_name)
    
    print('Deletando o endpoint: ', endpoint_name)
    delete_endpoint(sagemaker_client, endpoint_name)

def destroy_environment(boto3_session, versioned_model_name):

    sagemaker_client = boto3_session.client("sagemaker")
    endpoint_name = f"endpoint-{versioned_model_name}"
    endpoint_config_name = f"ecfg-{versioned_model_name}"

    
    print('Deletando o modelo: ', versioned_model_name)
    delete_model(sagemaker_client, versioned_model_name)

    print('Deletando o endpoint_config: ', endpoint_config_name)
    delete_endpoint_config(sagemaker_client, endpoint_config_name)
    
    print('Deletando o endpoint: ', endpoint_name)
    delete_endpoint(sagemaker_client, endpoint_name)
