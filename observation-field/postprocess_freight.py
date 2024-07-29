import logging
import textdistance
import json
import re
from preprocess import convert_dict_to_lowercase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_last_number(texto):
    """
    Extrai o último número de padrões específicos em uma string. A função busca por sequências de dois números
    separados pela palavra 'a' (por exemplo, '31 a 33'). Ela retorna uma listancontendo o último número de cada 
    padrão encontrado.

    Parameters:
        texto (str): O texto do qual os números serão extraídos. O texto deve conter padrões numéricos 
                     onde os números são explicitamente separados por ' a ', como em '100 a 200'.

    Returns:
        list of int: Uma lista de inteiros, onde cada inteiro é o último número de um padrão encontrado
                     no texto. Retorna uma lista vazia se nenhum padrão for encontrado.
    """

    padroes = re.findall(r'\d+\s+a\s+\d+', texto)
    if padroes:
        ultimo_numero = re.search(r'(\d+)$', padroes[-1]).group()
        return ultimo_numero
    return None

def validate_and_adjust_data(freight_data, openai_response):
    """
    Valida e ajusta os dados extraídos da resposta da OpenAI para garantir que estejam no formato correto para processamento posterior.

    A função verifica cada campo da resposta para determinar se está no tipo de dados adequado (numérico ou string). 
    Para os campos numéricos, tenta converter strings para floats, tratando formatos comuns de erros como pontos de milhares e vírgulas 
    como decimais. Além disso, ajusta valores especificados em toneladas para quilogramas e trata abreviações como 'mil'. Campos que 
    devem ser strings são verificados para evitar conversões errôneas para números.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos pela OpenAI a serem validados e ajustados.

    Returns:
        dict: O dicionário openai_response após a validação e ajustes dos campos.
    """

    numeric_fields = ['num_itens', 'peso', 'comprimento', 'altura', 'largura', 'cubagem']
    string_fields = ['tipo_unidade_itens', 'unidade_peso', 'unidade_comprimento', 'unidade_altura', 'unidade_largura', 'unidade_cubagem']

    # Verificação e ajuste dos campos numéricos
    for field in numeric_fields:
        original_value = openai_response.get(field)
        if isinstance(original_value, str):
            ultimos_numeros = extract_last_number(original_value)
            if ultimos_numeros:
                original_value = ultimos_numeros
            
            try:
                temp_conversion_check = float(original_value)
                logging.info(f"Successful direct conversion to float for {field}: {original_value}")

                # Verifica se os dois últimos caracteres são '00' após um ponto decimal
                if '.' in original_value and original_value.endswith('00'):
                    openai_response[field] = float(original_value.replace('.', ''))
                else:
                    openai_response[field] = temp_conversion_check
                
            except ValueError:
                comma_count = original_value.count(',')
                print(comma_count)
                if comma_count == 2:
                    # Substitui a primeira vírgula com "" e a segunda com "."
                    parts = original_value.split(',')
                    print(parts)
                    adjusted_value = parts[0] + parts[1] + '.' + parts[2]
                    openai_response[field] = float(adjusted_value)
                else:
                    adjusted_value = original_value.replace('.', '').replace(',', '.')
                    
                try:
                    adjusted_value = original_value.replace('.', '').replace(',', '.')
                    openai_response[field] = float(adjusted_value)
                    logging.info(f"Successful direct conversion to float for {field}: {openai_response[field]}")
                except ValueError:
                        # Se ainda falhar, verifica se há "mil" ou toneladas para tratamento adicional
                    value_with_mil_replaced = adjusted_value.replace(' mil', '000')
                    value_with_ton_replaced = value_with_mil_replaced.lower().replace('toneladas', '').replace('tonelada', '').replace('ton', '').strip()
                    try:
                        final_value = float(value_with_ton_replaced) * 1000 if 'ton' in value_with_mil_replaced.lower() else float(value_with_mil_replaced)
                        openai_response[field] = final_value
                        logging.info(f"Value after handling 'mil' and 'ton' for {field}: {final_value}")


                    except ValueError:
                        logging.error(f"Final conversion error on field '{field}' with value '{original_value}'")
                        continue

    # Verificação dos campos de string
    for field in string_fields:
        value = openai_response.get(field)
        if value is not None:
            try:
                adjusted_value = value.replace(',', '.') if ',' in value else value
                float(adjusted_value)  # Tentativa de conversão para float
                logging.error(f"Invalid string on field '{field}' with value '{value}'")
            except ValueError:
                pass  # Se falhar, está correto, pois deve ser uma string

    return openai_response


