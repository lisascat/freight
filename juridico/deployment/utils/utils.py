import pandas as pd
import numpy as np
from rapidfuzz import fuzz
import unidecode
import re
import ujson as json
from typing import List, Tuple, Dict


# Lista de palavras-chave a serem excluídas
KEYWORDS_EXCLUDE_MAINSUBJECT = ['precatória', 'iptu', 'ipva', 'fiscal', 'bancario', 'condomini', 'divida', 'consumidor', 'pagamento', 'inadimple', 'pretação', 'imposto', 'devedor', 'finan', 'fiduciaria', 'alienacao', 'recurso', 'inventario', 'usucapiao', 'tutela', 'promissoria', 'administrativ', 'imovel', 'civil', 'peticao', 'obrigacao', 'tribut', 'regulamentação', 'despejo', 'expropriação', 'telefonia', 'contrato', 'seguro', 'compra e venda', 'nulidade', 'precatoria', 'auxilio', 'licenciamento', 'duplicata', 'inquirição ', 'consorcio', 'fixação', 'intimação', 'penhora', 'monitoria', 'reivindicacao', 'liquidação', 'citacao', 'gratificaç', 'aposentadoria', 'dispensa', 'fornecimento de agua', 'benfeitoria', 'arbitramento', 'medida cautelar', 'emprestimo', 'diligenc', 'dissoluc', 'liminar', 'gratuita', 'atos processuais', 'aquisição', 'honorarios', 'levantamento', 'pensao', 'ordinari', 'reconvencao', 'indeniza', 'recuperação', 'falencia', 'mandato', 'cauculo', 'fgts', 'suspensivo', 'execu', 'arrenda', 'erario', 'adimplemento', 'compromisso', 'direito de imagem', 'impugnação de valor', 'inflação', 'jurisdição', 'trabalho', 'declaratória', 'concurso publico', 'protesto', 'debito', 'decadencia', 'acompanha', 'reintegração de posse', 'correcao monetaria', 'taxa', 'cobranca', 'extrajudicial', 'credito', 'competencia do mp', 'previdencia', 'deposito', 'classificação', 'exoneração', 'direitos da personalidade', 'interroga', 'arrolamento', 'atraso de voo', 'rescisao', 'improbidade', 'vizinh', 'beneficio', 'formal', 'corretagem', 'custas', 'dpvat', 'procedimento do juizado', 'medico', 'redibitorio', 'bem de familia', 'vicios de construção', 'mutuo', 'expediente', 'transação', 'plano de saude', 'planos de saude', 'inss', 'divorcio', 'estabelecimento de ensino', 'processo sem assunto', 'carta precatoria', 'oitiva', 'apelação', 'separação de corpos', 'adjudicacao compulsoria', 'partilha', 'cheque', 'sucessoes', 'termo circunstanciado', 'procedimento sumário', 'inquirição de testemunha', 'garantias constitucionais', 'auxilio-reclusao', 'auxilio reclusao', 'cdc', 'servidao', 'praticas abusivas', 'perturbação', 'apreensão de veículo']
# Remove a acentuação e converte as palavras-chave para minúsculas
KEYWORDS_EXCLUDE_MAINSUBJECT = [unidecode.unidecode(keyword).lower() for keyword in KEYWORDS_EXCLUDE_MAINSUBJECT]

