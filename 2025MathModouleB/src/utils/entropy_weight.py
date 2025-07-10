# src/utils/entropy_weight.py

import numpy as np
import pandas as pd

def calculate_entropy_weight(norm_df: pd.DataFrame) -> np.ndarray:
    P = norm_df / norm_df.sum(axis=0)
    E = -np.nansum(P * np.log(P + 1e-12), axis=0) / np.log(len(norm_df))
    d = 1 - E
    w = d / d.sum()
    return w