def correct_units_with_dimension_priority(freight_data, openai_response):
    """
    Corrige e realoca unidades nas respostas da OpenAI baseando-se nas prioridades de dimensões quando há incompatibilidades ou erros
    nos campos de unidades.

    Esta função itera sobre um mapeamento predefinido de unidades e seus campos associados, corrigindo entradas onde o valor de um campo
    é nulo, mas sua unidade não, e tentando realocar unidades que foram mal atribuídas para campos de dimensões corretos (comprimento, 
    largura, altura). Por exemplo, se no campo "unidade_peso" vir "m3", os valores associados aos campos "peso" e "unidade_peso" serão 
    realocados para os campos "cubagem" e "unidade_cubagem". A função também lida com a normalização de unidades de peso e volume para 
    padrões consistentes, e remove unidades incorretas se não conseguir realocá-las apropriadamente.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos a serem corrigidos.

    Returns:
        dict: O dicionário openai_response após a correção das unidades.
    """

    unit_mappings = [
        ('kg', 'peso', 'unidade_peso'),
        ('kgs', 'peso', 'unidade_peso'),
        ('kls', 'peso', 'unidade_peso'),
        ('quilo', 'peso', 'unidade_peso'),
        ('quilos', 'peso', 'unidade_peso'),
        ('ton', 'peso', 'unidade_peso'),
        ('t', 'peso', 'unidade_peso'),
        ('tn', 'peso', 'unidade_peso'),
        ('tonelada', 'peso', 'unidade_peso'),
        ('toneladas', 'peso', 'unidade_peso'),
        ('m3', 'cubagem', 'unidade_cubagem'),
        ('cubicos', 'cubagem', 'unidade_cubagem'),
        ('cubico', 'cubagem', 'unidade_cubagem'),
        ('metros cubicos', 'cubagem', 'unidade_cubagem'),
        ('mts cubicos', 'cubagem', 'unidade_cubagem'),
        ('litros', 'cubagem', 'unidade_cubagem'),
        ('litro', 'cubagem', 'unidade_cubagem'),
        ('m', 'comprimento', 'unidade_comprimento'),
        ('cm', 'comprimento', 'unidade_comprimento'),
        ('mm', 'comprimento', 'unidade_comprimento'),
        ('m', 'largura', 'unidade_largura'),
        ('cm', 'largura', 'unidade_largura'),
        ('mm', 'largura', 'unidade_largura'),
        ('m', 'altura', 'unidade_altura'),
        ('cm', 'altura', 'unidade_altura'),
        ('mm', 'altura', 'unidade_altura')
    ]

    dimension_units = ['m', 'cm', 'mm']

    # Limpar unidades quando os valores correspondentes são nulos
    for unit, field, unit_field in unit_mappings:
        if openai_response.get(field) is None and openai_response.get(unit_field) is not None:
            openai_response[unit_field] = None
            logging.info(f"None found in {field}, {unit_field} changed to None")

    for unit, field, unit_field in unit_mappings:
        value = openai_response.get(field)
        unit_val = openai_response.get(unit_field)

        if unit_val and unit_val.lower() in dimension_units:
            if field in ['comprimento', 'largura', 'altura']:
                continue  # Não realoque se já está no campo correto
            dimensions = ['comprimento', 'largura', 'altura']
            assignable = False
            for dim in dimensions:
                dim_value_field = dim
                dim_unit_field = 'unidade_' + dim
                if openai_response.get(dim_value_field) is None:
                    openai_response[dim_value_field] = value
                    openai_response[dim_unit_field] = unit_val
                    openai_response[field] = None
                    openai_response[unit_field] = None
                    assignable = True
                    logging.info(f"Unit mismatch in {unit_field}, corrected to {dim_value_field} with new value {value} and unit {unit_val}.")
                    break

            if not assignable:
                # Se não há onde realocar o valor, zerar os campos errados
                openai_response[field] = None
                openai_response[unit_field] = None
                logging.error(f"No appropriate dimension fields available; {field} and {unit_field} set to None due to incorrect unit.")

    return openai_response

