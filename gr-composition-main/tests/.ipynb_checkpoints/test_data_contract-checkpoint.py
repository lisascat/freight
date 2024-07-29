# import json
# import pytest
# from pytest_lazyfixture import lazy_fixture
# from jsonschema import Draft7Validator
# from jsonschema.exceptions import SchemaError
# from pathlib import Path

# ROOT_PATH = Path(__file__).parents[1]


# def test_check_contract():
#     path_schema = f'{ROOT_PATH}/deployment/contract/contrato_dados.json'
#     # path_schema = 'contrato_dados.json'

#     with open(path_schema, 'r') as file:
#         schema = json.load(file)

#     try:
#         Draft7Validator.check_schema(schema)
#         schema_is_valid = True
#     except SchemaError:
#         schema_is_valid = False
#     assert schema_is_valid == True

# @pytest.mark.parametrize(
#     'input, response', 
#     [
#         (lazy_fixture('input_predictor1'), True),
#         (lazy_fixture('input_predictor2'), True),
#         (lazy_fixture('input_predictor3'), True),
#         (lazy_fixture('input_predictor4'), True),
#         (lazy_fixture('input_predictor5'), True),
#         (lazy_fixture('input_datacontract1'), False),
#         (lazy_fixture('input_datacontract2'), False),
#         # (lazy_fixture('input_datacontract3'), False)
#     ]
# )
# def test_contract(input, response):
#     path_schema = f'{ROOT_PATH}/deployment/contract/contrato_dados.json'
#     # path_schema = 'contrato_dados.json'
#     validated = True
#     with open(path_schema, 'r') as file:
#         schema = json.loads(file.read())
    
#     errors = Draft7Validator(schema).iter_errors(input)
    
#     for error in errors:
#         print(error.message)
#         validated = False
#     if validated:
#         print("Valid response")
#         validated = True
    
#     assert validated == response

