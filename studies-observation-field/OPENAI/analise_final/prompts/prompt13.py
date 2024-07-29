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

1: gerenciadoras_de_risco (1.1: necessidade_gr, 1.2: empresas_gr): Para o campo gerenciadoras_de_risco, siga estas instruções: Verifique se o texto menciona a necessidade de uma gerenciadora de risco ou seguradora. Identifique se nomes de empresas específicas de gerenciamento de risco estão presentes, considerando erros comuns de ortografia. Se qualquer nome de empresa for mencionado, marque necessidade_gr como true e liste a empresa em empresas_gr. Preste atenção especial a palavras-chave como 'segurado', 'Buonny', 'Pamcary', 'Skymark', 'Guep', 'Raster', 'Apisul', 'Gertran', 'Telerisco', 'Opentech', 'Inova', etc. Por exemplo, se o texto diz 'buonny 12 volumes', necessidade_gr deve ser true e empresas_gr deve incluir 'Buonny'."
2: ear_carteira: No contexto de logística, a sigla "ear" se refere à "Exerce Atividade Remunerada" e é adicionada à carteira de motorista (CNH) de quem indica que pode usar seu veículo para fins profissionais. Alguns fretes vão mencionar que é necessário ter "ear" na carteira. Se você identificar essa informação, preencha o campo ear_carteira como true e false, caso contrário.
Mantenha a consistência com o assunto de cada campo. ASSEGURE A FORMATAÇÃO CORRETA DO OUTPUT E MANTENHA TODAS OS CAMPOS SUGERIDOS, NÃO CRIE NOVOS CAMPOS ALÉM DOS PRESENTES NOS EXEMPLOS E PREENCHA COM NULOS AS INFORMAÇÕES FALTANTES. 
3: cnpj: Verifique se o texto menciona a exigência de um CNPJ. Marque true para expressões como 'necessário CNPJ', 'exige-se CNPJ', 'CNPJ obrigatório', entre outras variações que sinalizem essa exigência. Marque false caso contrário.
4: vinculacao_antt (4.1: antt_cpf, 4.2: antt_cnpj): Para o campo vinculacao_antt, investigue se o texto menciona a necessidade de a autorização da ANTT estar vinculada especificamente a um CPF ou a um CNPJ. Marque antt_cpf como true se a vinculação à antt for especificamente com cpf, e antt_cnpj como true for exigido um cnpj vinculado à antt. Se não houver menção à necessidade de vinculação, ambos os subcampos devem ser marcados como false. Se antt_cpf for marcado como true, antt_cnpj deve ser false, e vice-versa, refletindo a exclusividade da vinculação documental.
5: transferencia_filial: Identifique se o texto menciona uma transferência entre filiais. Se sim, marque e_transferencia como true; caso contrário, false. Casos como "entregar na filial" não indica que transferencia_filial deve ser true. 
6: logistica_reversa (6.1: e_logistica_reversa): Verifique se há menção a logística reversa. Se afirmativo, marque e_logistica_reversa como true; se não, false.
7: agregamento: Analise o texto para identificar menções que sugiram agregamento de transportadores ou parcerias, incluindo termos como "agregamos", "contrata-se para safra", "agregando", "operação dedicada", "parceria de sucesso", "fazer parte de nossa frota", "operação e-commerce", "arrendamento",  rota fixa", "segunda a sexta", "trabalho semanal", "recebe mensal" assim como a menção a empresas específicas que podem indicar agregamento, como "Shopee", "Mercado Livre", "Amazon". Se qualquer dessas expressões, contextos ou menções a essas empresas estiver presente, marque e_agregamento como true; caso contrário, false. A inclusão de empresas específicas serve como um forte indicativo de oportunidades de agregação e parcerias.
8: excessos_carga (8.1: tem_excesso, 8.2: tipo_excesso, 8.3: licenca_excesso): Analise o texto para identificar se há menções a cargas com excesso de medidas (largura, altura, peso). Marque tem_excesso como true se o texto indicar a presença de cargas com excesso e detalhe em tipo_excesso quais são os excessos mencionados (ex: "lateral 3.20 metros", "excesso de altura", "excesso de largura"). Para licenca_excesso, marque como true se há menção à necessidade de obter licenças específicas para o transporte dessas cargas (ex: "vai tirar licença", "licença de excesso", "obrigatório ter placa").