def adjust_weight_units(freight_data, openai_response):
    """
    Ajusta as unidades de peso nas respostas da OpenAI com base na similaridade das strings de unidade de peso com termos padrões 
    como "kg" e "ton". A função examina a unidade de peso atual e a ajusta para "kg" ou "ton" se houver uma alta similaridade com essas 
    unidades, (os threshold previamente calculados) conforme calculado pela métrica Jaro-Winkler. Isso ajuda a normalizar as unidades de
    peso em toda a resposta, convertendo abreviações ou termos similares aos padrões desejados.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos a serem ajustados para a unidade de peso correta.

    Returns:
        dict: O dicionário openai_response após ajustar as unidades de peso.
    """

    if 'unidade_peso' in openai_response and openai_response['unidade_peso'] is not None:
        unit = openai_response['unidade_peso']
        if unit == "kg" or unit == "ton":
            return openai_response

        # Calculando similaridades com a métrica Jaro-Winkler
        similarity_to_ton = textdistance.jaro_winkler("tonelada", unit)
        if similarity_to_ton >= 0.73:
            openai_response['unidade_peso'] = "ton"
            logging.info(f"unidade_peso changed to 'ton' due to jaro winkler similarity")
        else:
            similarity_to_kg = textdistance.jaro_winkler("kg", unit)
            if similarity_to_kg >= 0.9:
                openai_response['unidade_peso'] = "kg"
                logging.info(f"unidade_peso changed to 'kg' due to jaro winkler similarity")
            else:
                similarity_to_quilo = textdistance.jaro_winkler("quilo", unit)
                if similarity_to_quilo >= 0.73:
                    openai_response['unidade_peso'] = "kg"
                    logging.info(f"unidade_peso changed to 'kg' due to jaro winkler similarity")

        if unit == "kls":
            openai_response['unidade_peso'] = "kg"

    return openai_response

def adjust_tipo_unidade_itens_units(freight_data, openai_response):
    """
    Ajusta e valida as unidades do tipo de itens nas respostas da OpenAI, normalizando termos ou removendo unidades inválidas.
    Esta função verifica e corrige a unidade do tipo de itens com base em um conjunto de unidades válidas e outro de inválidas. 
    Se a unidade atual está nos termos válidos, a resposta é retornada sem mudanças. Se está nos inválidos, a unidade e a quantidade 
    de itens são anuladas. Isso foi feito devido a dificuldades em obter a resposta do campo tipo_unidade_itens sem a inclusão de 
    palavras como entrega e coleta. Além disso, a função verifica a similaridade com termos conhecidos usando a métrica Jaro-Winkler 
    (com os thresholds previamente calculados) e ajusta conforme necessário para padronizar as unidades.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos a serem ajustados para corrigir ou validar as unidades do tipo de itens.

    Returns:
        dict: O dicionário openai_response após os ajustes das unidades do tipo de itens.
    """

    valid_units = {"pallets", "caixas", "caixa", "cxs", "vols", "bag", "bags", "maquina", "maquinas", "rolo", "rolos"}
    invalid_units = {"entrega", "entregas", "coleta", "coletas"}

    similarity_check_pallets = {
        "pallets": 0.77
    }

    if 'tipo_unidade_itens' in openai_response and openai_response['tipo_unidade_itens'] is not None:
        unit = openai_response['tipo_unidade_itens']

        if unit in valid_units:
            return openai_response
        if unit in invalid_units:
            openai_response['tipo_unidade_itens'] = None
            openai_response['num_itens'] = None
            logging.info(f'invalid_unit found {unit}, changed to None')
            return openai_response

        for term, threshold in similarity_check_pallets.items():
            if textdistance.jaro_winkler(term, unit) >= threshold or unit == "plts":
                openai_response['tipo_unidade_itens'] = "pallets"
                logging.info(f"tipo_unidade_itens changed to 'pallets' due to jaro winkler similarity")
                break

    return openai_response

