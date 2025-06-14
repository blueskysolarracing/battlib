#!/bin/bash

cd "$(dirname $0)"
export PYTHONPATH=../../..

python main.py EKFSOCEstimator data/battery.json data/2-cell-hppc-charge.csv 2 fig/ekf/2-cell-hppc-charge.pdf
python main.py EKFSOCEstimator data/battery.json data/2-cell-hppc-discharge.csv 2 fig/ekf/2-cell-hppc-discharge.pdf
python main.py EKFSOCEstimator data/battery.json data/2-cell-constant-charge.csv 2 fig/ekf/2-cell-constant-charge.pdf
python main.py EKFSOCEstimator data/battery.json data/2-cell-constant-discharge.csv 2 fig/ekf/2-cell-constant-discharge.pdf
