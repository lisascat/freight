import json
import flask
# from flask import request, current_app as app
# from utils.utils import personsPreProcessor, preProcessing, processJson
from utils.utils import preProcessing, processJson
from utils.sigmoidFunctions import get_score
import os
import pickle
import logging
import time

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

logging.basicConfig(level=logging.INFO)

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
    
    try:
        model = load_model()
        responses = {}
        for key, value in input_json.items():
            if isinstance(value, list):
                list_person = []
                for person in value:
                    if person['process'] is not None:
                        preProcessed = preProcessing(processJson(person))
                        if preProcessed.empty:
                            list_person.append({'document': person['document'], 'LegalScore': 0})
                        else:
                            list_person.append(get_score(model, preProcessed, ['document', 'LegalScore']))
                    else:
                        list_person.append({'document': person['document'], 'LegalScore': 0})
                responses.update({key: list_person})
            else:
                if input_json[key]['process'] is not None:
                    preProcessed = preProcessing(processJson(input_json[key]), key)
                    if preProcessed.empty:
                        responses.update({key: {'person_uuid': input_json[key]['person_uuid'], 'LegalScore': 0}})
                    else:
                        responses.update({key: get_score(model, preProcessed, ['person_uuid', 'LegalScore'])})
                else:
                    responses.update({key: {'person_uuid': input_json[key]['person_uuid'], 'LegalScore': 0}}) 
        response = json.dumps(responses)

        processing_time = time.time() - start_time  
        
        logging.info(f"Processing time: {processing_time} seconds") 

        return flask.Response(response=response, status=200, mimetype='application/json')
    except Exception as e:
        logging.exception(e)
        processing_time = time.time() - start_time  
        logging.info(f"Processing time: {processing_time} seconds")
        return flask.Response(response='Error processing file', status=500,
                              mimetype='application/json')
