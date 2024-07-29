from openai import OpenAI
import time
from dotenv import load_dotenv
import os
from retry import retry

class ObservationFieldScanner:
    
    def __init__(self, delay_in_seconds: float = 1):
        self.prompt = self.__observation_field_prompt()
        self.delay = delay_in_seconds
        load_dotenv()  
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:  
            self.client = OpenAI(api_key=api_key)
        else:
            raise ValueError("OPENAI_API_KEY not found. Please ensure it's set in your environment.")
        
    def __observation_field_prompt(self, ):
        """ Generate a prompt for extracting informations based on the observation field of the freight.
        Returns:
            str: A textual prompt tailored for the task of extracting relevant information from the
             observation field of a freight item.
        """
        
        return '''Trabalho em uma empresa de fretes, cujo sistema permite que empresas insiram informações adicionais do frete em um campo de texto livre durante o cadastro do frete. Sua tarefa é analisar, organizar, extrair informações desse campo e categorizá-las de acordo com os outputs de exemplo e as diretrizes abaixo. As informações que você deve coletar incluem:
1: total_entregas: Quantas entregas que o motorista deverá fazer.
2: total_coletas: Quantas coletas o motorista deverá fazer.
3: datas (3.1: data_coleta, 3.2: data_entrega, 3.3: restricoes_horario): Datas de carregamento e entrega. preencha as datas no formato 'YYYY-MM-DD'. Para palavras chave como 'hoje', 'amanhã', não substitua a data, matenha a palavra chave. Para o campo restricoes_horario você deve preencher informações relativas à restrições de horário que você encontrar. Alguns exemplos são "necessário coletar e entregar hoje até às 21:00" ou "entregar amanhã até as 13".
4: quantidade: Identifique informações da quantidade de itens, como "2 caixas", "10 pallets", "5 volumes". Abreviações de caixa: cx, cxs... Pallets pode aparecer escrito como palets, paletes, pellets... 
5: caracteristicas_carga (5.1: subunidades, 5.2: volume, 5.3: peso, 5.4: largura, 5.5: comprimento, 5.6: altura): 
NÃO confunda com as informações da carroceria. PREENCHA O CAMPO "VOLUME" APENAS SE A INFORMAÇÃO CONTIVER MEDIDAS FÍSICAS DE VOLUME (METROS CÚBICOS, LITROS...) Mantenha as unidades de medidas.
Se no texto aparecer 4 volumes medidas 2.70 a x 0.80 l x 1.40 c, 4 volumes deve ser preenchido subitem unidades. 2.7 é altura, 0.8 largura e 1.4 é comprimento. O subitem volume deve ser mantido nulo. 
6: tipo_carga (6.1: tipo_carga, 6.2: precisa_mopp, 6.3: carga_complemento): Para o campo 6.1, preencher Carga seca, líquida, frigorífica, viva ou perigosa. APENAS ESSAS CATEGORIAS, NAO CRIE NOVAS PALAVRAS. Não havendo menção do tipo de carga, manter como nulo. Campo 6.2: MOPP é um curso de especialização para movimentação operacional de produtos perigosos. Nos casos em que estiver escrito explicitamente "precisa mopp", preencher 6.2 como true, false caso contrário. Considere as palavras 'mop', 'mopp' e 'mope' como tendo o mesmo significado. Complemento de frete é quando o frete oferecido não irá ocupar o espaço disponível para transporte completamente. carga_complemento deve ser preenchido com true quando houver a palavra chave complemento. Se estiver escrito "carga completa", carga_complemento deve ser preenchido com false.
7: carga_palletizada: Retorna true para carga palletizada. False caso contrário.
8: caracteristicas_caminhao (8.1: tipo_veiculo, 8.2: carroceria, 8.3: eixos, 8.4: ano_minimo, 8.5: idade_maxima, 8.6: comprimento_minimo, 8.7: altura_minima, 8.8: largura_minima, 8.9: acessorios): Ano mínimo do caminhão ou idade máxima (se fornecido o ano, calcule o tempo em anos a partir da data de hoje). Tipo necessário de veículo (vlc, utilitário, fiorino, van, HR, vuc, 3/4, toco, truck, bi-truck, carreta, carreta ls...) e de carroceria (bau, sider, caçamba basculante, porta container, aberto grade baixa, canavieiras, carrega tudo, florestal, boiadeiro, refrigerado (frigorifico), tanque, bitrem, rodotrem, tritrem, romeu e julieta, cegonha, graneleiro, silo, plataforma, betoneira, munk, rollon...). Dimensões mínimas do caminhão (largura, altura e comprimento). Acessórios necessários (lona, madeirite, corda, cintas, catracas, forro sem odor... AQUI NÃO ENTRA INFORMAÇÕES DE PAGAMENTO)
9: Itinerário (9.1: cidade_origem, 9.2: uf_origem, 9.3: cidade_destino, 9.4: uf_destino): Cidades e estados de origem, destino, e intermediárias. Havendo mais que uma cidade, preencher na forma de lista. Aqui deve entrar apenas nomes de cidades e siglas de estados.
10: Combustível: Se a empresa paga o combustível ou oferece algum desconto (apenas preencher true ou false). A entrega ser em posto de combustível não significa benefícios de combustível (deve ser preenchido como false). A informação pode vir em litros de combustível, ex: "frete r 14.850,00 mais 1.223 litros de diesel mais pedágios.". Nesse caso, combustível deve ser preenchido como true e essa informação de volume NÃO é referente à carga não deve ser preenchida em "caracteristicas_carga".
11: pedagio (11.1: tag_pedagio, 11.2: empresas_tag): Identifique apenas menções indicando a necessidade da tag de pedágio. 'Tag' deve ser entendido como relacionado ao pedágio somente se mencionado junto ou em contexto claro com as empresas listadas para pedágio (ex:  Sem parar, veloe, conectcar, c6 tag, move mais, zul+ (zul+ digital), tag itau, ultrapasse, mercado pago, inter tag, sicredi, via facil). Não utilize palavras diferentes das desta lista. Subcampo 11.1: Preencher com true true se precisar ter tag de pedágio, false caso contrário. O termo TAG pode ser APENAS utilizado no contexto de pedágio.
12: livre_carga_descarga: Existem três possibilidades de resposta: True (o motorista não precisa carregar ou descarregar), False (o motorista precisa carregar/descarregar, null: não há informação.
13: rastreador (13.1: precisa_rastreador, 13.2: teclado_marcas_rastreador): Quando analisar informações sobre rastreadores, concentre-se exclusivamente em menções que especificam a necessidade de um rastreador, incluindo se é necessário um teclado e as marcas permitidas 
(ex: autotrac, ominilink, onix (onixsat), positron, sascar, ravex, sighra).
Utilize apenas essas marcas. Ignore menções a tecnologias ou dispositivos que não sejam claramente identificados como parte do sistema de rastreamento. Para o subcampo 7.1, preencher true, false ou null.
14: pagamento (14.1: valor_frete, 14.2: adiantamento, 14.3: percentual_adiantamento, 14.4: forma_pagamento, 14.5: pagamento_saldo": ", 14.6: agenciamento): Ao analisar informações de pagamento, se atente a casos em que há adiantamento (preencher 13.2 (adiantamento) como true ou false). Adiantamento pode estar explicito ou deve ser subentendido em casos como "pagamento via pix 70/30", significando haver 70% de adiantamento. Saldo deve entrar APENAS no contexto de pagamento. O preenchimento da forma de pagamento deve levar em consideração palavras como "pix, a vista, em conta" ou também casos em que há menção de empresas específicas: "repom, pamcard, valecard". Apenas preencher forma_pagamento se houver menção explicita da forma de pagamento. Saldo é o valor que será pago após a conclusão do serviço. Alguns textos mencionaram etapas a serem cumpridas para o pagamento do saldo, como envio de comprovantes. Preencha o campo agenciamento com true ou false apenas para menções explicitas de haver ou não pagamento de agenciamento, se não houver informação, deixar como nulo. Palavras como seguradora  e gerenciadora NÃO devem ser utilizadas para o contexto de agenciamento.

Mantenha a consistência com o assunto de cada campo. ASSEGURE A FORMATAÇÃO CORRETA DO OUTPUT E MANTENHA TODAS OS CAMPOS SUGERIDOS, NÃO CRIE NOVOS CAMPOS ALÉM DOS PRESENTES NOS EXEMPLOS E PREENCHA COM NULOS AS INFORMAÇÕES FALTANTES. 

Abaixo seguem exemplos de observações e a estrutura do output:
- Exemplo 1: 'carga complemento, carrega hoje, entrega sexta-feira em São Paulo até as 21 horas. 22 volumes 140 kg 270 cubicos, precisa ser refrigerado ano 2010 diante. 11.5 mts de comprimento livre por dentro. rastreador com teclado para macro (onix, ominilink, sascar e autotrac). Precisa mopp. Necessário ter tag do sem parar ou conectcar. Livre de carga e descarga. Pagamento via pix 70/30 e saldo após envio dos canhotos via correios ou pessoalmente. Paga agenciamento. Necessario genciadoras ok'
- Output 1: {{
    "total_entregas": "1 entrega",
    "total_coletas": "1 coleta",
    "datas": [{{
        "data_coleta": "2024-03-13",
        "data_entrega": "2024-03-15",
        "restricoes_horario": ["entrega até as 21 horas"]
    }}],
    "quantidade": [{{
       "caixas": null,
       "pallets": null,
       "unidades": "22 volumes"
   }}],
    "caracteristicas_carga": [{{
      "subunidades": "22 volumes",
      "volume": "270 m³",
      "peso": "140 kg",
      "largura": null,
      "comprimento": null,
      "altura": null
   }}],
    "tipo_carga": [{{
        "tipo_carga": "frigorífica",
        "precisa_mopp": true,
        "carga_complemento": true
    }}],
    "carga_palletizada":false,
    "caracteristicas_caminhao": [{{
       "tipo_veiculo": null,
       "carroceria":  "refrigerado",
       "eixos": null,
       "ano_minimo": "2010",
       "idade_maxima": "14 anos",
       "comprimento_minimo": "11.5 metros",
       "altura_minima": null,
       "largura_minima": null,
       "acessorios": null
   }}],
    "itinerario": [{{
       "cidade_origem": null,
       "uf_origem": null,
       "cidade_destino": "são paulo",
       "uf_destino": "sp"Analise o texto e preencha o JSON de acordo com os exemplos de output:
       }}],
    "combustivel": null,
    "pedagio": [{{
       "precisa_tag": true,
       "empresas_tag": ["sem parar", "conectcar"]
       }}],
    "livre_carga_descarga": true,
    "rastreador": [{{
       "rastreador": true,
       "especificidades_rastreador": "com teclado para macro (onix, ominilink, sascar e autotrac)"
       }}],
    "pagamento": [{{
        "valor_frete": null,
        "adiantamento": true,
        "percentual_adiantamento": "70%",
        "forma_pagamento": "pix",
        "pagamento_saldo": "saldo após envio dos canhotos via correios ou pessoalmente",
        "agenciamento": true
    }}]
   }}
--------
- Exemplo 2: 'Carga completa. Medidas: 2,30 de comprimento x 1,50 de altura x 1,20 de largura 2,30 de comprimento x 1,50 de altura x 0,40 de largura. nao cobramos agenciamento. Pagamento na entrega, sem combustível. Frete 4.700,00 80/20 no pix livre de agenciamento. carreta bau ou sider de 14 x 280 livre de altura aberto com lonas. veiculo de 2000 no máximo com pamcary ou bounny. precisa 20 madeirites e todas as rguas impecvel sem odor coletar amanhã. Precisa tag. Precisa descarregar.'
- Output 2: {{
    "total_entregas": "1 entrega",
    "total_coletas": "1 coleta",
    "datas": [{{
        "data_coleta": "2024-03-14",
        "data_entrega": null,
        "restricoes_horario": null
    }}],
    "quantidade": [{{
       "caixas": null,
       "pallets": null,
       "unidades": "2 unidades"
   }}],
    "caracteristicas_carga": [
    {{
      "subunidades": "1 unidade",
      "volume": null,
      "peso": null,
      "largura": "1.20",
      "comprimento": "2.30",
      "altura": "1.50"
    }},
    {{
     "subunidades": "1 unidade",
      "volume": null,
      "peso": null,
      "largura": "0.40",
      "comprimento": "2.30",
      "altura": "1.50"
    }}],
    "tipo_carga": [{{
        "tipo_carga": null,
        "precisa_mopp": null,
        "carga_complemento": false
    }}],
    "carga_palletizada":false,
    "caracteristicas_caminhao": [{{
        "tipo_veiculo": null,
        "carroceria": "carreta bau ou sider",
        "eixos": null,
        "ano_minimo": "2004",
        "idade_maxima": "20 anos",
        "comprimento_minimo": "14 metros",
        "altura_minima": "2.8 metros",
        "largura_minima": null,
        "acessorios": "20 madeirites e todas as réguas impecáveis sem odor"
   }}],
    "itinerario": [{{
       "cidade_origem": null,
       "uf_origem": null,
       "cidade_destino": null,
       "uf_destino": null
       }}],
    "combustivel": false,
    "pedagio": [{{
       "precisa_tag": true,
       "empresas_tag": null
       }}],
    "livre_carga_descarga": false,
    "rastreador": [{{
       "rastreador": false,
       "especificidades_rastreador": null
       }}],
    "pagamento": [{{
        "valor_frete": "4.700,00",
        "adiantamento": true,
        "percentual_adiantamento": "80%",
        "forma_pagamento": "pix",
        "pagamento_saldo": null,
        "agenciamento": false
    }}]
   }}
--------
- Exemplo 3: 'buonny entrega em 2 cidades: 18 caixas Caconde SP 68 caixas Bauru SP. Necessário carregar 15/03 até as 8 horas. Carga seca. Precisa rastreador com teclado. Ano mínimo caminhão: 2010. Saldo com foto do código de rastreio.'
Output 3: {{
   "total_entregas": "3 entregas",
   "total_coletas": "1 coleta",
   "datas": [{{
        "data_coleta": "2024-03-15",
        "data_entrega": null,
        "restricoes_horario": ["carregar 15/03 até as 8 horas"]
    }}],
   "quantidade": [{{
       "caixas": "86 caixas",
       "pallets": null,
       "unidades": null
   }}],
  "caracteristicas_carga": [
    {{
     "subunidades": "18 caixas",
      "volume": null,
      "peso": null,
      "largura": null,
      "comprimento": null,
      "altura": null
    }},
    {{
     "subunidades": "68 caixas",
      "volume": null,
      "peso": null,
      "largura": null,
      "comprimento": null,
      "altura": null
    }}],
    "tipo_carga": [{{
        "tipo_carga": "seca",
        "precisa_mopp": null,
        "carga_complemento": null
    }}],
   "carga_palletizada": false,
   "caracteristicas_caminhao": [{{
        "tipo_veiculo": null,
        "carroceria": null,
        "eixos": null,
        "ano_minimo": "2010",
        "idade_maxima": "24 anos",
        "comprimento_minimo": null,
        "altura_minima": null,
        "largura_minima": null,
        "acessorios": null
   }}],
   "itinerario": [{{
       "cidade_origem": null,
       "uf_origem": null,
       "cidade_destino": ["caconde", "bauru"],
       "uf_destino": "sp"
       }}],
   "combustivel": null,
   "pedagio": [{{
       "precisa_tag": false,
       "empresas_tag": null
       }}],
   "livre_carga_descarga": null,
   "rastreador": [{{
       "rastreador": true,
       "especificidades_rastreador": "com teclado"
   }}],
    "pagamento": [{{
        "valor_frete": null,
        "adiantamento": null,
        "percentual_adiantamento": null,
        "forma_pagamento": null,
        "pagamento_saldo": "com foto do código de rastreio",
        "agenciamento": null
    }}]
   }}
'''
    
    @retry(exceptions=(Exception,), tries=2, delay=1)  
    def observation_field(self, OBS: str):
        """ Generates the outputs of the observation field. """
        time.sleep(self.delay)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": self.prompt},
                    {"role": "user", "content": OBS}
                ],
                temperature=0,
                max_tokens=2000,
                top_p=0.2,
                frequency_penalty=0,
                presence_penalty=0
            )
                
            # Adapt to the new response format if necessary
            return response.choices[0].message.content
        except Exception as e:  # Update to catch specific exceptions if necessary
            print(f"An error occurred: {e}")