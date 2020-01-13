'''

API to fetch static analysis result
Developed by: Somanshu Kalra

'''

import flask
import os
import sys
import json
import re
from flask import render_template, jsonify, request
import collections
app = flask.Flask(__name__)
app.config["DEBUG"] = True


#Method to render home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


#Method to load static analysis home page
@app.route('/staticAnalysis', methods=['GET'])
def staticAnalysis():
    return render_template('index.html')


#Method to process static analysis by generating prediction results
@app.route('/staticAnalysis', methods=['POST'])
def evaluate_staticAnalysis():
    print('request received')
    response = {}
    key = ''
    values = []
    function_names = []
    i = 0
    payload = str(request.data, encoding='utf-8')
    print('payload is - ', payload)
    with open('function.c', 'w+') as outputfile:
        outputfile.write(payload)
    outputfile.close()
    os.system('sudo bash predict.sh')
    with open('function_names.txt', 'r') as func_name:
        function_names = func_name.readlines()
    func_name.close()
    print(function_names)
    with open('result.txt', 'r') as responsefile:
        for line in responsefile:
            if 'Function Name'in line:
                line = 'Function Name - ' + function_names[i]
                i += 1
                key = line
                response[key] = ''
                values = []
            else:
                values.append(line)
            response[key] = dict(s.split('^') for s in values)
    responsefile.close()
    print('response generated, converting to json')
    response_json = json.dumps(response)
    return response_json


#Method to load clause analyser home page
@app.route('/clauseAnalysis', methods=['GET'])
def load_clause_analysis():
    return render_template('clause.html')


@app.route('/clauseAnalysis', methods=['POST'])
def evaluate_clasueAnalysis():
    print('Request received')
    final_output = ''
    payload = str(request.data, encoding='utf-8')
    payload = re.sub(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", "\n", payload)
    #sentences = filter(None, re.split("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", payload))
    sentences = payload.split("\n")
    print('Sentences are - ', sentences)
    sentences = [re.sub(r'[^a-zA-Z0-9\.\,\?\!\(\)\:\-\\\/ ]', '', sentence) for sentence in sentences]
    json_input = str([{"Sentence": sentence.lstrip()} for sentence in sentences]).replace('\'', '\"')
    with open('/home/ubuntu/multi-class-text-classification-cnn/data/predictionData.json', 'w+') as inputfile:
        inputfile.writelines(json_input)
    inputfile.close()
    os.system('sudo bash claudette.sh')
    with open('/home/ubuntu/multi-class-text-classification-cnn/data/prediction.json', 'r') as outputfile:
        final_output = json.load(outputfile)
    outputfile.close()
    return json.dumps(final_output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
