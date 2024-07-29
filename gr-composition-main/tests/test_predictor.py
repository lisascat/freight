import json
import pytest
from pytest_lazyfixture import lazy_fixture
from pytest import mark

# def test_ping_model_not_found(client):
#     res = client.get('/ping')
#     assert res.status_code == 404

def test_load_model(client):
    res = client.get('/ping')
    assert res.status_code == 200

@pytest.mark.parametrize(
    "input, output, response_code",
    [
        (lazy_fixture("input_predictor1"), lazy_fixture("output_predictor1"), 200)
    ]
)
def test_invocations(client, input, output, response_code):
    res = client.post('/invocations', data=json.dumps(input), content_type='application/json')
    try:
        response_data = json.loads(res.data)
    except: 
        response_data = res.data.decode("utf-8")
    assert response_data == output and res.status_code == response_code


# # @pytest.mark.parametrize(
# #     'input, response',
# #     [(lazy_fixture('input_legal_invalid'), 500)])
# # def test_invocations_input_invalid(client, input, response):
# #     res = client.post('/invocations', data=json.dumps(input), content_type='application/json')
# #     assert res.status_code == response


def test_invocations_content_type(client):
    res = client.post('/invocations', data='testing...', content_type='')
    assert res.status_code == 415
