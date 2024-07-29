import json
import flask
import time
import joblib
import pandas as pd
# from flask import request, current_app as app
from utils.utils import *
from typing import List, Dict, Hashable, Optional, Union, Tuple
from sklearn.pipeline import Pipeline
import os
import pickle
import logging
import pdb
from pathlib import Path

model_path = Path('/opt/ml/model')

if not model_path.is_dir():
    logging.warning(f"O diretório do modelo '{model_path}' não existe.")
    root_path = Path(__file__).resolve().parents[1]
    model_path = root_path/'model'
    logging.info(f"O diretório do modelo foi redefinido para '{model_path}'")
    
logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)

app = flask.Flask(__name__)

def load_model():
    try: 
        with open(os.path.join(model_path, 'model.pkl'), 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        logging.exception("Erro ao carregar o modelo.")
        model = None
    return model

@app.route('/ping', methods=['GET'])
def ping():
    model = load_model()

    if model is not None:
        status = 200
    else:
        status = 404
        
    return flask.Response(response= '\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    
    start_time = time.time()
    
    if flask.request.content_type != 'application/json':
        return flask.Response(response='This predictor only supports JSON data', status=415, mimetype='application/json')
    
    input_json = flask.request.get_json(force=True)
    
    logging.info('Dados recebidos para inferencia')
    logging.info(input_json)

    try:
        response = {}

        person_uuid = input_json['trucker']['person_uuid']
        response['person_uuid'] = person_uuid

        if input_json['vehicles']:
            model = load_model()
            df = preprocessor(input_json)
            y_pred_proba = model.predict_proba(df)[:, 1]

            response['predict_proba'] = y_pred_proba[0] if y_pred_proba.size > 0 else None
        else:
            response['predict_proba'] = 0

        processing_time = time.time() - start_time  
        logging.info(f"Processing time: {processing_time} seconds")

        return flask.Response(response=json.dumps(response), status=200, mimetype='application/json')  
    except Exception as e:
        logging.exception(e)
        processing_time = time.time() - start_time  
        logging.info(f"Processing time: {processing_time} seconds")  
        return flask.Response(response='Error processing file', status=500, mimetype='application/json')
