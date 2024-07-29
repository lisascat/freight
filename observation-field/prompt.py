import openai
import time
from dotenv import load_dotenv
import os
import asyncio
from retry import retry

class ObservationFieldScanner:
    """
    Classe responsável por, a patir da API da OpenAI, escanear e extrair informações do texto presento no campo de observação presente
    no cadastro do frete 

    Utiliza o modelo GPT-3.5 para processar e extrair informações físicas do frete a partir de textos de campo livre. Implementa o 
    reenvio automático e gestão de timout para as chamadas à API.

    Attributes:
        prompt (str): Texto inicial configurado para orientar o modelo GPT-3.5 em suas respostas.
        delay (float): Tempo de espera (em segundos) antes de cada tentativa de envio da requisição.
        timeout (float): Tempo máximo (em segundos) para a resposta da API antes de um timeout.
        max_retries (int): Número máximo de tentativas para cada requisição.
        retry_delay (float): Tempo de espera (em segundos) entre tentativas consecutivas.

    Methods:
        observation_field(obs: str):
            Processa o campo de observações para extrair informações usando a API da OpenAI.
    """

    def __init__(self, delay_in_seconds: float=1, timeout_seconds: float=10, max_retries: int = 2, retry_delay: float = 1):
        """
        Inicializa uma instância de ObservationFieldScanner com os parâmetros necessários para o controle de requisições.

        Parameters:
            delay_in_seconds (float): Tempo de espera antes de cada requisição.
            timeout_seconds (float): Tempo limite para espera da resposta da API.
            max_retries (int): Número máximo de tentativas de requisição.
            retry_delay (float): Tempo de espera entre tentativas falhas.
        """

        self.prompt = self.__system_ner()
        self.delay = delay_in_seconds
        self.timeout = timeout_seconds
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
        else:
            raise ValueError("OPENAI_API_KEY not found. Please ensure it's set in your environment.")

    def __system_ner(self, ):
        """
        Define o prompt inicial usado para configurar a sessão de chat com o modelo GPT-3.5.

        Returns:
            str: O prompt que direciona o modelo para focar na extração de informações específicas de frete.
        """

        return '''Você é um sistema de reconhecimento de entidades nomeadas (NER) em uma empresa que conecta o frete de outras empresas a motoristas. Neste sistema, empresas podem adicionar informações sobre o frete em um campo de texto livre. Sua tarefa é extrair entidades específicas de informações físicas da carga do frete deste campo, conforme as definições e exemplos abaixo. Caso uma informação solicitada não seja encontrada, retorne null. Alguns textos podem não possuir nenhuma das entidades listadas.
Você deve extrair as informações:
num_itens: NÚMERO de itens da carga a ser entregues no frete. 
tipo_unidade_itens: Extraia a descrição da num_itens da carga a ser entregues no frete, como total de caixas, pallets e volumes. Algumas palavras podem conter erros ortográficos, ex: palletes, paletes, palets, palets...
peso: NÚMERO que representa o peso da carga. Números seguidos por "kg", "quilos", "kilos", "ton", "toneladas" ou outras unidades de medida de peso devem ser considerados como peso.
unidade_peso: unidade de medida do peso, como "kg" ou "tonelada".
comprimento: NÚMERO que representa o comprimento da carga. Essa informação pode vir explicita, mas, algumas vezes, pode estar implícita como comprimento da carreta ou baú, ou escrita de maneira similar a "adiciona 14 metros".
unidade_comprimento: unidade de medida do comprimento, como "m" ou "cm".
altura: NÚMERO que representa a altura da carga.
unidade_altura: unidade de medida da altura, como "m" ou "cm".
largura: NÚMERO que representa a largura da carga.
unidade_largura: unidade de medida da largura, como "m" ou "cm".
cubagem: Procure por informações de volume do frete que estejam EXPLICITAS. NÃO REALIZE CÁLCULOS.
unidade_cubagem: Extraia com atenção unidade de volume, tal como m3, m³, cúbico, metro cúbico e litros.
Instruções Especiais:
Quando as dimensões da carga são fornecidos em uma sequência, como "50x50x50", considere a ordem padrão como comprimento x largura x altura. Ignore palavras que destacam peças necessárias para o frete (cantoneira, madeirite, cinta, catrata...). 
Números ligados às palavras pagamento, adiantamento e saldo DEVEM ser ignorados: "80 de adiantamento" não condiz com nenhum campo a ser preenchido!!!
É CRUCIAL QUE AS INFORMAÇÕES SEJAM PRECISAS; PREFIRA RETORNAR NULO A FORNECER DADOS INCORRETOS.
ASSEGURE A FORMATAÇÃO CORRETA DO OUTPUT E MANTENHA TODAS OS CAMPOS SUGERIDOS. ASSEGURE O PREENCHIMENTO DOS CAMPOS DE ACORDO COM AS UNIDADES DE MEDIDAS.
Preste especial atenção em textos como 'carreta precisa de duas lonas 6m por 8': essas informaçãos descrevem itens necessários, as medidas não são relativas à carga do frete!!!
Preste especial atenção em textos como 'acima de 6mts carroceria': essa informação diz respeito ao veículo!!!!
Abaixo seguem os exemplo e a estrutura do output que você DEVE seguir.
- Exemplo 1: "adiantamento 80, 20kg, 1 cx 50x50x50 0,125 litros complemento"
- Output 1: {"num_itens": "1","tipo_unidade_itens": "cx", "peso": "20","unidade_peso": "kg","comprimento": "50","unidade_comprimento": null,"largura": "50","unidade_largura": null,"altura": "50","unidade_altura": null,"cubagem": "0,125","unidade_cubagem": "litros"}
- Exemplo 2: "2 entregas - carretas precisar ter no mínimo 12,5m de comprimento, sider acima de 85 m3 mais detalhaes entrar em contato"
- Output 2: {"num_itens": null,"tipo_unidade_itens": null,"peso": null,"unidade_peso": null,"comprimento": "12.5","unidade_comprimento": "m","largura": null,"unidade_largura": null,"altura": null,"unidade_altura": null,"cubagem": "5","unidade_cubagem": "m3"}
- Exemplo 3: "carreta de 5 eixos. dimensão: 2,50m de comprimento x 1,03m de largura x 0,42m de profundidade total: 1 volume dimensão: 1,50m de comprimento x 0,60m de largura x 0,45m de profundidade total: 1 volume"
- Output 3: [{"num_itens": "1","tipo_unidade_itens": "volume","peso": null,"unidade_peso": null,"comprimento": "2,50","unidade_comprimento": "m","largura": "1,03","unidade_largura": "m","altura": "0,42","unidade_altura": "m","cubagem": null,"unidade_cubagem": null},{"num_itens": "1","tipo_unidade_itens": "volume","peso": null,"unidade_peso": null,"comprimento": "1,50","unidade_comprimento": "m","largura": "0,60","unidade_largura": "m","altura": "0,45","unidade_altura": "m","cubagem": null,"unidade_cubagem": null}]
- Exemplo 4: "sider sem furos ter 14 cantoneiras de 1 metro + 4 chapatex, 4,50m³, peso 2 to, 10,00 x 3,00 x 2,50, decarregar em curitiba"
- Output 4: {"num_itens": null,"tipo_unidade_itens": null,"peso": "2","unidade_peso": "to","comprimento": "10,00","unidade_comprimento": null,"largura": "3,00","unidade_largura": null,"altura": "2,5","unidade_altura": null,"cubagem": "4,5","unidade_cubagem": "m³"}
- Exemplo 5: "sider. a peça ocupa 3 metros de carroceria, 105m cúbicos 31,500 kg"
- Output 5: {"num_itens": "1","tipo_unidade_itens": "peça","peso": "31,500","unidade_peso": "kg","comprimento": "3","unidade_comprimento": "metros","largura": null,"unidade_largura": null,"altura": null,"unidade_altura": null,"cubagem": "105","unidade_cubagem": "m3"}
- Exemplo 6: "livre de carga e descarga"
- Output 6: {"num_itens": null,"tipo_unidade_itens": null,"peso": null,"unidade_peso": null,"comprimento": null,"unidade_comprimento": null,"largura": null,"unidade_largura": null,"altura": null,"unidade_altura": null,"cubagem": null,"unidade_cubagem": null}
- Exemplo 7: "5,2 cubico peças de 4 mt peso 750 quilos paga 1,5 mil, obter cantoneiras de ferro forradas, necessario tag sem parar"
- Output 7: {"num_itens": null,"tipo_unidade_itens": null,"peso": "750","unidade_peso": "quilos","comprimento": "4","unidade_comprimento": "mt","largura": null,"unidade_largura": null,"altura": null,"unidade_altura": null,"cubagem": "5,2","unidade_cubagem": "cubicos"}
- Exemplo 8: "carreta para 500 palets, o bau tem que ter 90m³"
- Output 8: {"num_itens": "500","tipo_unidade_itens": "palets","peso": null,"unidade_peso": null,"comprimento": null,"unidade_comprimento": null,"largura": null,"unidade_largura": null,"altura": null,"unidade_altura": null,"cubagem": "90","unidade_cubagem": "m³"}
Agora é a sua vez, extraia as informações do texto a seguir e retorne apenas o output: {}
'''

    async def observation_field(self, obs: str):
        """
        Processa de forma assíncrona o campo de observações para extrair informações, utilizando tentativas repetidas e timeout.

        Parameters:
            obs (str): Texto do campo de observações a ser processado.

        Returns:
            str: As informações extraídas em forma de string, se bem-sucedido.
        """

        attempt = 0
        while attempt < self.max_retries:
            attempt += 1
            await asyncio.sleep(self.delay)
            try:
                response = await asyncio.wait_for(
                    openai.ChatCompletion.acreate(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": self.prompt},
                            {"role": "user", "content": obs}
                        ],
                        temperature=0,
                        max_tokens=2000,
                        top_p=0.01,
                        frequency_penalty=0,
                        presence_penalty=0
                    ),
                    timeout=self.timeout
                )
                return response.choices[0].message['content']
            except asyncio.TimeoutError:
                print("The request timed out. Retrying...")
            except Exception as e:
                print(f"An error occurred: {e}. Retrying...")
            else:
                break
        raise Exception("Maximum retries reached. The function failed to execute successfully.")
