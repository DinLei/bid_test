#!/bin/bash

interval=160
while true
do
#/opt/predict/predictor/dsp_predictor/release/manual_modify_bid.sh
/opt/predict/predictor/release/bid_update_v2.sh
sleep $interval
done