Abaixo seguem exemplos de observações e a estrutura do output:
- Exemplo 1: 'entrega em São Paulo 22 volumes 140 kg 270 cubicos, rastreador com teclado para macro (onix, ominilink, sascar e autotrac). Necessário ter tag do sem parar ou conectcar. Pagamento via pix 70/30 e saldo após envio dos canhotos via correios ou pessoalmente. precisa ter cnpj.  não coloca excesso de peso'
- Output 1: {{
    "gerenciadoras_de_risco": [{{
        "necessidade_gr": true
        "empresas_gr": null
        }}],
    "ear_carteira": true,
    "cnpj": true,
    "vinculacao_antt": [{{
        "antt_cpf": false,
        "antt_cnpj": false
        }}],
    "transferencia_filial": false,
    "logistica_reversa": false,
    "agregamento": false,
    "excessos_carga": [{{
        "tem_excesso": false,
        "tipo_excesso": null,
        "licenca_excesso": null
        }}]
   }}
--------
- Exemplo 2: 'logistica reversa. Medidas: 2,30 de comprimento x 1,50 de altura x 1,20 de largura 2,30 de comprimento x 1,50 de altura x 0,40 de largura. nao cobramos agenciamento. Pagamento na entrega, sem combustível. Frete 4.700,00 80/20 no pix livre de agenciamento. carreta bau ou sider de 14 x 280 livre de altura aberto com lonas. veiculo de 2000 no máximo com pamcary ou bounny. precisa 20 madeirites e todas as rguas impecvel sem odor coletar hoje. Precisa tag. Precisa descarregar. antt jurídica'
- Output 2: {{
    "gerenciadoras_de_risco": [{{
        "necessidade_gr": true,
        "empresas_gr": ["pamcary", "bounny"]
        }}], 
    "ear_carteira": false,
    "cnpj": false,
    "vinculacao_antt": [{{
        "antt_cpf": false,
        "antt_cnpj": true
        }}],
    "transferencia_filial": false,
    "logistica_reversa": true,
    "agregamento": false,
    "excessos_carga": [{{
        "tem_excesso": false,
        "tipo_excesso": null,
        "licenca_excesso": null
        }}]
        }}
--------
- Exemplo 3: 'buonny. transferencia entre filiais. excesso lateral de 3m.'
Output 3: {{
    "gerenciadoras_de_risco": [{{
        "necessidade_gr": true
        "empresas_gr": ["buonny"]
        }}],
    "ear_carteira": false,
    "cnpj": false,
    "vinculacao_antt": [{{
        "antt_cpf": false,
        "antt_cnpj": false
        }}],
    "transferencia_filial": true,
    "logistica_reversa" true,
    "agregamento": false,
    "excessos_carga": [{{
        "tem_excesso": true,
        "tipo_excesso": "excesso lateral de 3m",
        "licenca_excesso": null
        }}]
   }}
-------
- Exemplo 4: 'cargill - filial campo novo. operaçao dedicada, frete todo dia. carreta precisa ter licença de excesso de largura'
Output 3: {{
    "gerenciadoras_de_risco": [{{
        "necessidade_gr": false
        "empresas_gr": null
        }}],
    "ear_carteira": false,
    "cnpj": false,
    "vinculacao_antt": [{{
        "antt_cpf": false,
        "antt_cnpj": false
        }}],
    "transferencia_filial": false,
    "logistica_reversa" false,
    "agregamento": true,
    "excessos_carga": [{{
        "tem_excesso": true,
        "tipo_excesso": "excesso de largura",
        "licenca_excesso": true
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
                max_tokens=1600,
                top_p=0.2,
                frequency_penalty=0,
                presence_penalty=0
            )
                
            # Adapt to the new response format if necessary
            return response.choices[0].message.content
        except Exception as e:  # Update to catch specific exceptions if necessary
            print(f"An error occurred: {e}")