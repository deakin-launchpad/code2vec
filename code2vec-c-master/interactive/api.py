'''

API to fetch static analysis result
Developed by: Somanshu Kalra

'''

import flask
import os
import sys
import json
from flask import render_template, jsonify, request
import collections
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def test():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def home():
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
    response_json = json.dumps(response)
    print(response_json)
    return response_json


