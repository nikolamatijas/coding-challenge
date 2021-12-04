import time
from pathlib import Path

import pandas as pd

from roas_calculator.constants import MANDATORY_COLUMNS, COLUMS_NAME_MAPPING


def write_output_csv(code, df):
    base_path = f'processed/{code}/search_terms'
    target_dir = Path(base_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / f'{time.time()}.csv'
    df.to_csv(file_path, index=False)


class RoasCalculator:
    def __init__(self, path):
        self.data_frame = pd.read_csv(path, encoding='utf_16', sep='\t')
        self.__cast_numeric_colums()

    def __cast_numeric_colums(self):
        self.data_frame['Conv. value'] = pd.to_numeric(self.data_frame['Conv. value'], errors='coerce')
        self.data_frame['Cost'] = pd.to_numeric(self.data_frame['Cost'], errors='coerce')
        self.data_frame['Clicks'] = pd.to_numeric(self.data_frame['Clicks'], errors='coerce').astype('Int64')

    def __drop_unnecessary_colums(self):
        unnecessary_colums = (set(self.data_frame.columns).difference(MANDATORY_COLUMNS))
        self.data_frame = self.data_frame.drop(list(unnecessary_colums), axis=1)

    def __drop_dirty_data(self):
        self.data_frame = self.data_frame[self.data_frame['Cost'] != 0]
        self.data_frame = self.data_frame.dropna()

    def clean_data(self):
        self.__drop_unnecessary_colums()
        self.__drop_dirty_data()

    def calculate_roas(self):
        self.data_frame['roas'] = self.data_frame['Conv. value'] / self.data_frame['Cost']
        currency_codes = self.data_frame['Currency code'].unique()
        df_dict = {}
        for code in currency_codes:
            df = self.data_frame[self.data_frame['Currency code'] == code]
            df_dict[code] = df

        for code, df_currency in df_dict.items():
            out_df = df_currency.drop(['Currency code'], axis=1)
            out_df = out_df.rename(columns=COLUMS_NAME_MAPPING)
            write_output_csv(code, out_df)
