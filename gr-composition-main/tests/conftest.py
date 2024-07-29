import pytest
import pathlib
import sys
import pandas as pd
import json
import numpy as np

ROOT_PATH = pathlib.Path(__file__).parents[1]
code_directory = ROOT_PATH/'deployment'/'code'

if str(code_directory) not in sys.path:
    sys.path.append(str(code_directory))

from predictor import app

@pytest.fixture
def input_predictor1():
    input_data = {
      "trucker": {
        "person_uuid": "dc6e0435-9991-421e-a982-26c6391a4868",
        "document": "69992397805"
      },
      "vehicles": [
        {
          "plate": "62WFW01",
          "proprietary_vehicle": "69992397805",
          "rntrc": "567890",
          "rntrc_state": "SP",
          "proprietary_rntrc": "69992397805",
          "rntrc_registration_date": "2000-01-18"
        },
        {
          "plate": "D16440Z",
          "proprietary_vehicle": "69992397805",
          "rntrc": "567890",
          "rntrc_state": "PR",
          "proprietary_rntrc": "69992397805",
          "rntrc_registration_date": "2023-08-09"
        }
      ]
    }

    return input_data

@pytest.fixture
def output_predictor1():
    output_data = {
      "person_uuid": "dc6e0435-9991-421e-a982-26c6391a4868",
      "predict_proba": [
        0.11802061464787242
      ]
    }

    return output_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
