# src/utils/topsis.py

import numpy as np
import pandas as pd

def topsis_score(norm_df: pd.DataFrame, weights: np.ndarray) -> np.ndarray:
    weighted = norm_df * weights
    ideal_best = weighted.max()
    ideal_worst = weighted.min()
    d_pos = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
    score = d_neg / (d_pos + d_neg)
    return score
