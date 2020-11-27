#!/bin/bash

MODEL_DIR=${SM_HP_MODEL_DIR}
PIPELINE_CONFIG_PATH=${SM_HP_PIPELINE_CONFIG_PATH}
NUM_TRAIN_STEPS=${SM_HP_NUM_TRAIN_STEPS}
SAMPLE_1_OF_N_EVAL_EXAMPLES=${SM_HP_SAMPLE_1_OF_N_EVAL_EXAMPLES}

if [ ${SM_NUM_GPUS} > 0 ]
then
   NUM_WORKERS=${SM_NUM_GPUS}
else
   NUM_WORKERS=1
fi

echo "===TRAINING THE MODEL=="
python model_main_tf2.py \
    --pipeline_config_path ${PIPELINE_CONFIG_PATH} \
    --model_dir ${MODEL_DIR} \
    --num_train_steps ${NUM_TRAIN_STEPS} \
    --num_workers ${NUM_WORKERS} \
    --sample_1_of_n_eval_examples ${SAMPLE_1_OF_N_EVAL_EXAMPLES} \
    --alsologtostderr

echo "==EVALUATING THE MODEL=="
python model_main_tf2.py \
    --pipeline_config_path ${PIPELINE_CONFIG_PATH} \
    --model_dir ${MODEL_DIR} \
    --checkpoint_dir ${MODEL_DIR} \
    --eval_timeout 10

echo "==EXPORTING THE MODEL=="
python exporter_main_v2.py \
    --trained_checkpoint_dir ${MODEL_DIR} \
    --pipeline_config_path ${PIPELINE_CONFIG_PATH} \
    --output_directory /tmp/exported
    
mv /tmp/exported/saved_model /opt/ml/model/1