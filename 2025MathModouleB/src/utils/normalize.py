# src/utils/normalize.py

import numpy as np
import pandas as pd

def min_max_normalize(df: pd.DataFrame) -> pd.DataFrame:
    return (df - df.min()) / (df.max() - df.min())

def reverse_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    df_copy = df.copy()
    for col in columns:
        df_copy[col] = 1 - df_copy[col]
    return df_copy
