#!/usr/bin/env bash
###########################################################
# Change the following values to train a new model.
# type: the name of the new model, only affects the saved file name.
# dataset: the name of the dataset, as was preprocessed using preprocess.sh
# test_data: by default, points to the validation set, since this is the set that
#   will be evaluated after each training iteration. If you wish to test
#   on the final (held-out) test set, change 'val' to 'test'.
type=git-repos-32
dataset_name=git-repos-32
data_dir=data/${dataset_name}
data=${data_dir}/${dataset_name}
test_data=${data_dir}/${dataset_name}.val.c2v
model_dir=models/${type}

mkdir -p models/${model_dir}
set -e
python3 -u code2vec.py --data ${data} --test ${test_data} --save ${model_dir}/saved_model

data_dir=data/git-repos-32
data=data/git-repos-32/git-repos-32
model_dir=models/git-repos-32
test_data=data/git-repos-32/git-repos-32.val.c2v
--data data/git-repos-32/git-repos-32 --test data/git-repos-32/git-repos-32.val.c2v --save models/git-repos-32/saved_model

