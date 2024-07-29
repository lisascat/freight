import pandas as pd
import numpy as np

def transform_json_to_dataframe(json_data):

    #request_date = json_data['request_date']

    trucker_data = json_data['trucker']
    cpf_motorista = trucker_data['document']

    df_dict = {'cpf_motorista': cpf_motorista}

    for i, vehicle in enumerate(json_data['vehicles'], start=1):
        df_dict[f'plate{i}'] = vehicle['plate']
        df_dict[f'proprietary_vehicle{i}'] = vehicle['proprietary_vehicle']
        df_dict[f'rntrc{i}'] = vehicle['rntrc']
        df_dict[f'rntrc_state{i}'] = vehicle['rntrc_state']
        df_dict[f'proprietary_rntrc{i}'] = vehicle['proprietary_rntrc']
        df_dict[f'rntrc_registration_date{i}'] = vehicle['rntrc_registration_date']

    return pd.DataFrame([df_dict])

def total_plates(row):
    """
    Função para calcular o número total de placas de uma composição.
    
    Essa função itera sobre as colunas de um pandas DataFrame, identificando as colunas com nomes que 
    iniciam pelo prefixo 'plate' (plate1, plate2, plate3...) e determina o número total de placas pelo maior
    índice das das colunas plates que possui valor não nulo.

    Parameters:
    row (pd.Series): Uma linha de um pandas DataFrame que contenha colunas com o nome iniciando por 'plate', 
                     seguidas por um número (ex: 'plate1', 'plate2', etc.).

    Returns:
    int: O número mais alto da placa com um valor não nulo na linha analisada. Se tais colunas não forem encontradas, 
         ou se todas as colunas de 'placa' contiverem valores NA, a função retorna 0.
    """
    plate_columns = [col for col in row.index if col.startswith('plate')]
    for col in reversed(sorted(plate_columns)):
        if pd.notna(row[col]):
            return int(col.replace('plate', ''))
    return 0

def cpf_cnpj_percentual(df):
    """
    Conta a quantidade de CPFs e CNPJs em cada linha de um DataFrame e calcula o percentual de CPFs.
    Adiciona uma nova coluna 'percentual_cpfs' ao DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame do pandas a ser processado.

    Returns:
    pd.DataFrame: DataFrame original com a coluna adicional 'percentual_cpfs'.
    """
    df['cpf_motorista'] = df['cpf_motorista'].astype(str).str.zfill(11).str.strip()
    
    def count_cpf_cnpj(row):
        cpf_vehicles_count = 0
        cnpj_vehicles_count = 0
        cpf_rntrc_count = 0
        cnpj_rntrc_count = 0

        total_plates = row['total_plates']

        vehicles_cols = [f'proprietary_vehicle{i}' for i in range(1, total_plates + 1)]
        rntrc_cols = [f'proprietary_rntrc{i}' for i in range(1, total_plates + 1)]

        for col in vehicles_cols + rntrc_cols:
            if col in row:
                value = row[col]
                if pd.notna(value):
                    value_str = str(value)  # Convert value to string before checking its length
                    if len(value_str) <= 11:
                        if col in vehicles_cols:
                            cpf_vehicles_count += 1
                        else:
                            cpf_rntrc_count += 1
                    else:
                        if col in vehicles_cols:
                            cnpj_vehicles_count += 1
                        else:
                            cnpj_rntrc_count += 1

        return pd.Series([cpf_vehicles_count, cnpj_vehicles_count, cpf_rntrc_count, cnpj_rntrc_count])

    df[['total_vehicle_cpfs', 'total_vehicles_cnpj', 'total_rntrc_cpfs', 'total_rntrc_cnpj']] = df.apply(count_cpf_cnpj, axis=1)

    df['percentual_cpfs'] = (df['total_rntrc_cpfs'] + df['total_vehicle_cpfs']) / (df['total_rntrc_cpfs'] + df['total_rntrc_cnpj'] + df['total_vehicle_cpfs'] + df['total_vehicles_cnpj'])

    df.drop(columns=['total_vehicle_cpfs', 'total_vehicles_cnpj', 'total_rntrc_cpfs', 'total_rntrc_cnpj'], inplace=True)

    return df

def remove_row_based_on_plate(df):

    for i in range(1, df['total_plates'].max()):
        plate_column = f'plate{i}'

        other_cols_with_same_numeral = [col for col in df.columns if col.endswith(str(i)) and col != plate_column]

        df = df[df[plate_column].isna() | df[other_cols_with_same_numeral].notna().all(axis=1)]

    return df

