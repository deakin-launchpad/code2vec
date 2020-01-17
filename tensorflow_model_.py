import tensorflow as tf
import numpy as np
import time
from typing import Dict, Optional, List, Iterable
from collections import Counter
from functools import partial

from path_context_reader import PathContextReader, ModelInputTensorsFormer, ReaderInputTensors, EstimatorAction
from common import common
from vocabularies import VocabType
from config import Config
from model_base import Code2VecModelBase, ModelEvaluationResults, ModelPredictionResults

import pdb
tf.compat.v1.disable_eager_execution()


class Code2VecModel(Code2VecModelBase):
    def __init__(self, config: Config):
        self.sess = tf.compat.v1.Session()
        self.saver = None

        self.eval_reader = None
        self.eval_input_iterator_reset_op = None
        self.predict_reader = None

        # self.eval_placeholder = None
        self.predict_placeholder = None
        self.eval_top_words_op, self.eval_top_values_op, self.eval_original_names_op, self.eval_code_vectors = None, None, None, None
        self.predict_top_words_op, self.predict_top_values_op, self.predict_original_names_op = None, None, None

        self.vocab_type_to_tf_variable_name_mapping: Dict[VocabType, str] = {
            VocabType.Token: 'WORDS_VOCAB',
            VocabType.Target: 'TARGET_WORDS_VOCAB',
            VocabType.Path: 'PATHS_VOCAB'
        }

        super(Code2VecModel, self).__init__(config)

    def train(self):
        self.log('Starting training')
        start_time = time.time()

        batch_num = 0
        sum_loss = 0
        multi_batch_start_time = time.time()
        num_batches_to_save_and_eval = max(int(self.config.train_steps_per_epoch * self.config.SAVE_EVERY_EPOCHS), 1)
        #pdb.set_trace()
        train_reader = PathContextReader(vocabs=self.vocabs,
                                         model_input_tensors_former=_TFTrainModelInputTensorsFormer(),
                                         config=self.config, estimator_action=EstimatorAction.Train)

        #eval_reader = PathContextReader(vocabs=self.vocabs,
        #                                model_input_tensors_former=_TFEvaluateModelInputTensorsFormer(),
        #                                config=self.config, estimator_action=EstimatorAction.Evaluate)
        #input_iterator2 = tf.compat.v1.data.make_initializable_iterator(eval_reader.get_dataset())
        #eval_input_iterator_reset_op = input_iterator2.initializer
        #input_tensors2 = input_iterator2.get_next()
        #input_tensors3 = _TFEvaluateModelInputTensorsFormer().from_model_input_form(input_tensors2)
        input_iterator = tf.compat.v1.data.make_initializable_iterator(train_reader.get_dataset())
        input_iterator_reset_op = input_iterator.initializer

        input_tensors = input_iterator.get_next()
        #input_tensors1 = _TFTrainModelInputTensorsFormer().from_model_input_form(input_tensors)
        optimizer,train_loss,code2vec,label,logit,input_tensors1,new_lable,target_voca,logits,acc = self._build_tf_training_graph(input_tensors)


        self.saver = tf.compat.v1.train.Saver(max_to_keep=self.config.MAX_TO_KEEP)

        self.log('Number of trainable params: {}'.format(
            np.sum([np.prod(v.get_shape().as_list()) for v in tf.compat.v1.trainable_variables()])))
        for variable in tf.compat.v1.trainable_variables():
            self.log("variable name: {} -- shape: {} -- #params: {}".format(
                variable.name, variable.get_shape(), np.prod(variable.get_shape().as_list())))
        #keys_tensor = tf.constant(['oneonenine', 'eeninenine'])
        #vals_tensor = tf.constant([0, 1])
        # input_tensor = tf.constant(['CWE399', 'CWE119', 'CWE399', 'CWE119', 'CWE399', 'CWE119', 'CWE399', 'CWE119', 'CWE399'])
        # input
        #table = tf.lookup.StaticHashTable(
        #    tf.lookup.KeyValueTensorInitializer(keys_tensor, vals_tensor), -1)

        self._initialize_session_variables()

        if self.config.MODEL_LOAD_PATH:
            self._load_inner_model(self.sess)

        self.sess.run(input_iterator_reset_op)

        time.sleep(1)
        #input_tensors = _TFTrainModelInputTensorsFormer().from_model_input_form(input_tensors)
        self.log('Started reader...')
        #se1 = tf.compat.v2.strings.split('hello|world|d|g|gd|re', sep='|', maxsplit=-1)
        acc = self.sess.run(acc)
        a = self.sess.run(input_tensors)
        #input_tensor_test = self.sess.run(input_tensors3)
        new_label_ = self.sess.run(new_lable)
        a1 = self.sess.run(input_tensors1.target_index)
        b = self.sess.run(code2vec)
        c = self.sess.run(label)
        c = self.sess.run(tf.shape(label))
        target_voca = self.sess.run(target_voca)
        logit_ = self.sess.run(logits)

        d = self.sess.run(logit)
        #e = self.sess.run(train_reader)
        g = self.sess.run(input_tensors1.path_source_token_indices)
        #k = self.sess.run(input_tensors1.path_indices)
        p = self.sess.run(input_tensors1.path_target_token_indices)
        g = self.sess.run(input_tensors1.context_valid_mask)
        h = input_tensors1.target_string
        #k = tf.strings.substr(h, -10, -1)
        #tabl = table.lookup(k)

        #label_new = self.sess.run(tabl)
        #shap_ = tf.shape(k)
        #sh = self.sess.run(shap_)
        se1 = tf.compat.v2.strings.split(h,sep='|',maxsplit=-1)
        #se1_ = self.sess.run(k)

        #las = se1[:, -1]
        h_ori = self.sess.run(h)
        #h_sepa = self.sess.run(input_tensors1.target_string)

        #las_0 = self.sess.run(las)
        #las_ = self.sess.run(las)
        #h_0 = h[0]

        a = tf.strings.regex_full_match(h,"ninenine")
        a1 = self.sess.run(a)
        #subs_1 = tf.strings.substr(h_0,2,10,unit='BYTE',name=None)
        #se = tf.strings.split('fsdfds fdf ff',)
        #h___0 = self.sess.run(se)
        #h__0 = self.sess.run(h_0)

        #subs__1  = self.sess.run(subs_1)
        subs = tf.strings.substr(input_tensors1.target_string,1,7,unit='BYTE',name=None)
        sub = self.sess.run(subs)
        #for i in range(h):
        #   if 'CWE-'
        print(sorted(c))
        # run evaluation in a loop until iterator is exhausted.
        try:
            while True:
                # Each iteration = batch. We iterate as long as the tf iterator (reader) yields batches.
                batch_num += 1
                h = self.sess.run(input_tensors1.target_string)

                subs = tf.strings.substr(
                    input_tensors1.target_string[0],
                    - 1,
                    7,
                    unit='BYTE',
                    name=None
                )
                sub = self.sess.run(subs)
                # Actual training for the current batch.
                _, batch_loss = self.sess.run([optimizer, train_loss])

                sum_loss += batch_loss
                if batch_num % self.config.NUM_BATCHES_TO_LOG_PROGRESS == 0:
                    self._trace_training(sum_loss, batch_num, multi_batch_start_time)
                    # Uri: the "shuffle_batch/random_shuffle_queue_Size:0" op does not exist since the migration to the new reader.
                    # self.log('Number of waiting examples in queue: %d' % self.sess.run(
                    #    "shuffle_batch/random_shuffle_queue_Size:0"))
                    sum_loss = 0
                    multi_batch_start_time = time.time()
                #if batch_num % num_batches_to_save_and_eval == 0:
                if batch_num == 5:
                    epoch_num = int((batch_num / num_batches_to_save_and_eval) * self.config.SAVE_EVERY_EPOCHS)
                    model_save_path = self.config.MODEL_SAVE_PATH + '_iter' + str(epoch_num)
                    self.save(model_save_path)
                    self.log('Saved after %d epochs in: %s' % (epoch_num, model_save_path))
                    evaluation_results = self.evaluate()
                    #evaluation_results_str = (str(evaluation_results).replace('topk', 'top{}'.format(
                        #self.config.TOP_K_WORDS_CONSIDERED_DURING_PREDICTION)))
                    #self.log('After {nr_epochs} epochs -- {evaluation_results}'.format(
                     #   nr_epochs=epoch_num,
                      #  evaluation_results=evaluation_results_str
                    #))
        except tf.errors.OutOfRangeError:
            pass  # The reader iterator is exhausted and have no more batches to produce.

        self.log('Done training')

        if self.config.MODEL_SAVE_PATH:
            self._save_inner_model(self.config.MODEL_SAVE_PATH)
            self.log('Model saved in file: %s' % self.config.MODEL_SAVE_PATH)

        elapsed = int(time.time() - start_time)
        self.log("Training time: %sH:%sM:%sS\n" % ((elapsed // 60 // 60), (elapsed // 60) % 60, elapsed % 60))

    def evaluate(self) -> Optional[ModelEvaluationResults]:
        eval_start_time = time.time()
        if self.eval_reader is None:
            self.eval_reader = PathContextReader(vocabs=self.vocabs,
                                                 model_input_tensors_former=_TFEvaluateModelInputTensorsFormer(),
                                                 config=self.config, estimator_action=EstimatorAction.Evaluate)
            input_iterator = tf.compat.v1.data.make_initializable_iterator(self.eval_reader.get_dataset())
            self.eval_input_iterator_reset_op = input_iterator.initializer
            input_tensors = input_iterator.get_next()
            acc, input_tensors1 = self._build_tf_test_graph(input_tensors)
            #input_tensors1 = _TFEvaluateModelInputTensorsFormer().from_model_input_form(input_tensors)
            #self.eval_top_words_op, self.eval_top_values_op, self.eval_original_names_op, _, _, _, _, \
            #    self.eval_code_vectors = self._build_tf_test_graph(input_tensors)
            #self.eval_top_words_op, self.eval_top_values_op, self.eval_original_names_op, _, _, _, _, \

            #self._initialize_session_variables()
            self.saver = tf.compat.v1.train.Saver()
            #input = self.sess.run(input_tensors1)
            #ACC = self.sess.run(input_tensors)
            #if self.config.MODEL_LOAD_PATH and not self.config.TRAIN_DATA_PATH_PREFIX:
            self._initialize_session_variables()
            self._load_inner_model(self.sess)
            self.sess.run(self.eval_input_iterator_reset_op)
            acc = self.sess.run(acc)
            input = self.sess.run(input_tensors1)
            if self.config.RELEASE:
                release_name = self.config.MODEL_LOAD_PATH + '.release'
                self.log('Releasing model, output model: %s' % release_name)
                self.saver.save(self.sess, release_name)
                return None  # FIXME: why do we return none here?

        # with open('log.txt', 'w') as log_output_file:
        #     if self.config.EXPORT_CODE_VECTORS:
        #         code_vectors_file = open(self.config.TEST_DATA_PATH + '.vectors', 'w')
        #     total_predictions = 0
        #     total_prediction_batches = 0
        #     subtokens_evaluation_metric = SubtokensEvaluationMetric(
        #         partial(common.filter_impossible_names, self.vocabs.target_vocab.special_words))
        #     topk_accuracy_evaluation_metric = TopKAccuracyEvaluationMetric(
        #         self.config.TOP_K_WORDS_CONSIDERED_DURING_PREDICTION,
        #         partial(common.get_first_match_word_from_top_predictions, self.vocabs.target_vocab.special_words))
        #     start_time = time.time()
        #
        #     self.sess.run(self.eval_input_iterator_reset_op)
        #
        #     self.log('Starting evaluation')
        #
        #     # Run evaluation in a loop until iterator is exhausted.
        #     # Each iteration = batch. We iterate as long as the tf iterator (reader) yields batches.
        #     try:
        #         while True:
        #             top_words, top_scores, original_names, code_vectors = self.sess.run(
        #                 [self.eval_top_words_op, self.eval_top_values_op,
        #                  self.eval_original_names_op, self.eval_code_vectors],
        #             )
        #
        #             # shapes:
        #             #   top_words: (batch, top_k);   top_scores: (batch, top_k)
        #             #   original_names: (batch, );   code_vectors: (batch, code_vector_size)
        #
        #             top_words = common.binary_to_string_matrix(top_words)  # (batch, top_k)
        #             original_names = common.binary_to_string_list(original_names)  # (batch,)
        #
        #             self._log_predictions_during_evaluation(zip(original_names, top_words), log_output_file)
        #             topk_accuracy_evaluation_metric.update_batch(zip(original_names, top_words))
        #             subtokens_evaluation_metric.update_batch(zip(original_names, top_words))
        #
        #             total_predictions += len(original_names)
        #             total_prediction_batches += 1
        #             if self.config.EXPORT_CODE_VECTORS:
        #                 self._write_code_vectors(code_vectors_file, code_vectors)
        #             if total_prediction_batches % self.config.NUM_BATCHES_TO_LOG_PROGRESS == 0:
        #                 elapsed = time.time() - start_time
        #                 # start_time = time.time()
        #                 self._trace_evaluation(total_predictions, elapsed)
        #     except tf.errors.OutOfRangeError:
        #         pass  # reader iterator is exhausted and have no more batches to produce.
        #     self.log('Done evaluating, epoch reached')
        #     log_output_file.write(str(topk_accuracy_evaluation_metric.topk_correct_predictions) + '\n')
        # if self.config.EXPORT_CODE_VECTORS:
        #     code_vectors_file.close()
        
        elapsed = int(time.time() - eval_start_time)
        self.log("Evaluation time: %sH:%sM:%sS" % ((elapsed // 60 // 60), (elapsed // 60) % 60, elapsed % 60))
        return ModelEvaluationResults(
            topk_acc=topk_accuracy_evaluation_metric.topk_correct_predictions,
            subtoken_precision=subtokens_evaluation_metric.precision,
            subtoken_recall=subtokens_evaluation_metric.recall,
            subtoken_f1=subtokens_evaluation_metric.f1)

    def _build_tf_training_graph(self, input_tensors):
        # Use `_TFTrainModelInputTensorsFormer` to access input tensors by name.
        input_tensors = _TFTrainModelInputTensorsFormer().from_model_input_form(input_tensors)
        # shape of (batch, 1) for input_tensors.target_index
        # shape of (batch, max_contexts) for others:
        #   input_tensors.path_source_token_indices, input_tensors.path_indices,
        #   input_tensors.path_target_token_indices, input_tensors.context_valid_mask

        with tf.compat.v1.variable_scope('model'):
            #self.sess = tf.compat.v1.Session()

            keys_tensor = tf.constant(['oneonenine', 'eeninenine'])
            vals_tensor = tf.constant([0, 1])
            table = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(keys_tensor, vals_tensor), -1)

            h = input_tensors.target_string
            k = tf.strings.substr(h, -10, -1)
            tabl = table.lookup(k)



            #endddddddddddddddddddddddddddddd
            tokens_vocab = tf.compat.v1.get_variable(
                self.vocab_type_to_tf_variable_name_mapping[VocabType.Token],
                shape=(self.vocabs.token_vocab.size, self.config.TOKEN_EMBEDDINGS_SIZE), dtype=tf.float32,
                initializer=tf.compat.v1.initializers.variance_scaling(scale=1.0, mode='fan_out', distribution="uniform"))
            #targets_vocab = tf.compat.v1.get_variable(
                #self.vocab_type_to_tf_variable_name_mapping[VocabType.Target],
                #shape=(self.vocabs.target_vocab.size, self.config.TARGET_EMBEDDINGS_SIZE), dtype=tf.float32,
                #initializer=tf.compat.v1.initializers.variance_scaling(scale=1.0, mode='fan_out', distribution="uniform"))
            targets_vocab = tf.compat.v1.get_variable(
                self.vocab_type_to_tf_variable_name_mapping[VocabType.Target],
                shape=(2, self.config.TARGET_EMBEDDINGS_SIZE), dtype=tf.float32,
                initializer=tf.compat.v1.initializers.variance_scaling(scale=1.0, mode='fan_out',
                                                                       distribution="uniform"))
            attention_param = tf.compat.v1.get_variable(
                'ATTENTION',
                shape=(self.config.CODE_VECTOR_SIZE, 1), dtype=tf.float32)
            paths_vocab = tf.compat.v1.get_variable(
                self.vocab_type_to_tf_variable_name_mapping[VocabType.Path],
                shape=(self.vocabs.path_vocab.size, self.config.PATH_EMBEDDINGS_SIZE), dtype=tf.float32,
                initializer=tf.compat.v1.initializers.variance_scaling(scale=1.0, mode='fan_out', distribution="uniform"))

            code_vectors, _ = self._calculate_weighted_contexts(
                tokens_vocab, paths_vocab, attention_param, input_tensors.path_source_token_indices,
                input_tensors.path_indices, input_tensors.path_target_token_indices, input_tensors.context_valid_mask)

            logits = tf.matmul(code_vectors, targets_vocab, transpose_b=True)

            batch_size = tf.cast(tf.shape(input_tensors.target_index)[0], dtype=tf.float32)
            #loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(
                #labels=tf.reshape(input_tensors.target_index, [-1]),
                #logits=logits)) / batch_size
            loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(
                labels=tf.reshape(tabl, [-1]),
                logits=logits)) / batch_size
            optimizer = tf.compat.v1.train.AdamOptimizer().minimize(loss)

            labels_ = tf.reshape(tabl, [-1])
            labels__ = tf.dtypes.cast(labels_, tf.int64)
            # target_ = self.sess.run(target1)
            # correct_prediction = tf.equal(tf.argmax(logit, 1), label)
            correct_pred = tf.equal(tf.argmax(logits, 1), labels__)
            a = tf.dtypes.cast(correct_pred, tf.float32)
            acc = tf.reduce_mean(a)
            accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

            #b = self.sess.run(code_vectors)
            label = input_tensors.target_index
        return optimizer, loss,code_vectors,label,logits,input_tensors,tabl,targets_vocab,logits,acc

    def _calculate_weighted_contexts(self, tokens_vocab, paths_vocab, attention_param, source_input, path_input,
                                     target_input, valid_mask, is_evaluating=False):

        source_word_embed = tf.nn.embedding_lookup(params=tokens_vocab, ids=source_input)  # (batch, max_contexts, dim)
        path_embed = tf.nn.embedding_lookup(params=paths_vocab, ids=path_input)  # (batch, max_contexts, dim)
        target_word_embed = tf.nn.embedding_lookup(params=tokens_vocab, ids=target_input)  # (batch, max_contexts, dim)

        context_embed = tf.concat([source_word_embed, path_embed, target_word_embed],
                                  axis=-1)  # (batch, max_contexts, dim * 3)

        if not is_evaluating:
            context_embed = tf.nn.dropout(context_embed, rate=1-self.config.DROPOUT_KEEP_RATE)

        flat_embed = tf.reshape(context_embed, [-1, self.config.context_vector_size])  # (batch * max_contexts, dim * 3)
        transform_param = tf.compat.v1.get_variable(
            'TRANSFORM', shape=(self.config.context_vector_size, self.config.CODE_VECTOR_SIZE), dtype=tf.float32)

        flat_embed = tf.tanh(tf.matmul(flat_embed, transform_param))  # (batch * max_contexts, dim * 3)

        contexts_weights = tf.matmul(flat_embed, attention_param)  # (batch * max_contexts, 1)
        batched_contexts_weights = tf.reshape(
            contexts_weights, [-1, self.config.MAX_CONTEXTS, 1])  # (batch, max_contexts, 1)
        mask = tf.math.log(valid_mask)  # (batch, max_contexts)
        mask = tf.expand_dims(mask, axis=2)  # (batch, max_contexts, 1)
        batched_contexts_weights += mask  # (batch, max_contexts, 1)
        attention_weights = tf.nn.softmax(batched_contexts_weights, axis=1)  # (batch, max_contexts, 1)

        batched_embed = tf.reshape(flat_embed, shape=[-1, self.config.MAX_CONTEXTS, self.config.CODE_VECTOR_SIZE])
        code_vectors = tf.reduce_sum(tf.multiply(batched_embed, attention_weights), axis=1)  # (batch, dim * 3)

        return code_vectors, attention_weights

    def _build_tf_test_graph(self, input_tensors, normalize_scores=False):
        input_tensors = _TFEvaluateModelInputTensorsFormer().from_model_input_form(input_tensors)
        with tf.compat.v1.variable_scope('model', reuse=self.get_should_reuse_variables()):
            keys_tensor1 = tf.constant(['oneonenine', 'eeninenine'])
            vals_tensor1 = tf.constant([0, 1])
            table1 = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(keys_tensor1, vals_tensor1), -1)

            h = input_tensors.target_string
            k = tf.strings.substr(h, -10, -1)
            tabl1 = table1.lookup(k)
            #endddddddddddddddddddddddddddddddddddddddddddd
            tokens_vocab = tf.compat.v1.get_variable(
                self.vocab_type_to_tf_variable_name_mapping[VocabType.Token],
                shape=(self.vocabs.token_vocab.size, self.config.TOKEN_EMBEDDINGS_SIZE),
                dtype=tf.float32, trainable=False)
            #targets_vocab = tf.compat.v1.get_variable(
            #    self.vocab_type_to_tf_variable_name_mapping[VocabType.Target],
            #    shape=(self.vocabs.target_vocab.size, self.config.TARGET_EMBEDDINGS_SIZE),
            #    dtype=tf.float32, trainable=False)

            targets_vocab = tf.compat.v1.get_variable(
                self.vocab_type_to_tf_variable_name_mapping[VocabType.Target],
                shape=(2, self.config.TARGET_EMBEDDINGS_SIZE),
                dtype=tf.float32, trainable=False)
            attention_param = tf.compat.v1.get_variable(
                'ATTENTION', shape=(self.config.context_vector_size, 1),
                dtype=tf.float32, trainable=False)
            paths_vocab = tf.compat.v1.get_variable(
                self.vocab_type_to_tf_variable_name_mapping[VocabType.Path],
                shape=(self.vocabs.path_vocab.size, self.config.PATH_EMBEDDINGS_SIZE),
                dtype=tf.float32, trainable=False)

            #targets_vocab = tf.transpose(targets_vocab)  # (dim * 3, target_word_vocab)

            # Use `_TFEvaluateModelInputTensorsFormer` to access input tensors by name.

            # shape of (batch, 1) for input_tensors.target_string
            # shape of (batch, max_contexts) for the other tensors

            code_vectors, attention_weights = self._calculate_weighted_contexts(
                tokens_vocab, paths_vocab, attention_param, input_tensors.path_source_token_indices,
                input_tensors.path_indices, input_tensors.path_target_token_indices,
                input_tensors.context_valid_mask, is_evaluating=True)

        scores = tf.matmul(code_vectors, targets_vocab,transpose_b=True)  # (batch, target_word_vocab)
        #batch_size = tf.cast(tf.shape(input_tensors.target_index)[0], dtype=tf.float32)
        # loss = tf.reduce_sum(tf.nn.sparse_softmax_cross_entropy_with_logits(
        # labels=tf.reshape(input_tensors.target_index, [-1]),
        # logits=logits)) / batch_size



        labels_ = tf.reshape(tabl1, [-1])
        labels__ = tf.dtypes.cast(labels_, tf.int64)
        # target_ = self.sess.run(target1)
        # correct_prediction = tf.equal(tf.argmax(logit, 1), label)
        correct_pred = tf.equal(tf.argmax(scores, 1), labels__)
        a = tf.dtypes.cast(correct_pred, tf.float32)
        # topk_candidates = tf.nn.top_k(scores, k=tf.minimum(
        #     self.config.TOP_K_WORDS_CONSIDERED_DURING_PREDICTION, self.vocabs.target_vocab.size))
        # top_indices = topk_candidates.indices
        # top_words = self.vocabs.target_vocab.lookup_word(top_indices)
        # original_words = input_tensors.target_string
        # top_scores = topk_candidates.values
        # if normalize_scores:
        #     top_scores = tf.nn.softmax(top_scores)

        #return top_words, top_scores, original_words, attention_weights, input_tensors.path_source_token_strings, \
        #       input_tensors.path_strings, input_tensors.path_target_token_strings, code_vectors
        acc = tf.reduce_mean(a)
        accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        return acc, input_tensors
    def predict(self, predict_data_lines: Iterable[str]) -> List[ModelPredictionResults]:
        if self.predict_reader is None:
            self.predict_reader = PathContextReader(vocabs=self.vocabs,
                                                    model_input_tensors_former=_TFEvaluateModelInputTensorsFormer(),
                                                    config=self.config, estimator_action=EstimatorAction.Predict)
            self.predict_placeholder = tf.compat.v1.placeholder(tf.string)
            reader_output = self.predict_reader.process_input_row(self.predict_placeholder)

            self.predict_top_words_op, self.predict_top_values_op, self.predict_original_names_op, \
            self.attention_weights_op, self.predict_source_string, self.predict_path_string, \
            self.predict_path_target_string, self.predict_code_vectors = \
                self._build_tf_test_graph(reader_output, normalize_scores=True)

            self._initialize_session_variables()
            self.saver = tf.compat.v1.train.Saver()
            self._load_inner_model(sess=self.sess)

        prediction_results: List[ModelPredictionResults] = []
        for line in predict_data_lines:
            batch_top_words, batch_top_scores, batch_original_name, batch_attention_weights, batch_path_source_strings,\
                batch_path_strings, batch_path_target_strings, batch_code_vectors = self.sess.run(
                    [self.predict_top_words_op, self.predict_top_values_op, self.predict_original_names_op,
                     self.attention_weights_op, self.predict_source_string, self.predict_path_string,
                     self.predict_path_target_string, self.predict_code_vectors],
                    feed_dict={self.predict_placeholder: line})
            # shapes:
            #   batch_top_words, top_scores: (batch, top_k)
            #   batch_original_name: (batch, )
            #   batch_attention_weights: (batch, max_context, 1)
            #   batch_path_source_strings, batch_path_strings, batch_path_target_strings: (batch, max_context)
            #   batch_code_vectors: (batch, code_vector_size)

            # remove first axis: (batch=1, ...)
            assert all(tensor.shape[0] == 1 for tensor in (batch_top_words, batch_top_scores, batch_original_name,
                                                           batch_attention_weights, batch_path_source_strings,
                                                           batch_path_strings, batch_path_target_strings,
                                                           batch_code_vectors))
            top_words = np.squeeze(batch_top_words, axis=0)
            top_scores = np.squeeze(batch_top_scores, axis=0)
            original_name = batch_original_name[0]
            attention_weights = np.squeeze(batch_attention_weights, axis=0)
            path_source_strings = np.squeeze(batch_path_source_strings, axis=0)
            path_strings = np.squeeze(batch_path_strings, axis=0)
            path_target_strings = np.squeeze(batch_path_target_strings, axis=0)
            code_vectors = np.squeeze(batch_code_vectors, axis=0)

            top_words = common.binary_to_string_list(top_words)
            original_name = common.binary_to_string(original_name)
            attention_per_context = self._get_attention_weight_per_context(
                path_source_strings, path_strings, path_target_strings, attention_weights)
            prediction_results.append(ModelPredictionResults(
                original_name=original_name,
                topk_predicted_words=top_words,
                topk_predicted_words_scores=top_scores,
                attention_per_context=attention_per_context,
                code_vector=(code_vectors if self.config.EXPORT_CODE_VECTORS else None)
            ))
        return prediction_results

    def _save_inner_model(self, path: str):
        self.saver.save(self.sess, path)

    def _load_inner_model(self, sess=None):
        if sess is not None:
            #self.log('Loading model weights from: ' + self.config.MODEL_LOAD_PATH)
            self.log('Loading model weights from: ' + '/home/dung/Downloads/Mohamed/code2vec-master_local/models/git'
                                                      '-repos-32/saved_model_iter0')
            #self.saver.restore(sess, self.config.MODEL_LOAD_PATH)
            self.saver.restore(sess, '/home/dung/Downloads/Mohamed/code2vec-master_local/models/git-repos-32'
                                     '/saved_model_iter0')
            self.log('Done loading model weights')

    def _get_vocab_embedding_as_np_array(self, vocab_type: VocabType) -> np.ndarray:
        assert vocab_type in VocabType
        vocab_tf_variable_name = self.vocab_type_to_tf_variable_name_mapping[vocab_type]
        with tf.compat.v1.variable_scope('model', reuse=None):
            embeddings = tf.compat.v1.get_variable(vocab_tf_variable_name)
            self.saver = tf.compat.v1.train.Saver()
            self._load_inner_model(self.sess)
            vocab_embedding_matrix = self.sess.run(embeddings)
            return vocab_embedding_matrix

    def get_should_reuse_variables(self):
        if self.config.TRAIN_DATA_PATH_PREFIX:
            return True
        else:
            return None

    def _log_predictions_during_evaluation(self, results, output_file):
        for original_name, top_predicted_words in results:
            found_match = common.get_first_match_word_from_top_predictions(
                self.vocabs.target_vocab.special_words, original_name, top_predicted_words)
            if found_match is not None:
                prediction_idx, predicted_word = found_match
                if prediction_idx == 0:
                    output_file.write('Original: ' + original_name + ', predicted 1st: ' + predicted_word + '\n')
                else:
                    output_file.write('\t\t predicted correctly at rank: ' + str(prediction_idx + 1) + '\n')
            else:
                output_file.write('No results for predicting: ' + original_name)

    def _trace_training(self, sum_loss, batch_num, multi_batch_start_time):
        multi_batch_elapsed = time.time() - multi_batch_start_time
        avg_loss = sum_loss / (self.config.NUM_BATCHES_TO_LOG_PROGRESS * self.config.TRAIN_BATCH_SIZE)
        throughput = self.config.TRAIN_BATCH_SIZE * self.config.NUM_BATCHES_TO_LOG_PROGRESS / \
                     (multi_batch_elapsed if multi_batch_elapsed > 0 else 1)
        self.log('Average loss at batch %d: %f, \tthroughput: %d samples/sec' % (
            batch_num, avg_loss, throughput))

    def _trace_evaluation(self, total_predictions, elapsed):
        state_message = 'Evaluated %d examples...' % total_predictions
        throughput_message = "Prediction throughput: %d samples/sec" % int(
            total_predictions / (elapsed if elapsed > 0 else 1))
        self.log(state_message)
        self.log(throughput_message)

    def close_session(self):
        self.sess.close()

    def _initialize_session_variables(self):
        self.sess.run(tf.group(
            tf.compat.v1.global_variables_initializer(),
            tf.compat.v1.local_variables_initializer(),
            tf.compat.v1.tables_initializer()))
        self.log('Initalized variables')

    def _initialize_session_variables1(self):
        self.sess.run(tf.group(
            tf.compat.v1.global_variables_initializer(),
            tf.compat.v1.local_variables_initializer()))
        self.log('Initalized variables')
class SubtokensEvaluationMetric:
    def __init__(self, filter_impossible_names_fn):
        self.nr_true_positives: int = 0
        self.nr_false_positives: int = 0
        self.nr_false_negatives: int = 0
        self.nr_predictions: int = 0
        self.filter_impossible_names_fn = filter_impossible_names_fn

    def update_batch(self, results):
        for original_name, top_words in results:
            prediction = self.filter_impossible_names_fn(top_words)[0]
            original_subtokens = Counter(common.get_subtokens(original_name))
            predicted_subtokens = Counter(common.get_subtokens(prediction))
            self.nr_true_positives += sum(count for element, count in predicted_subtokens.items()
                                          if element in original_subtokens)
            self.nr_false_positives += sum(count for element, count in predicted_subtokens.items()
                                           if element not in original_subtokens)
            self.nr_false_negatives += sum(count for element, count in original_subtokens.items()
                                           if element not in predicted_subtokens)
            self.nr_predictions += 1

    @property
    def true_positive(self):
        return self.nr_true_positives / self.nr_predictions

    @property
    def false_positive(self):
        return self.nr_false_positives / self.nr_predictions

    @property
    def false_negative(self):
        return self.nr_false_negatives / self.nr_predictions

    @property
    def precision(self):
        return self.nr_true_positives / (self.nr_true_positives + self.nr_false_positives)

    @property
    def recall(self):
        return self.nr_true_positives / (self.nr_true_positives + self.nr_false_negatives)

    @property
    def f1(self):
        return 2 * self.precision * self.recall / (self.precision + self.recall)


class TopKAccuracyEvaluationMetric:
    def __init__(self, top_k: int, get_first_match_word_from_top_predictions_fn):
        self.top_k = top_k
        self.nr_correct_predictions = np.zeros(self.top_k)
        self.nr_predictions: int = 0
        self.get_first_match_word_from_top_predictions_fn = get_first_match_word_from_top_predictions_fn

    def update_batch(self, results):
        for original_name, top_predicted_words in results:
            self.nr_predictions += 1
            found_match = self.get_first_match_word_from_top_predictions_fn(original_name, top_predicted_words)
            if found_match is not None:
                suggestion_idx, _ = found_match
                self.nr_correct_predictions[suggestion_idx:self.top_k] += 1

    @property
    def topk_correct_predictions(self):
        return self.nr_correct_predictions / self.nr_predictions


class _TFTrainModelInputTensorsFormer(ModelInputTensorsFormer):
    def to_model_input_form(self, input_tensors: ReaderInputTensors):
        return input_tensors.target_index, input_tensors.path_source_token_indices, input_tensors.path_indices, \
               input_tensors.path_target_token_indices, input_tensors.context_valid_mask,input_tensors.target_string

    def from_model_input_form(self, input_row) -> ReaderInputTensors:
        return ReaderInputTensors(
            target_index=input_row[0],
            path_source_token_indices=input_row[1],
            path_indices=input_row[2],
            path_target_token_indices=input_row[3],
            context_valid_mask=input_row[4],
            target_string=input_row[5]
        )


class _TFEvaluateModelInputTensorsFormer(ModelInputTensorsFormer):
    def to_model_input_form(self, input_tensors: ReaderInputTensors):
        return input_tensors.target_string, input_tensors.path_source_token_indices, input_tensors.path_indices, \
               input_tensors.path_target_token_indices, input_tensors.context_valid_mask, \
               input_tensors.path_source_token_strings, input_tensors.path_strings, \
               input_tensors.path_target_token_strings

    def from_model_input_form(self, input_row) -> ReaderInputTensors:
        return ReaderInputTensors(
            target_string=input_row[0],
            path_source_token_indices=input_row[1],
            path_indices=input_row[2],
            path_target_token_indices=input_row[3],
            context_valid_mask=input_row[4],
            path_source_token_strings=input_row[5],
            path_strings=input_row[6],
            path_target_token_strings=input_row[7]
        )