def adjust_volume_units(freight_data, openai_response):
    """
    Normaliza as unidades de volume nas respostas da OpenAI, corrigindo e padronizando termos associados ao volume para 'm3' 
    ou 'litros'. A função verifica se a unidade de cubagem está corretamente especificada como 'm3' ou 'litros'. Caso contrário, 
    ela procura por palavras-chave associadas a metros cúbicos e compara a similaridade de Jaro-Winkler (com os thresholds previamente 
    calculados) para ajustar a unidade de volume para 'm3' ou 'litros', de modo a garantir que as unidades de volume estejam consistentes
    e corretas nas respostas do modelo.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos a serem ajustados para corrigir as unidades de volume.

    Returns:
        dict: O dicionário freight_data, após tentar ajustar as unidades de volume em openai_response.
    """
    
    volume_keywords_m3 = ['cubicos', 'metros cubicos', 'mts cubicos', 'cubico', 'm 3', 'm³']

    if 'unidade_cubagem' in openai_response and openai_response['unidade_cubagem'] is not None:
        unit = openai_response['unidade_cubagem'].strip().lower()

        if unit == 'm3' or unit == 'litros':
            return openai_response

        if any(keyword in unit for keyword in volume_keywords_m3):
            openai_response['unidade_cubagem'] = 'm3'
            logging.info(f"unidade_cubagem changed to 'm3' due to presence in keywords list")
            return openai_response

        words = unit.split()
        for word in words:
            similarity_to_litros = textdistance.jaro_winkler('litros', word)
            similarity_to_cubicos = textdistance.jaro_winkler('cubicos', word)

            if similarity_to_cubicos > 0.9:
                openai_response['unidade_cubagem'] = 'm3'
                logging.info(f"unidade_cubagem changed to 'm3' due to jaro winkler similarity")
                break
            elif similarity_to_litros > 0.9:
                openai_response['unidade_cubagem'] = 'litros'
                logging.info(f"unidade_cubagem changed to 'litros' due to jaro winkler similarity")
                break

    return freight_data

def adjust_dimension_units(freight_data, openai_response):
    """
    Normaliza as unidades de dimensão nas respostas da OpenAI, convertendo variantes de unidades para formas canônicas ('m', 'cm', 'mm').
    A função itera sobre as unidades de dimensão especificadas (comprimento, largura, altura) e utiliza um dicionário de mapeamento para 
    converter variantes como 'metros', 'centimetros', 'milimetros' para suas formas abreviadas e padronizadas. Caso a unidade já esteja 
    em um formato canônico, ela é mantida. As alterações são registradas para monitoramento.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos a serem ajustados em termos de unidades de dimensão.

    Returns:
        dict: O dicionário openai_response após a normalização das unidades de dimensão.
    """
    inverted_unit_map = {
        'metros': 'm',
        'metro': 'm',
        'm': 'm',
        'mt': 'm',
        'mts': 'm',
        'centimetros': 'cm',
        'centimetro': 'cm',
        'cm': 'cm',
        'cms': 'cm',
        'cem': 'cm',
        'milimetros': 'mm',
        'milimetro': 'mm',
        'mm': 'mm'
    }

    # Função auxiliar para normalizar as unidades
    def normalize_unit(unit):
        unit = unit.lower().strip()
        return inverted_unit_map.get(unit, unit)  # Retorna a unidade canônica ou a original se não encontrada

    for key in ['unidade_comprimento', 'unidade_largura', 'unidade_altura']:
        if key in openai_response and openai_response[key] is not None:
            original_unit = openai_response[key]
            new_unit = normalize_unit(openai_response[key])
            openai_response[key] = new_unit
            if original_unit != new_unit:
                logging.info(f"Dimensions adjusted: {key} changed from {original_unit} to {new_unit}")

    return openai_response