def get_registration_dates(row):
    dates = [pd.to_datetime(row[f'rntrc_registration_date{i}'], errors='coerce') for i in range(1, row['total_plates'] + 1)]
    dates = [date for date in dates if pd.notna(date)]
    
    if not dates:
        return pd.NaT, pd.NaT

    most_recent_date = max(dates)
    oldest_date = min(dates)
    return most_recent_date, oldest_date

def calculate_days_difference(df):
    df['request_date'] = pd.Timestamp.today()

    registration_dates = df.apply(get_registration_dates, axis=1, result_type='expand')
    df['most_recent_date'], df['oldest_date'] = registration_dates[0], registration_dates[1]

    df['days_difference_lower'] = (df['request_date'] - df['most_recent_date']).dt.days
    df['days_difference_higher'] = (df['request_date'] - df['oldest_date']).dt.days

    return df

def check_uf_rntrc(row):
    total_plates = row['total_plates']
    ufs = [row[f'rntrc_state{i}'] for i in range(1, total_plates + 1)]

    # Verifica se todas as colunas rntrc_state são nulas
    if all(x is None for x in ufs):
        return None  # ou qualquer outro valor para indicar a remoção da linha

    # Verifica se todas as colunas rntrc_state são iguais
    if all(x == ufs[0] for x in ufs):
        return True
    else:
        return False

def check_cpfcnpj_equivalence(row):
    total_plates = row['total_plates']
    cpf_motorista = str(row['cpf_motorista'])

    for i in range(1, total_plates + 1):
        cpfcnpj_rntrc_i = str(row[f'proprietary_rntrc{i}'])
        if cpfcnpj_rntrc_i == cpf_motorista:
            continue  

        for j in range(1, total_plates + 1):
            cpfcnpj_vehicle_j = str(row[f'proprietary_vehicle{j}'])
            if cpfcnpj_vehicle_j == cpf_motorista:
                continue 

            if cpfcnpj_rntrc_i in cpfcnpj_vehicle_j or cpfcnpj_vehicle_j in cpfcnpj_rntrc_i:
                return True
    return False

def check_owner_some_plate_all_rntrc(row):
    """
    Quantas vezes a mesma pessoa é proprietária de alguma das placas e de todos os documentos
    """
    vehicle_cols = [col for col in row.index if 'proprietary_vehicle' in col]
    rntrc_cols = [col for col in row.index if 'proprietary_rntrc' in col]

    cpf_motorista = str(row['cpf_motorista'])
    rntrc_values = [str(row[col]) for col in rntrc_cols if pd.notnull(row[col]) and str(row[col]) != cpf_motorista]

    for vehicle_col in vehicle_cols:
        if pd.notnull(row[vehicle_col]):
            vehicle_numeric = str(row[vehicle_col])
            if vehicle_numeric == cpf_motorista:
                continue  # Ignora se o CPF/CNPJ do veículo for igual ao do motorista

            if all(val in vehicle_numeric for val in rntrc_values):
                return True

    return False

def check_owner_all_plates_some_rntrc(row):
    vehicle_cols = [col for col in row.index if 'proprietary_vehicle' in col]
    rntrc_cols = [col for col in row.index if 'proprietary_rntrc' in col]

    cpf_motorista = row['cpf_motorista']
    vehicle_values = [row[col] for col in vehicle_cols if pd.notnull(row[col]) and row[col] != cpf_motorista]
    rntrc_values = [row[col] for col in rntrc_cols if pd.notnull(row[col]) and row[col] != cpf_motorista]
    
    if len(set(vehicle_values)) != 1:
        return False

    if any(any(str(rntrc_val) in str(vehicle_val) for vehicle_val in vehicle_values) for rntrc_val in rntrc_values):

        return True

    return False

def check_single_owner_for_all(row):
    vehicle_cols = [col for col in row.index if 'proprietary_vehicle' in col]
    rntrc_cols = [col for col in row.index if 'proprietary_rntrc' in col]
    
    cpf_motorista = row['cpf_motorista']
    vehicle_values = [row[col] for col in vehicle_cols if pd.notnull(row[col]) and row[col] != cpf_motorista]
    rntrc_values = [row[col] for col in rntrc_cols if pd.notnull(row[col]) and row[col] != cpf_motorista]
    
    if len(set(vehicle_values)) != 1:
        return False
    
    if len(set(rntrc_values)) != 1:
        return False
    
    if not all(all(str(rntrc_val) in str(vehicle_val) for vehicle_val in vehicle_values) for rntrc_val in rntrc_values):
        return False

    return True

