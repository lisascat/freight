import json
import logging
import asyncio
from botocore.exceptions import ClientError
from postprocess_freight import apply_data_manipulations, validate_freight, infer_units
from prompt import ObservationFieldScanner
from preprocess import text_preprocess
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def parse_multiple_jsons(data):
    """
    Analisa uma string que pode conter múltiplos objetos JSON e tenta retorná-los como uma lista ou um único objeto.

    Esta função tenta carregar os dados de entrada como JSON. Se os dados forem uma lista, retorna toda a lista junto com 
    a contagem de itens. Se for um único objeto, retorna o objeto e uma contagem de um. Se a análise JSON falhar devido a 
    problemas de formato, especialmente com objetos separados por novas linhas, ela tenta corrigir o formato e analisar novamente.

    Parameters:
        data (str): A string contendo um ou mais objetos JSON, potencialmente mal formatados.

    Returns:
        tuple: Uma tupla contendo ou a lista de JSONs parseados ou um único objeto JSON, e o número de itens analisados.
    """
    json_data = None
    item_count = 0
    
    data = correct_json(data)
    
    if isinstance(data, dict):
        try:
            json_data = list(data.values())
            json_str = json.dumps(json_data)
            if '[[' in json_str:

                json_str = json_str.replace("[[", "[").replace("]]", "]")
                json_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Initial JSON decode error: {e}")
            raise 

    try:
        if not isinstance(data, list) and not isinstance(data, dict):
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                item_count = len([json_data])
                return json_data, item_count

        if isinstance(json_data, list):
            json_str = json.dumps(json_data)
            if '[[' in json_str:
                json_str = json_str.replace("[", "").replace("]", "")
                json_data = json.loads(json_str) 
            item_count = len([json_data])

            if item_count == 1:
                return json_data, item_count
            return json_data, item_count
        return json_data, item_count
    except json.JSONDecodeError:
        try:
            corrected_data = data.replace("[{{", "[{").replace("}}]", "}]")

            data = json.loads(corrected_data)
            item_count = len(data)
            if item_count == 1:
                    return data[0], item_count
            if item_count > 1:
                    logger.info("Observation field description contains more than one item.")
            return data, item_count
        except json.JSONDecodeError:
            try:
                corrected_data = data.replace("{{", "[{").replace("}}", "}]")
                data = json.loads(corrected_data)
                item_count = len(data)
                if item_count == 1:
                    return data[0], item_count
                if item_count > 1:
                    logger.info("Observation field description contains more than one item.")
                return data, item_count
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON: {e}")
                raise ValueError("Invalid JSON format")

def correct_json(json_string):
    """
    Corrige chaves mal formatadas em uma string JSON que podem não estar cercadas por aspas duplas corretamente.
    A função trata chaves que estão sem aspas ou com aspas faltantes, garantindo que todas as chaves sejam corretamente formatadas.
    """

    pattern_before = r'(?<!")\b\w+\b(?=":|\s*:)'
    pattern_after = r'"(\b\w+\b)(?=\s*:)'

    adjusted_json = re.sub(pattern_before, lambda m: f'"{m.group(0)}"', json_string)
    adjusted_json = re.sub(pattern_after, lambda m: f'"{m.group(0)}"', adjusted_json)
    
    corrected_adjusted_json = re.sub(r'"(\w+)""', r'"\1"', adjusted_json)
    corrected_adjusted_json = re.sub(r'""(\w+)"', r'"\1"', corrected_adjusted_json)

    return corrected_adjusted_json

def check_null_dict(parsed_data):
    """
    Verifica se um dicionário contém algum valor que não seja None.

    Esta função avalia se um dicionário fornecido está completamente vazio ou se todos os seus valores são None. Retorna 
    False se o dicionário estiver vazio ou se todos os valores forem None, indicando que não há dados válidos. Caso contrário, 
    retorna True. Essa função é utilizada para verificar a necessidade de processamentos adicionais após a chamada da OpenAI. 

    Parameters:
        parsed_data (dict): O dicionário a ser verificado.

    Returns:
        bool: False se todos os valores no dicionário forem None ou se o dicionário estiver vazio, caso contrário, True.
    """

    if not parsed_data:
        return False
    # Verifica se todos os valores no dicionário são None
    return not all(value is None for value in parsed_data.values())