def adjust_height_based_on_obs(freight_data, openai_response):
    """
    Ajusta o valor da altura no dicionário de resposta da OpenAI com base no texto do campo observações. Esta função verifica 
    a existência da palavra 'porta' nas observações dos dados do frete. Se encontrada, a altura e a unidade de altura são anuladas 
    no dicionário de resposta. Essa abordagem é necessária, dado que via prompt não foi possível tratar casos como "precisa de 2.8 m
    de altura de porta". Essas casos são de informações relativas ao caminhão e não da carga.

    Parameters:
        freight_data (dict): Dicionário contendo os dados originais do frete, atualmente não utilizado diretamente na função.
        openai_response (dict): Dicionário contendo os dados extraídos a serem ajustados, especificamente o valor da altura.

    Returns:
        dict: O dicionário openai_response após possíveis ajustes no valor da altura baseados nas observações.
    """

    altura = openai_response.get('altura')
    obs = freight_data.get('data', {}).get('observations', '')

    if altura is not None and 'porta' in obs:
        
        openai_response['altura'] = None
        openai_response['unidade_altura'] = None
        logging.info(f"altura ajustada para None devido à presença da palavra 'porta' em OBS: {obs}")

    return openai_response

def adjust_length_based_on_obs(freight_data, openai_response):
    """
    Ajusta o valor do comprimento no dicionário de resposta da OpenAI com base em frases específicas encontradas no campo de
    observações. Essa função foi criada para lidar especificamente com casos como "A carreta precisa ter 14 metros". Essa
    informação, apesar de ter vínculo com a carga é específica da carroceria. Deste modo, caso o campo "comprimento" do dicionário
    de resposta da OpenAI não for nulo, verifica-se se há correspondência com esse padrão na frase. Se sim, o campo comprimento
    é alterado para nulo.

    Parameters:
        freight_data (dict): Dicionário contendo dados originais do frete, incluindo o campo de observações que pode influenciar
                             os valores de resposta.
        openai_response (dict): Dicionário contendo dados extraídos que serão ajustados conforme descrito.

    Returns:
        None: A função não retorna nenhum valor, mas modifica o dicionário openai_response diretamente.
    """

    comprimento = openai_response.get('comprimento')
    obs = freight_data.get('data', {}).get('observations', '')

    if comprimento is not None:
        search_phrase = f"precisa ter {comprimento}"

        if search_phrase in obs:
            openai_response['comprimento'] = None
            openai_response['unidade_comprimento'] = None
            logging.info(f"Comprimento ajustado para None devido à presença da frase '{search_phrase}' em OBS: {obs}")

    return openai_response