def driver_features_creator(df):
    proprietary_vehicle_cols = [col for col in df.columns if col.startswith('proprietary_vehicle')]
    proprietary_rntrc_cols = [col for col in df.columns if col.startswith('proprietary_rntrc')]

    def normalize_cpf_cnpj(value):
        if pd.isnull(value):
            return np.nan
        value_str = str(value)
        # Remover o sufixo '.0' se ele existir na string
        if value_str.endswith('.0'):
            value_str = value_str[:-2]
        # Remover outros caracteres que não sejam dígitos
        value_str = ''.join(filter(str.isdigit, value_str))
        # Verificar se a string resultante não está vazia e é numérica
        if not value_str or not value_str.isdigit():
            return np.nan
        # Ajustar o comprimento da string
        if len(value_str) < 11:
            value_str = value_str.zfill(11)
        elif len(value_str) > 11 and len(value_str) < 14:
            value_str = value_str.zfill(14)
        return value_str

    df['cpf_motorista'] = df['cpf_motorista'].apply(normalize_cpf_cnpj)
    for col in proprietary_vehicle_cols + proprietary_rntrc_cols:
        df[col] = df[col].apply(normalize_cpf_cnpj)

    # Criar feature 'mot_prop_alguma_placa'
    df['mot_prop_alguma_placa'] = df.apply(lambda row: row['cpf_motorista'] in [row[col] for col in proprietary_vehicle_cols], axis=1)

    # Criar feature 'mot_prop_todas_placas'
    df['mot_prop_todas_placas'] = df.apply(lambda row: all(row['cpf_motorista'] == row[col] or pd.isna(row[col]) for col in proprietary_vehicle_cols), axis=1)

    # Criar feature 'mot_prop_algum_rntrc'
    df['mot_prop_algum_rntrc'] = df.apply(lambda row: row['cpf_motorista'] in [row[col] for col in proprietary_rntrc_cols], axis=1)

    # Criaçr feature 'mot_prop_todos_rntrc'
    df['mot_prop_todos_rntrc'] = df.apply(lambda row: all(str(row['cpf_motorista']).find(str(item)) != -1 for item in [row[f'proprietary_rntrc{i}'] for i in range(1, row['total_plates'] + 1)] if not pd.isna(item)), axis=1)
    
    return df
    
def owner_features_creator(df):
    
    df['msm_proprietario_todas_placas'] = (
    (df[[col for col in df.columns if col.startswith('proprietary_vehicle')]].nunique(axis=1) == 1) &
    (~df[[col for col in df.columns if col.startswith('proprietary_vehicle')]].isin([df['cpf_motorista']]).any(axis=1))
)
    
    df['msm_prop_alguma_placa_algum_documento'] = df.apply(check_cpfcnpj_equivalence, axis=1)
    
    df['msm_prop_algum_placa_todos_documentos'] = df.apply(check_owner_some_plate_all_rntrc, axis=1)
    
    df['msm_prop_todas_placas_algum_doc'] = df.apply(check_owner_all_plates_some_rntrc, axis=1)
    
    df['msm_proprietario_todos_documentos'] = (
    (df[[col for col in df.columns if col.startswith('proprietary_rntrc')]].nunique(axis=1) == 1) &
    (~df[[col for col in df.columns if col.startswith('proprietary_rntrc')]].isin([df['cpf_motorista']]).any(axis=1))
)
    
    df['msm_prop_all'] = df.apply(check_single_owner_for_all, axis=1)
    
    return df

def preprocessor(data):

    df = transform_json_to_dataframe(data)
    df['total_plates'] = df.apply(total_plates, axis=1)
    df = cpf_cnpj_percentual(df)
    df = remove_row_based_on_plate(df)
    df = calculate_days_difference(df)
    df['comparacao_ufs_rntrcs'] = df.apply(check_uf_rntrc, axis=1)
    df = df.dropna(subset=['comparacao_ufs_rntrcs']) 
    df = driver_features_creator(df)
    df = owner_features_creator(df)
    df = df[['mot_prop_alguma_placa', 'mot_prop_todas_placas',
       'mot_prop_algum_rntrc', 'mot_prop_todos_rntrc',
       'msm_proprietario_todas_placas',
       'msm_proprietario_todos_documentos',
       'msm_prop_alguma_placa_algum_documento',
       'msm_prop_algum_placa_todos_documentos',
       'msm_prop_todas_placas_algum_doc', 'msm_prop_all',
       'comparacao_ufs_rntrcs', 'days_difference_lower', 
       'days_difference_higher', 'total_plates',
       'percentual_cpfs']]
    
    return df