async def process_observations(s3_client, selected_event_data, bucket_name, object_path):
    """
    Esta função assíncrona primeiro aplica pré-processamento do texto do campo de observações. Além disso, verifica 
    a existência das features ("hash do texto.json") no S3 e, em caso positivo, recupera e valida esses dados. Se os dados 
    não forem encontrados no S3, trata a situação de arquivo ausente a partir da função handle_missing_file.

    Parâmetros:
        s3_client (boto3.S3.Client): Cliente S3 para acessar o bucket do AWS S3.
        selected_event_data (dict): Dados do evento selecionados para processamento.
        bucket_name (str): Nome do bucket no S3 onde os dados estão armazenados ou serão armazenados.
        object_path (str): Caminho base no bucket do S3 para a localização dos objetos.

    Retorna:
        tuple: Uma tupla contendo as features validadas extraídas a partir do texto do campo de observações, 
        dados pré-processados e um booleano indicando se os dados foram encontrados no S3.
    """

    preprocessed_data = text_preprocess(selected_event_data)
    logger.info(f'text_preprocess function applied. Selected data ofter preprocessing: {preprocessed_data}')

    features = None
    found_in_s3 = False

    if not preprocessed_data['data']['observations']:
        logger.info('No observations found after preprocessing.')
        return features, preprocessed_data, found_in_s3
    hash_key = preprocessed_data['data']['hash']
    file_name = f"{object_path}{hash_key}.json"

    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        logger.info(f"Object found in S3.")
        file_content = response['Body'].read().decode('utf-8')
        try:
            data_s3 = json.loads(file_content)
            found_in_s3 = True
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from file_content: {e}")
            raise ValueError("Invalid JSON in file_content")
        logger.info(f'File retrieved from S3 with features: {data_s3}.')
        if not data_s3:
            logger.info("No features to validate, skipping validate_freight function.")
            features = {'features': data_s3}
        else:
            logger.info(f'Features will be validated with validate_freight function.')
            response = validate_freight(preprocessed_data, data_s3)
            features = {'features': response}
            logger.info(f'Validated features: {features}')

        return features, preprocessed_data, found_in_s3
    except ClientError as error:
        if error.response['Error']['Code'] == '404' or error.response['Error']['Code'] == 'NoSuchKey':
            logger.info(f'File not found in s3, file key: {file_name}')
            features = await handle_missing_file(s3_client, preprocessed_data, file_name, bucket_name)
            return features, preprocessed_data, found_in_s3
        logger.error(f'Unexpected S3 error: {error}')
        raise

    return features, preprocessed_data, found_in_s3

async def handle_missing_file(s3_client, preprocessed_data, file_name, bucket_name):
    """
    Esta função assíncrona é chamada quando o arquivo esperado ("hash do texto.json") não é encontrado no S3. 
    Ela envia os dados do campo de observações pré-processado para a API da OpenAI, processa a resposta, valida 
    e salva o resultado no S3. Se a resposta da OpenAI não for adequada para processamento adicional (Se o retorno for 
    nulo ou um dicinário com todas as features nulas), ou se houver mais de um item nos dados processados, a função 
    gerencia essas condições adequadamente.

    Parâmetros:
        s3_client (boto3.S3.Client): Cliente S3 para interagir com o AWS S3.
        preprocessed_data (dict): Texto do campo de observações pré-processados, pronto para a extração de informações.
        file_name (str): Nome do arquivo que foi procurado no S3 e não encontrado.
        bucket_name (str): Nome do bucket no S3 onde os dados devem ser armazenados.

    Retorna:
        dict: Dicionário contendo as características dos dados processados e validados ou None se os dados
              não puderem ser processados adequadamente.
    """

    observations = preprocessed_data['data']['observations']
    logger.info('Calling OpenAI')
    scanner = ObservationFieldScanner(delay_in_seconds=1)
    response_openai = await scanner.observation_field(observations)
    if response_openai is None:
        features = {'features': None}
        return features
    logger.info(f'Openai response raw data: {response_openai}')
    
    try:
        parsed_data, item_count = parse_multiple_jsons(response_openai)
    except json.JSONDecodeError:
        logger.warning("Malformed JSON detected, attempting to correct.")
        response_openai = correct_json(response_openai)
        try:
            parsed_data, item_count = parse_multiple_jsons(response_openai)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON even after correction: {e}")
            raise ValueError("Invalid JSON format in OpenAI response")

    logger.info(f'Total itens found on freight: {item_count}')
    if item_count != 1:
        features = {'features': None}
        logger.info(f'Features changed to None, as there is more than one item on the freight')
        return features

    if isinstance(parsed_data, str):
        try:
            parsed_data = json.loads(parsed_data)
            logger.info(f'Type of data after JSON parsing: {type(response_openai)}')
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from response_openai: {e}")
            raise ValueError("Invalid JSON in response_openai")

    if isinstance(parsed_data, list):
        if item_count == 1:
            parsed_data = parsed_data[0]
        else:
            logger.error("Parsed data contains more than one item and cannot be processed as a single item.")
            raise ValueError("Parsed data contains more than one item and cannot be processed as a single item.")
    if check_null_dict(parsed_data):
        response = apply_data_manipulations(preprocessed_data, parsed_data)
        logger.info(f'OpenAI response after postprocess functions: {response}')
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(response))
        logger.info("Response processed and saved to S3.")
        response = validate_freight(preprocessed_data, parsed_data)
        logger.info("Response validated with validate_freight function.")
    else:
        logger.info("Parsed data is not valid for further processing.")
        response = {'features': None}

    return response