def validate_freight(freight_data, openai_data, threshold_ton=74, max_height=4.4, max_width=2.6):
    """
    Valida e ajusta as especificações de carga com base nos limites de peso, dimensão e quantidade permitidos
    por categorias de veículos (leve, médio, pesado). A função converte e normaliza unidades quando necessário
    e ajusta dados que excedem os limites estabelecidos para garantir conformidade com restrições de transporte.

    Parameters:
        freight_data (dict): Dicionário contendo dados originais do frete, incluindo o texto do campo observações
                             e tipos de veículos.
        openai_data (dict): Dicionário contendo dados extraídos que serão validados e ajustados conforme necessário.
        threshold_ton (float): Limite de peso em toneladas acima do qual os pesos são considerados implausíveis.
        max_height (float): Altura máxima permitida em metros para todos os tipos de veículos.
        max_width (float): Largura máxima permitida em metros para todos os tipos de veículos.

    Returns:
        dict: O dicionário openai_data após a validação e ajustes de peso, dimensões, volume e quantidade de itens.
    """

    freight_data = convert_dict_to_lowercase(freight_data)
    openai_data = infer_units(openai_data)
    
    weight_limits = {
        'light': {'kg': 6000, 'ton': 6},
        'medium': {'kg': 22000, 'ton': 22},
        'heavy': {'kg': threshold_ton * 1000, 'ton': threshold_ton}
    }
    length_limits = {
        'light': 14,
        'medium': 14,
        'heavy': 19.8
    }
    volume_limits = {
        'light': 90,
        'medium': 120,
        'heavy': 190
    }
    pallet_limits = {
        'light': 22,
        'medium': 30,
        'heavy': 48
    }

    # max_height = 4.4  # Maximum allowed height in meters for all categories
    # max_width = 2.6  # Maximum allowed width in meters for all categories

    # Determine the highest category present in the vehicle types
    highest_category = 'light'
    vehicle_types = freight_data.get('data', {}).get('vehicles', {}).get('types', [])

    for vehicle in vehicle_types:
        category = vehicle.get('category', '')
        if category == 'heavy':
            highest_category = 'heavy'
            break
        elif category == 'medium' and highest_category != 'heavy':
            highest_category = 'medium'


    # Validate weight
    weight_unit = openai_data.get('unidade_peso')
    actual_weight = openai_data.get('peso', None)
    if actual_weight is not None and weight_unit == 'ton' and actual_weight > threshold_ton:
        print(f'actual_weight {actual_weight}')
        plausible_weight_in_ton = actual_weight / 1000
        print(f'plausible_weight_in_ton {plausible_weight_in_ton}')
        if plausible_weight_in_ton <= weight_limits[highest_category]['ton']:
            logging.info(f"Weight {actual_weight} tons seems implausible. Converting weight_unit to kg.")
            weight_unit = 'kg'
            openai_data['unidade_peso'] = weight_unit

    if actual_weight is not None:
        print(f'highest_category: {highest_category}')
        if weight_unit in weight_limits[highest_category]:
            max_allowed_weight = weight_limits[highest_category][weight_unit]
            if actual_weight > max_allowed_weight:
                logging.info(f"Weight {actual_weight} {weight_unit} exceeds maximum of {max_allowed_weight} {weight_unit} for {highest_category} vehicles. Adjusting weight to None.")
                openai_data['peso'] = None
                actual_weight = None

        if actual_weight is not None and weight_unit == 'ton' and actual_weight > threshold_ton:
            logging.info(f"Weight in tons {actual_weight} exceeds threshold {threshold_ton}, converting to None.")
            actual_weight = None
            weight_unit = None
            openai_data['peso'] = None
            openai_data['unidade_peso'] = None

    # Validate dimensions (length, width, height)

    for dimension_key, unit_key in [('comprimento', 'unidade_comprimento'), ('largura', 'unidade_largura'), ('altura', 'unidade_altura')]:
        actual_dimension = openai_data.get(dimension_key, None)
        dimension_unit = openai_data.get(unit_key)

        # Essa parte da função transformaria tudo em metros
#         if actual_dimension is not None:
#             if dimension_unit == 'cm':
#                 actual_dimension /= 100  # Convert cm to m
#                 openai_data[unit_key] = 'm'  # Update unit to meters
#             elif dimension_unit == 'mm':
#                 actual_dimension /= 1000  # Convert mm to m
#                 openai_data[unit_key] = 'm'  # Update unit to meters
#             elif dimension_unit is None:
#                 continue  # If unit is None, keep the original value and skip conversion

#             openai_data[dimension_key] = actual_dimension  # Update dimension after conversion

        if dimension_key == 'comprimento' and unit_key == 'm':
            max_allowed_length = length_limits[highest_category]
            if actual_dimension > max_allowed_length:
                logging.info(f"Length {actual_dimension}m exceeds maximum of {max_allowed_length}m for {highest_category} vehicles. Adjusting length to None.")
                openai_data['comprimento'] = None
        elif dimension_key == 'largura' and unit_key == 'm' and actual_dimension > max_width:
            logging.info(f"Width {actual_dimension}m exceeds universal maximum of {max_width}m. Adjusting width to None.")
            openai_data['largura'] = None
        elif dimension_key == 'altura' and unit_key == 'm' and actual_dimension > max_height:
            logging.info(f"Height {actual_dimension}m exceeds universal maximum of {max_height}m. Adjusting height to None.")
            openai_data['altura'] = None

    # Validate volume
    volume_unit = openai_data.get('unidade_volume')
    actual_volume = openai_data.get('cubagem', None)
    if actual_volume is not None and volume_unit == 'm3':
        max_allowed_volume = volume_limits[highest_category]
        if actual_volume > max_allowed_volume:
            logging.info(f"Volume {actual_volume}m3 exceeds maximum of {max_allowed_volume}m3 for {highest_category} vehicles. Adjusting volume to None.")
            openai_data['cubagem'] = None

    # Validate number of pallets
    unit_type = openai_data.get('tipo_unidade_itens')
    num_items = openai_data.get('num_itens', None)
    if unit_type == 'pallets' and num_items is not None:
        max_allowed_pallets = pallet_limits[highest_category]
        if num_items > max_allowed_pallets:
            logging.info(f"Number of pallets {num_items} exceeds maximum of {max_allowed_pallets} for {highest_category} vehicles.")
            openai_data['num_itens'] = None

    return openai_data

