from argparse import ArgumentParser, Namespace
from json import load
from pathlib import Path

from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd

from battlib import Battery, CCSOCEstimator
import battlib

MAX_CELL_COUNT = 9


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        'soc_estimator',
        type=str,
        help='soc estimator',
    )
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


def main() -> None:
    args = parse_args()
    battery = Battery(**load(args.battery_file))
    iv_df = pd.read_csv(args.iv_file)
    cell_count = args.cell_count
    initial_voltage = iv_df[' Output Voltage '][0]
    estimator = getattr(battlib, args.soc_estimator)(battery, initial_voltage)
    predicted_x = []
    predicted_y = []

    for _, row in tqdm(iv_df.iterrows(), total=len(iv_df)):
        dt = row[' Time Delta']
        i_in = row[' Input Current'] / cell_count * MAX_CELL_COUNT
        measured_v = row[' Output Voltage ']

        estimator.step(dt=dt, i_in=i_in, measured_v=measured_v)
        predicted_x.append(estimator.soc)
        predicted_y.append(measured_v)

    estimator = CCSOCEstimator(battery, initial_voltage)
    actual_x = []
    actual_y = []

    for _, row in tqdm(iv_df.iterrows(), total=len(iv_df)):
        dt = row[' Time Delta']
        i_in = row[' Input Current'] / cell_count * MAX_CELL_COUNT
        measured_v = row[' Output Voltage ']

        estimator.step(dt=dt, i_in=i_in)
        actual_x.append(estimator.soc)
        actual_y.append(measured_v)

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
