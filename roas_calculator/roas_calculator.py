import logging
import time
from pathlib import Path

import pandas as pd
from pandas import DataFrame
from pandas.errors import EmptyDataError

from roas_calculator.constants import MANDATORY_COLUMNS, COLUMS_NAME_MAPPING


def write_output_csv(code: str, df: DataFrame):
    """
    Creates new CSV file with content of df DataFrame.

    Parameters:
        code(str): string that represents currency code
        df(pandas.DataFrame): df represents table with data
    """
    base_path = f'processed/{code}/search_terms'
    target_dir = Path(base_path)
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / f'{time.time()}.csv'
    df.to_csv(file_path, index=False, encoding='utf_16')


class RoasCalculator:
    """
    RoosCalculator class represents process of calculating ROAS values for input CSV files.

    Attributes:
        file_path (str): path of input CSV file
        data_frame (pandas.DataFrame): data frame created from input CSV file
    """
    def __init__(self, path: str):
        """
        The constructor for RoasCalculator class.

        Parameters:
           path (str): Path of input CSV file. Data from this CSV path will be used to calculate ROAS.
        """
        try:
            self.file_path = path
            self.data_frame = pd.read_csv(path, encoding='utf_16', sep='\t')
        except (FileNotFoundError, EmptyDataError, IOError):
            logging.error('Unable to read %s CSV file.File is corrupted.', self.file_path)
            self.data_frame = None

    def validate_data_frame_columns(self):
        """
        Validate does data_frame contain all necessary columns for output CSV file.

        Returns:
            bool: True if data_frame have all mandatory columns. Else returns False.
        """
        if MANDATORY_COLUMNS.issubset(set(self.data_frame.columns)):
            return True
        else:
            logging.error('CSV file %s does not contain mandatory columns.', self.file_path)
            return False

    def cast_numeric_columns(self):
        """
        Converts data from columns Conv. value, Cost and Click to numeric values. Invalid parsing will be set as NaN.
        """
        self.data_frame['Conv. value'] = pd.to_numeric(self.data_frame['Conv. value'], errors='coerce')
        self.data_frame['Cost'] = pd.to_numeric(self.data_frame['Cost'], errors='coerce')
        self.data_frame['Clicks'] = pd.to_numeric(self.data_frame['Clicks'], errors='coerce').astype('Int64')

    def drop_unnecessary_columns(self):
        """
        Removes all columns from data_frame which are not needed for the ROAS calculation and output CSV file.
        """
        unnecessary_columns = (set(self.data_frame.columns).difference(MANDATORY_COLUMNS))
        self.data_frame = self.data_frame.drop(list(unnecessary_columns), axis=1)

    def drop_dirty_data(self):
        """
        Removes corrupted rows from data_frame. Removes all rows with NA value and rows from Cost column to prevent
        dividing with zero.
        """
        self.data_frame = self.data_frame[self.data_frame['Cost'] != 0]
        self.data_frame = self.data_frame.dropna()

    def clean_data_frame(self):
        """
        Wrapper method. Calls methods which will prepare data_frame for ROAS calculation.
        """
        self.cast_numeric_columns()
        self.drop_unnecessary_columns()
        self.drop_dirty_data()

    def calculate_roas(self):
        """
        Calculates ROAS values and creates new column of data_frame with this value. Groups data in new DataFrame-s by
        currency code and prepare it for writing in CSV files.
        """
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