def infer_units(openai_data):
    """
    Infere e ajusta as unidades de medidas de peso e dimensões (comprimento, largura, altura) baseado nos valores fornecidos.
    A função apenas modifica casos em que as os capmos de unidades de peso e dimensões retornarem como nulos após inferẽncia com
    a OpenAi. A função atribui unidades de 'kg' para pesos acima de 74, dado que pesos acima de 74 toneladas ultrapassam os limites
    estabelecidos pela lei. A função também decide entre 'm' (metros) ou 'cm' (centímetros) para dimensões baseando-se na magnitude 
    do valor. Unidades são removidas se os valores excedem os limites máximos definidos para metros ou centímetros.

    Parameters:
        openai_data (dict): Dicionário contendo os dados que precisam de inferência e ajuste de unidades.

    Returns:
        dict: O dicionário openai_data após a inferência e ajuste das unidades.
    """

    if openai_data['peso'] is not None and openai_data['unidade_peso'] is None:
        if openai_data['peso'] > 74:
            openai_data['unidade_peso'] = 'kg'
        else:
            pass

    dimension_fields = ['comprimento', 'largura', 'altura']

    max_limits_meters = {
        'comprimento': 19.8,
        'largura': 2.6,
        'altura': 4.4
    }

    max_limits_centimeters = {
        'comprimento': 1980,
        'largura': 260,
        'altura': 440
    }

    for field in dimension_fields:
        value = openai_data.get(field)
        if value is not None:
            value = float(value)
            unit_field = f'unidade_{field}'

            # Divide por 100 e verifica a magnitude para tentativa de inferir a unidade
            scaled_value = value / 100
            if scaled_value < 0.1:
                openai_data[unit_field] = 'm'
            else:
                openai_data[unit_field] = 'cm'

    for field in dimension_fields:
        value = openai_data.get(field)
        unit_field = f'unidade_{field}'
        if value is not None:
            value = float(value)
            if openai_data[unit_field] == 'm' and value > max_limits_meters[field]:
                openai_data[unit_field] = None  # Deixa nulo se ultrapassar o limite
            elif openai_data[unit_field] == 'cm' and value > max_limits_centimeters[field]:
                openai_data[unit_field] = None  # Deixa nulo se ultrapassar o limite

    return openai_data

def apply_data_manipulations(freight_data, openai_response):
    """
    Aplica uma série de funções de manipulação de dados para validar e ajustar as respostas do OpenAI com base em regras e 
    também utilizando outros dados do frete.

    Parameters:
        freight_data (dict): Dicionário contendo os dados de frete que podem influenciar os ajustes nas respostas.
        openai_response (dict): Dicionário contendo as respostas do OpenAI que serão processadas pelas funções de ajuste.

    Returns:
        dict: O dicionário openai_response após a aplicação de todas as manipulações de dados.
    """

    functions = [
        validate_and_adjust_data,
        correct_units_with_dimension_priority,
        adjust_weight_units,
        adjust_tipo_unidade_itens_units,
        adjust_volume_units,
        adjust_dimension_units,
        adjust_height_based_on_obs,
    ]
    
    for func in functions:
        openai_response_processed = func(freight_data, openai_response)

    return openai_response_processed
