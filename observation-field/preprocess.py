import html
import re
import unidecode
import logging
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_dict_to_lowercase(d):
    """
    Converte recursivamente todas as chaves e valores string de um dicionário para lowercase.
    Args: 
        d (dict | list | str | any): O dicionário, lista, string ou qualquer outro tipo de dado a ser convertido. 
    Returns: 
        dict | list | str | any: O dicionário, lista ou string com todos os elementos de texto convertidos para minúsculas, 
        ou o dado original se não for um tipo manipulável pela função.
    """

    if isinstance(d, dict):
        return {key.lower(): convert_dict_to_lowercase(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [convert_dict_to_lowercase(item) for item in d]
    elif isinstance(d, str):
        return d.lower()
    else:
        return d

def normalize_text(text):
    """
    Normaliza uma string removendo acentuações, convertendo entidades HTML para seus caracteres correspondentes, convertendo o 
    texto para minúsculas, removendo caracteres especiais e substituindo espaços múltiplos e quebras de linha por um único espaço.

    A função segue várias etapas para limpar e padronizar o texto: 
        1. Converte todas as letras para minúsculas para uniformidade. 
        2. Converte entidades HTML em seus caracteres equivalentes 
        3. Remove acentos de caracteres, facilitando o processamento de texto sem perda de significado. 
        4. Remove caracteres especiais listados na expressão regular (como sinais de pontuação e símbolos). 
        5. Substitui quebras de linha, tabulações e espaços excessivos por um único espaço, garantindo a consistência do texto.

    Args:
        text (str): O texto a ser normalizado.
    Returns:
        str: O texto normalizado após aplicar todas as transformações mencionadas.
    """

    text = text.lower()  # Converte para minúsculas
    text = html.unescape(text)  # Converte entidades HTML
    text = unidecode.unidecode(text)  # Remove acentos
    text = re.sub('[!@#\$%\*;><{}\[\]|\']', '', text)  # Remove caracteres especiais
    text = text.replace('\n', ' ')  # Substitui quebras de linha por espaço
    text = text.replace('//', ' ')
    text = text.replace('\t', ' ')
    text = re.sub(' +', ' ', text)
    text = text.strip()
    return text

def preprocess_data(data):
    """
    Pré-processa o dicionário 'data' verificando e modificando o campo 'observations'. Se 'observations' for uma string, a 
    função normaliza o texto usando a função `normalize_text`. Após a normalização, se o texto resultante tem menos de 3 caracteres, 
    ele é substituído por `None` e um registro de log é criado para documentar a alteração. Se o texto tem 3 ou mais caracteres, ele é mantido.

    A função tem como objetivo garantir que o campo 'observations' contenha um texto significativo e bem formatado antes de prosseguir 
    com as próximas etapas.

    Args:
        data (dict): Dicionário que contém a chave 'observations' com um valor do tipo string.

    Returns:
        dict: O dicionário 'data' com o campo 'observations' modificado pela função `normalize_text`, conforme descrito.
    """

    if 'observations' in data and isinstance(data['observations'], str):
        processed_text = normalize_text(data['observations'])
        if len(processed_text.strip()) >= 3:
            data['observations'] = processed_text
        else:
            data['observations'] = None
            logging.info(f"Text length < 3 characters, changed to None.")
            
    return data

def hash_generator(texto):
    """
    Gera um hash SHA-256 para o texto fornecido. Esse hash é posteriormente utilizado para salvar o arquivo `hash.json` no bucket do s3.

    Args:
        text (str): O texto para o qual o hash será gerado.

    Returns:
        str: O hash SHA-256 do texto, representado como uma string hexadecimal.
    """

    hash_obj = hashlib.sha256()
    hash_obj.update(texto.encode('utf-8'))
    return hash_obj.hexdigest()

def text_preprocess(data):
    """
    Aplica uma sequência de funções de processamento de texto ao campo 'observations' dentro do sub-dicionário 'data'. As operações incluem:
        1. Conversão do texto para minúsculas (convert_dict_to_lowercase).
        2. Normalização do texto, incluindo a remoção de caracteres especiais e ajuste de espaços (normalize_text).
        3. Verificação e possível remoção de textos muito curtos (preprocess_data).
        4. Geração de um hash SHA-256 para o texto, se o texto for não nulo (hash_generator)

    O resultado é o texto processado sendo atualizado em 'data', junto com o hash correspondente.

    Args:
        data (dict): O dicionário contendo o sub-dicionário 'data' que deve incluir 'observations' como uma string.

    Returns:
        dict: O dicionário 'data' com o texto processado e o hash SHA-256.
    """

    if 'data' in data and 'observations' in data['data'] and isinstance(data['data']['observations'], str):
        processed_observation = data['data']['observations']
        processed_observation = convert_dict_to_lowercase({'temp': processed_observation})['temp']
        processed_observation = normalize_text(processed_observation)

        temp_data = {'observations': processed_observation}
        temp_data = preprocess_data(temp_data)
        processed_observation = temp_data['observations']

        if processed_observation:
            hashed_processed_observation = hash_generator(processed_observation)
            data['data']['hash'] = hashed_processed_observation
        else:
            data['data']['hash'] = None

        data['data']['observations'] = processed_observation


    return data
