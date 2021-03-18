import csv
from enum import Enum
import pandas as pd


class Extensions(Enum):
    CSV = ".csv"

class FileHandler:

    @staticmethod
    def load_data(path, file_ext):
        try:
            if file_ext == Extensions.CSV:
                dataDict = pd.read_csv(path,header=None, index_col=0, squeeze=True).to_dict()
                return dataDict

        except FileNotFoundError as e:
            print(f"Error: {e} - file does not exist")


def main():
    fh = FileHandler()
    fh.load_data("rb.csv",Extensions.CSV)

if __name__ == "__main__":
    main()