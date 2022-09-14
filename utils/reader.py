import pandas as pd
from configs import PATH_DATA_INPUT, PATH_STATICS_GLOBALS

def get_input_df(file: str, sep=";", low_memory=False, n_rows=None) -> pd.DataFrame:
    path = PATH_DATA_INPUT / "{}.csv".format(file)

    return pd.read_csv(path, sep=sep, low_memory=low_memory, nrows=n_rows)

def get_catalog():
    return pd.read_excel(PATH_STATICS_GLOBALS / "catalog.xlsx")

