#!/bin/bash

cd "$(dirname $0)"

python main.py data/battery.json data/14-cell-hppc-iv.csv data/14-cell-hppc-soc.csv 14 fig/14-cell-hppc.png
python main.py data/battery.json data/4-cell-constant-charge-iv.csv data/4-cell-constant-charge-soc.csv 4 fig/4-cell-constant-charge.png
python main.py data/battery.json data/4-cell-constant-discharge-iv.csv data/4-cell-constant-discharge-soc.csv 4 fig/4-cell-constant-discharge.png
