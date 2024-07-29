# import json
# from pytest import mark
# from pytest_lazyfixture import lazy_fixture
# from unittest.mock import patch

# # TODO: Implementar entradas de exemplo para testes de predicao
# @mark.parametrize(
#     "entrada, saida_esperada, status_code_esperado",
#     [(lazy_fixture('entrada_inferencia_exemplo1'), lazy_fixture('saida_exemplo1'), 200)]
# )
# def test_invocations(client, uncompress_model, entrada, saida_esperada, status_code_esperado):
#     """
#     Testes de predicao.

#     Testa se as predicoes para exemplos definidos no conftest.py geram as saidas esperadas.
#     Tanto as entradas quanto as saidas utilizadas nos testes devem estar definidas no
#     conftest.py
#     """
#     resposta = client.post('/invocations', data=json.dumps(entrada), content_type='application/json')
#     json_de_resposta = resposta.json
#     status_code = resposta.status_code
#     assert (json_de_resposta, status_code) == (saida_esperada, status_code_esperado)


# def test_invocations_content_type_invalido(client, uncompress_model):
#     """
#     Testes de predicao.

#     Testa se as requisicoes de inferencia em que o content-type nao e um json
#     retorna o status code 415 corretamente.
#     """
#     resposta = client.post('/invocations', content_type='')
#     assert resposta.status_code == 415
