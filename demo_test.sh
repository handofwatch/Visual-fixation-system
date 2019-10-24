#!/bin/bash

# Image and model names
TEST_IMG=ADE_val_00001519.jpg
MODEL_PATH=baseline-resnet50dilated-ppm_deepsup
RESULT_PATH=./

ENCODER=$MODEL_PATH/encoder_epoch_20.pth
DECODER=$MODEL_PATH/decoder_epoch_20.pth

# Download model weights and image
if [ ! -e $MODEL_PATH ]; then
  mkdir $MODEL_PATH
fi
if [ ! -e $ENCODER ]; then
  wget -P $MODEL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$ENCODER
fi
if [ ! -e $DECODER ]; then
  wget -P $MODEL_PATH http://sceneparsing.csail.mit.edu/model/pytorch/$DECODER
fi
if [ ! -e $TEST_IMG ]; then
  wget -P $RESULT_PATH http://sceneparsing.csail.mit.edu/data/ADEChallengeData2016/images/validation/$TEST_IMG
fi

# Inference
python -u test.py \
  --imgs C:\\sspm\\semantic-segmentation-pytorch-master\\data\\ADEChallengeData2016\\images\\validation\\ADE_val_00000001.jpg  \
  --cfg config/ade20k-mobilenetv2dilated-c1_deepsup.yaml \
  TEST.result ./ \
  TEST.suffix _epoch_20.pth

  #DIR $MODEL_PATH \