def courtSelector(data: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona apenas as linhas do DataFrame que correspondem a processos civis ou criminais.

    Args:
        data (pandas.DataFrame): o DataFrame de entrada contendo os dados dos processos.

    Returns:
        pandas.DataFrame: o DataFrame de saída contendo apenas as linhas que correspondem a processos civis ou criminais.
    """
    df = data.copy()
    
    # Define uma lista com as palavras que correspondem aos tribunais de interesse: civel e criminal
    courtWords = ['civel', 'criminal']
    
    # Seleciona apenas as linhas do DataFrame que contêm uma das palavras da lista "courtWords".
    df = df.loc[df['CourtType'].str.contains('|'.join(courtWords))]
    
    # Verifica se o DataFrame resultante está vazio
    if df.empty:
    # Retorna um novo DataFrame vazio
        return pd.DataFrame()

    # Retorna o DataFrame de saída contendo apenas as linhas que correspondem a processos civis ou criminais.
    return df

def civilSelector(data: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona os processos civis que correspondem aos assuntos que não devem ser levados em consideração para o cálculo do score jurídico. Esses assuntos
    foram considerados relevantes apenas para a vara criminal.

    Args:
        data (pandas.DataFrame): o DataFrame de entrada contendo os dados dos processos.

    Returns:
        pandas.DataFrame: o DataFrame de saída contendo os processos que não correspondem aos assuntos de interesse.
    """
    # Seleciona apenas os processos civis.
    civel = data.query("CourtType == 'civel'")

    # Seleciona apenas os processos civis que correspondem aos assuntos que devem ser excluídos.
    processWords = ['cnh', 'acidente de transito', 'busca e apreensao']
    civel = civel.query("MainSubject in @processWords")

    # Retorna os processos que não correspondem aos assuntos de interesse.
    df = data.loc[~data['Number'].isin(civel['Number'])]
    
        # Verifica se o DataFrame resultante está vazio
    if df.empty:
    # Retorna um novo DataFrame vazio
        return pd.DataFrame()

    # Retorna o DataFrame de saída.
    return df

def defendantSelector(data: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona apenas motoristas que são de réus dos processos do conjunto de dados.

    Args:
        data (pd.DataFrame): O conjunto de dados a ser processado.

    Returns:
        pd.DataFrame: O conjunto de dados filtrado apenas com os dados dos réus.
    """
    
    df_copy = data.copy()
    
    if 'Doc' not in df_copy.columns:
        df_copy['Doc'] = ''
    # Ajustar as colunas cpf e Doc para string
    df = df_copy.assign(
        document=df_copy['document'].astype(str),
        Doc=df_copy['Doc'].astype(str)
    )

    # Padrozina a formatação do cpf
    df['document'] = df['document'].str.pad(width=11, fillchar='0')
    # Seleciona linhas que dizem respeito aos réus apenas com as colunas cpf e Doc iguais
    cpf_doc = df.loc[df['document'] == df['Doc']]

    # Para os casos onde não foi encontrado o documento do réu (a informação não veio preenchida), fazer uma aproximação pelo nome
    df['name'] = df['name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()
    names = df.loc[df['document'] != df['Doc']]
    names = names.loc[names['name'] == names['Name'].str.lower()]

    # Concatena os réus selecionados (identificados)
    df_cpf_names = pd.concat([cpf_doc, names])
    # Seleciona réus que não conseguimos identificar com as colunas cpf e Doc, mas que possuem a informação name não nula
    df_fuzzy = df.loc[~df['person_uuid'].isin(df_cpf_names['person_uuid'])]
    if not df_fuzzy.empty:

        df_fuzzy = df_fuzzy.loc[(df_fuzzy['document'] != df_fuzzy['Doc']) & (df_fuzzy['Name'].notnull())]
        # Calcula o token set ratio para cada par de nome e Name
        df_fuzzy['token_set_ratio'] = df_fuzzy.apply(lambda row: fuzz.token_set_ratio(row['name'], row['Name']), axis=1)
        # Seleciona réus com token set ratio acima de 90
        df_fuzzy_90 = df_fuzzy.loc[df_fuzzy['token_set_ratio'] > 90]

        # Concatena os réus selecionados
        return pd.concat([df_cpf_names, df_fuzzy_90])
    
        # Verifica se o DataFrame resultante está vazio
    if df_cpf_names.empty:
    # Retorna um novo DataFrame vazio
        return pd.DataFrame()

    return df_cpf_names

def excludeKeywords(data: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona apenas processos relevantes para o problema de negócios da GR, excluíndo aqueles relacionados às palavras chaves em KEYWORDS_EXCLUDE_MAINSUBJECT

    Args:
        data (pd.DataFrame): O conjunto de dados a ser processado.

    Returns:
        pd.DataFrame: O conjunto de dados filtrado apenas com processos de assunto de interesse.

    """
    # Faz uma cópia do DataFrame de entrada para evitar alterá-lo diretamente.
    df = data.copy()

    # Remove a acentuação e converte para minúsculas a coluna de assunto principal dos processos
    df['MainSubject'] = (df['MainSubject'].str.lower().apply(unidecode.unidecode))

    # Filtra as linhas que contêm palavras-chave
    df = df.loc[~df['MainSubject'].str.contains('|'.join(KEYWORDS_EXCLUDE_MAINSUBJECT), na=False)]
    
    # Verifica se o DataFrame resultante está vazio
    if df.empty:
        # Retorna um novo DataFrame vazio
        return pd.DataFrame()
    
    return df

def typeSelector(data):
    """
    Processa uma coluna de um dataframe contendo jsons e retorna um novo dataframe com os dados processados.

    Args:
        data (pd.DataFrame): O dataframe contendo a coluna a ser processada.
        column (str): O nome da coluna a ser processada.

    Returns:
        pd.DataFrame: O novo dataframe com os dados processados.

    """
    # Faz uma cópia do dataframe para não alterar o original
    df = data.copy()

    df_parties = df.loc[df['Polarity'] == 'passive']
    
    df_parties['Type'] = np.where(df_parties['Type'] == '', df_parties['SpecificType'], df_parties['Type'])
    
    df_parties = df_parties.loc[(df_parties['Type'] == 'defendant') | (df_parties['Type'] == 'claimed')]
    
    df_processed = defendantSelector(df_parties)
    
    # Verifica se o DataFrame resultante está vazio
    if df_processed.empty:
        # Retorna um novo DataFrame vazio
        return pd.DataFrame()


    return df_processed

def subjectSelector(data: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], Dict[str, int]]:
    """
    Retorna um dataframe filtrado com base em palavras-chave relacionadas a crimes.

    Args:
        data (pd.DataFrame): O dataframe a ser filtrado.

    Returns:
        pd.DataFrame: O dataframe filtrado.
    """
    criminal = {'homicidio':4,
            'roubo':4,
            'furto':3,
            'lesao corporal':2,
            'ameaca':1,
            'contra a vida':4,
            'medidas protetivas':2,
            'pudor':1,
            'sistema nacional de armas':2,
            'porte ilegal de arma':2,
            'disparo de arma':2,
            'extorsao':2,
            'sequestro':4,
            'estupro':4,
            'violacao de domicilio':2,
            'violencia domestica':2,
            'esbulho':1,
            'turbacao':1,
            'trafico':4,
            'dano material':1, 
            'infanticidio':4,
            'matar':4,
            'morte':4,
            'omissao de socorro':4,
            'ameaca':1, 
            'carcere':3, 
            'corrupcao':4, 
            'corrupcao de menores':4,
            'feminicidio':4, 
            'abuso de vulneravel':4,
            'maria da penha':2, 
            'latrocinio':4, 
            'organizacao criminosa':4, 
            'terrorista':4, 
            'associacao criminosa':4, 
            'escravo':4,#'condições análogas à de escravo',
            'transito':4,     
            'veiculo':3, # 'Adulteração de sinal identificador de veículo',
            'embriaguez':3, # 'Embriaguez ao volante',
            'volante':3,
            'direcao':3,#'Entregar direção à pessoa não habilitada',
            'velocidade':2, #'Velocidade incompatível',
            'transporte irregular':3, #'Transporte irregular de madeira',
            'acidente de transito':3,
            'cnh':3,
            'lesao corporal':2,
            'transporte de coisas':2,
            'influencia de alcool':4,#'direção sob influência de álcool',
            'direcao perigosa':3, 
            'disputar corrida':3, 
            'manobra perigosa':3, 
            'racha':3, 
            'fraude':3,
            'lei antitoxicos':4,
            'quadrilha':4,
            'contrabando':4,
            'descaminho':3,
            'receptacao':4,
            'documento falso':4,
            'estelionato':2,
            'falsificacao':3,
            'falsidade ideologica':3,
            'enriquecimento':1, #Enriquecimento sem causa
            'fuga':4,
            'associacao criminosa':4,
               }


    keywords_criminal = [unidecode.unidecode(strings).lower() for strings in criminal.keys()]
    data = data.loc[(data['MainSubject'].str.lower().str.contains('|'.join(keywords_criminal), na=False))]

    return data, keywords_criminal, criminal

def weightCounter(rows, processKeyWordsdict):
    """
    Calcula o peso total das palavras em uma linha e a contagem de palavras com cada peso.

    Args:
        rows (pd.Series): Uma linha de um DataFrame.
        process_keywords_dict (dict): Dicionário com as palavras e seus respectivos pesos.

    Returns:
        pd.Series: Uma série com o peso total das palavras e a contagem de palavras com cada peso.
    """
    # inicializar o dicionário de contagem com zeros para cada peso
    count_weights = {weight: 0 for weight in set(processKeyWordsdict.values())}
    FinalValue = 0
    # percorrer todas as palavras e atualizar a contagem para cada peso correspondente
    for word in processKeyWordsdict.keys():
        if rows[word]:
            weight = processKeyWordsdict[word]
            FinalValue += weight
            count_weights[weight] += 1
    # retornar o valor final e a contagem de palavras com cada peso
    return pd.Series({'FinalValue': FinalValue, **count_weights})

def createFeatures(data: pd.DataFrame, processKeyWords: List[str]) -> pd.DataFrame:
    """
    Cria features booleanas baseadas em palavras-chave.

    Args:
        data: O dataframe de entrada.
        keywords: Uma lista de palavras-chave para criar as features.

    Returns:
        Um novo dataframe com as features criadas.
    """
    df = data.copy()

    for words in processKeyWords:
        df[words] = False
        df.loc[df['MainSubject'].str.lower().str.contains(words), words] = True

    for words in processKeyWords:
        df[words] = df[words].astype(int)

    df_final = df.fillna(0)

    return df_final.drop(columns='MainSubject')

def rowAtualizer(data):
    """
    Atualiza os valores das colunas do DataFrame de acordo com algumas condições pré-definidas.

    Args:
        data (pd.DataFrame): DataFrame com as informações a serem atualizadas.

    Returns:
        pd.DataFrame: DataFrame com as informações atualizadas.
    """

    df = data.copy()

    if df['transito'] and df['homicidio'] and df['contra a vida']:
        df['homicidio'] = 0
        df['contra a vida'] = 0

    if df['transito'] and df['acidente de transito']:
        df['transito'] = 0

    if df['lesao corporal'] and df['transito']:
        df['lesao corporal'] = 0

    if df['lesao corporal'] and df['veiculo']:
        df['lesao corporal'] = 0

    if df['homicidio'] and df['contra a vida']:
        df['contra a vida'] = 0

    if df['homicidio'] and df['veiculo']:
        df['veiculo'] = 0

    if df['homicidio'] and df['transito']:
        df['homicidio'] = 0

    if df['contra a vida'] and df['transito']:
        df['contra a vida'] = 0

    if df['embriaguez'] and df['volante']:
        df['embriaguez'] = 0

    if df['direcao'] and df['veiculo']:
        df['direcao'] = 0

    if df['influencia de alcool'] and df['veiculo']:
        df['veiculo'] = 0

    if df['contrabando'] and df['descaminho']:
        df['contrabando'] = 0

    if df['medidas protetivas'] and df['maria da penha']:
        df['medidas protetivas'] = 0

    if df['furto'] and df['roubo']:
        df['furto'] = 0

    if df['furto'] and df['veiculo']:
        df['veiculo'] = 0

    if df['transito'] and df['veiculo']:
        df['veiculo'] = 0

    if df['sistema nacional de armas'] and df['porte ilegal de arma']:
        df['sistema nacional de armas'] = 0

    if df['corrupcao'] and df['corrupcao de menores']:
        df['corrupcao'] = 0

    if df['lei antitoxicos'] and df['trafico']:
        df['lei antitoxicos'] = 0

    return df

def totalFeaturesCreator(data: pd.DataFrame) -> pd.DataFrame:
    """Cria uma nova coluna 'TotalFeatures' com a soma dos valores das colunas selecionadas.

    Args:
        data (pd.DataFrame): O conjunto de dados que será utilizado.

    Returns:
        pd.DataFrame: O conjunto de dados com a nova coluna adicionada.
    """
    data['TotalFeatures'] = data.loc[:,data.columns[-66:-5]].sum(axis=1)

    return data

def timeDecayParameter(data: pd.DataFrame, target) -> pd.DataFrame:
    """Calcula para cada linha do conjunto de dados um parâmetro de decaimento de tempo baseado em uma função de decaimento exponencial inversa para diferença em anos.
     O parâmetro será maior para datas mais recentes e menor para datas mais antigas. Além disso, o parâmetro de decaímento de tempo será proporcional a gravidade do processo:
     processos classificados com gravidade 1 terão um decaímento no tempo mais acentuado do que aqueles classificados com gravidade 4, por exemplo.

    Args:
        data (pd.DataFrame): O conjunto de dados que será utilizado.

    Returns:
        pd.DataFrame: O conjunto de dados com as colunas 'dev_date', 'timedelta' e 'time_decay' adicionadas.
    """
    df = data.copy()
    
    today = pd.Timestamp.now()
    

    date_columns = ['PublicationDate', 'NoticeDate', 'RedistributionDate']
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    # criar uma nova coluna de data e preencher seus valores como nulos
    df['DevDate'] = np.nan
    # substituir os valores nulos pela menor data entre as colunas de publication, notive e redistribution
    df['DevDate'] = df[['PublicationDate', 'NoticeDate', 'RedistributionDate']].min(axis=1)
    df['DevDate'] = df['DevDate'].where(df['DevDate'] != '0001-01-01T00:00:00', np.nan)
    df['DevDate'] = df['DevDate'].fillna(today)
    # utilizar a coluna LawsuitAge como coluna para calcular o parâmetro de tempo. Quanto essa coluna vier com valores negativos
    # substituir pela diferença da data de hoje com a data da coluna dev_date
    df['TimeDelta'] = np.where(df['LawsuitAge'] < 0, (today - df['DevDate']).dt.days, df['LawsuitAge'])
    df['TimeDelta'] = np.where(df['TimeDelta'] < 0, 0, df['TimeDelta'])
    # criar quatro parâmetros de decaimento de tempo. Cada um desses parâmetros será utilizado de acordo com os pesos dos processos.

    df['TimeDecay1'] = 1 / (1 + (df['TimeDelta'] / 365 / 10))
    df['TimeDecay2'] = 1 / (1 + (df['TimeDelta'] / 365 / 15))
    df['TimeDecay3'] = 1 / (1 + (df['TimeDelta'] / 365 / 20))
    df['TimeDecay4'] = 1 / (1 + (df['TimeDelta'] / 365 / 25))
    
    if target:

        df = df[['person_uuid', 'MainSubject', 'LawsuitAge', 'TimeDelta',
             'TimeDecay1', 'TimeDecay2', 'TimeDecay3', 'TimeDecay4']]
        df = df.drop_duplicates()

        return df
    
    else:
        
        df = df[['document', 'MainSubject', 'LawsuitAge', 'TimeDelta',
             'TimeDecay1', 'TimeDecay2', 'TimeDecay3', 'TimeDecay4']]
        df = df.drop_duplicates()

        return df

def finalAggregation(data: pd.DataFrame, processKeyWordsdict, target) -> pd.DataFrame:
    """Aplica o parâmetro de decaimento temporal correto para cada processo e agrupa as entradas para cada motorista.

    Args:
        data (pd.DataFrame): O conjunto de dados que será utilizado.

    Returns:
        pd.DataFrame: O conjunto de dados com as features que serão utilizadas no calculo com a função sigmoid.
    """
    df = data.copy()
    
    df = pd.concat([df, df.apply(lambda x: weightCounter(x, processKeyWordsdict), axis=1)], axis=1)
        
    df['ClassOne'] = df[1] * df['TimeDecay1']
    df['ClassTwo'] = df[2] * df['TimeDecay2']
    df['ClassThree'] = df[3] * df['TimeDecay3']
    df['ClassFour'] = df[4] * df['TimeDecay4']
    
    df2 = df.copy()
    df2.drop_duplicates(inplace=True)
    
    df2['TotalFeatures'] = df2.loc[:,df2.columns[-71:-9]].apply(lambda row: (row != 0).sum(), axis=1)
    
    if target:
        df2 = df2[['person_uuid', 'TotalFeatures']]
        df2 = df2.groupby('person_uuid', as_index=False).sum()

        df = df[['person_uuid', 'ClassOne', 'ClassTwo', 'ClassThree', 'ClassFour']]

        df = df.groupby('person_uuid', as_index=False).sum()

        return df.merge(df2)
    
    else:
        df2 = df2[['document', 'TotalFeatures']]
        df2 = df2.groupby('document', as_index=False).sum()

        df = df[['document', 'ClassOne', 'ClassTwo', 'ClassThree', 'ClassFour']]

        df = df.groupby('document', as_index=False).sum()

        return df.merge(df2)

def processJson(data):
    """
    Essa função recebe um objeto JSON com dados de motoristas, proprietários de veículos e proprietários de RNTRC,
    normaliza os dados
    
    Args:
    - data: objeto JSON
    
    Returns:
    - process_df: pandas DataFrame contendo as informações extraídas do objeto JSON
    """
    process_df = pd.json_normalize(data, record_path = ['process', ['ResponseParties']], meta=['person_uuid', 'document', 'name',
        ['process', 'Number'],
        ['process', 'CourtType'],
        ['process', 'MainSubject'],
        ['process', 'PublicationDate'],
        ['process', 'NoticeDate'],
        ['process', 'RedistributionDate'],
        ['process', 'LawsuitAge'],
       ], errors='ignore')

    process_df = process_df.rename(columns=lambda x:x.replace('process.', '') if x.startswith('process.') else x)
    process_df = process_df.rename(columns=lambda x:x.replace('PartyDetails.', '') if x.startswith('PartyDetails.') else x)
    process_df = process_df.apply(lambda x: x.astype(str).str.lower())
    # Alguns processos vem sem a informação de ResponseParties. No caso de o motorista ter apenas um processo sem a informação de ResponseParties, retorna um dataframe vazio. A etapa abaixo garante o funcionamento da função preProcessing
    if process_df.empty:
        columns = ['Doc', 'IsPartyActive', 'Name', 'Polarity', 'Type', 'LastCaptureDate', 'SpecificType', 'person_uuid', 'document', 'name', 'Number', 'CourtType', 'MainSubject', 'PublicationDate', 'NoticeDate', 'RedistributionDate', 'LawsuitAge']
        process_df = pd.DataFrame(columns=columns)
        process_df = process_df.astype(object)
        process_df.loc[0] = 0
        process_df['person_uuid'] = data['person_uuid']
        process_df['document'] = data['document']
        process_df['name'] = data['name']
        process_df = process_df.astype(str).apply(lambda x: x.str.lower() if x.name not in ['person_uuid', 'document', 'name'] else x)

    return process_df


def convert_to_int_if_not_null(x):
    """
    Função para converter os elementos x para inteiros, exceto aqueles que são nulos ('none').
    
    Args:
    - x: matriz numpy de entrada
    
    Returns:
    - x: matriz numpy com elementos convertidos para inteiros se não forem nulos, caso contrário mantém os elementos como nulos
    """
    x = np.where(x == 'none', None, x)
    x = np.vectorize(lambda v: int(v) if v is not None else v)(x)
    return x

def preProcessing(data, target = None):
    
    data['LawsuitAge'] = data['LawsuitAge'].apply(convert_to_int_if_not_null)
    
    data = courtSelector(data)
    if data.empty:
        return pd.DataFrame()
    
    data = civilSelector(data)
    if data.empty:
        return pd.DataFrame()
    
    data = excludeKeywords(data)
    if data.empty:
        return pd.DataFrame()
    
    data, processKeyWords, processKeyWordsdict = subjectSelector(data)
    
    data = typeSelector(data)
    if data.empty:
        return pd.DataFrame()

    df = timeDecayParameter(data, target)
    df = createFeatures(df, processKeyWords)
    df = df.apply(rowAtualizer, axis=1)
    df = finalAggregation(df, processKeyWordsdict, target)

    return df
