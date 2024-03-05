from argparse import ArgumentParser
from json import load
from math import isclose
from pathlib import Path
from sys import path

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path.append(str(Path(__file__).parent.parent.parent))

from battlib import Battery, EKFSOCEstimator

MAX_CELL_COUNT = 14


def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        'battery_file',
        type=open,
        help='battery parameters in json format',
    )
    parser.add_argument(
        'iv_file',
        type=open,
        help='iv data in csv format',
    )
    parser.add_argument(
        'soc_file',
        type=open,
        help='soc data in csv format',
    )
    parser.add_argument(
        'cell_count',
        type=int,
        help='number of cells',
    )
    parser.add_argument(
        'fig_file',
        type=Path,
        help='figure file path',
    )

    return parser.parse_args()


def main():
    args = parse_args()
    battery = Battery(**load(args.battery_file))
    iv_df = pd.read_csv(args.iv_file)
    soc_df = pd.read_csv(args.soc_file)
    cell_count = args.cell_count
    initial_voltage = iv_df['Output Voltage'][0]
    estimator = EKFSOCEstimator(battery, initial_voltage)
    predicted_x = []
    predicted_y = []
    actual_x = []
    actual_y = []

    for _, row in tqdm(iv_df.iterrows(), total=len(iv_df)):
        dt = row['Time Delta']
        i_in = row['Input Current'] / cell_count * MAX_CELL_COUNT
        measured_v = row['Output Voltage']

        estimator.step(dt, i_in, measured_v)
        predicted_x.append(estimator.soc)
        predicted_y.append(measured_v)

    for _, row in tqdm(soc_df.iterrows(), total=len(soc_df)):
        actual_x.append(row['SOC'])
        actual_y.append(row['VTerm'])

    plt.figure(figsize=(10, 6))
    plt.plot(predicted_x, predicted_y, label='Predicted')
    plt.plot(actual_x, actual_y, label='Actual')
    plt.title('Voltage versus SOC')
    plt.xlabel('SOC')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.savefig(args.fig_file, dpi=300)
    plt.show()


if __name__ == '__main__':
    main()
