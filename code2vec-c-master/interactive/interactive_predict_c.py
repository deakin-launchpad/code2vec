# coding=utf-8
# C extractor for code2vec
#
# Copyright 2019 Carnegie Mellon University. All Rights Reserved.
#
# NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
# Released under a MIT (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
# [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
# Carnegie Mellon® and CERT® are registered in the U.S. Patent and Trademark Office by Carnegie Mellon University.
# This Software includes and/or makes use of the following Third-Party Software subject to its own license:
# 1. code2vec (https://github.com/tech-srl/code2vec/blob/master/LICENSE) Copyright 2018 Technion.
# 2. LLVM / CLANG (https://github.com/llvm-mirror/clang/blob/master/LICENSE.TXT) Copyright 2019 LLVM.
# DM19-0540
import traceback
import hashlib
import os
from extractor_c import CExtractor

# This is in base code2vec
from common import common

SHOW_TOP_CONTEXTS = 1000
MAX_LEAF_NODES = 917

class InteractivePredictor:
    def __init__(self, config, model):
        model.predict([])
        self.model = model
        self.config = config
        self.path_extractor = CExtractor(config,
                                        clang_path=os.environ['CLANG_PATH'],
                                        max_leaves=MAX_LEAF_NODES)

    def predict(self):
        input_filename = 'function.c'
        print('Starting interactive prediction for c...')
        try:
            predict_lines, hash_to_string_dict = self.path_extractor.extract_paths(input_filename)
        except ValueError as e:
            print(e)
            #continue

        raw_prediction_results = self.model.predict(predict_lines)
        method_prediction_results = common.parse_prediction_results(
            raw_prediction_results, hash_to_string_dict,
            self.model.vocabs.target_vocab.special_words, topk=SHOW_TOP_CONTEXTS)
        with open('result.txt', 'w+') as resultfile:
            for raw_prediction, method_prediction in zip(raw_prediction_results, method_prediction_results):
                print('Original-name: ' + method_prediction.original_name + '\n')
                print(method_prediction)
                resultfile.writelines('Function Name - '+method_prediction.original_name + '\n')
                if 'NONE' in method_prediction.predictions[0]['name'] and float(method_prediction.predictions[0]['probability']) < 0.80:
                    for number in range(1,4):
                        prediction = method_prediction.predictions[number]
                        prediction['name'] = map_vulnerability_names(prediction['name'])
                        print('prediction for NONE is - ', prediction)
                        resultfile.writelines(prediction['name'] + ' ^ ' + str(float(prediction['probability']*100))+'%' + '\n')
                else:
                    for number in range(0,3):
                        prediction = method_prediction.predictions[number]
                        prediction['name'] = map_vulnerability_names(prediction['name'])
                        print('prediction for NONE is - ', prediction)
                        resultfile.writelines(prediction['name'] + ' ^ ' + str(float(prediction['probability']*100)) + '%' + '\n')

                for name_prob_pair in method_prediction.predictions:
                    print('\t(%f) predicted: %s' % (name_prob_pair['probability'], name_prob_pair['name']))


def map_vulnerability_names(name):
    if 'CWEONEHUNDREDTWENTY' in name:
        return 'CWE-120'
    if 'CWEONEHUNDREDNINETEEN' in name:
        return 'CWE-119'
    if 'CWEFOURHUNDREDSIXTYNINE' in name:
        return 'CWE-469'
    if 'CWEFOURHUNDREDSEVENTYSIX' in name:
        return 'CWE-476'
    if 'CWEOTHER' in name:
        return 'CWE-Other'
    else: 
        return 'None'

