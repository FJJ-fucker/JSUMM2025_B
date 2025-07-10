# src/utils/selection.py

import pandas as pd
from .normalize import min_max_normalize, reverse_columns
from .entropy_weight import calculate_entropy_weight
from .topsis import topsis_score


def select_top_enterprises(df: pd.DataFrame, top_n=7, method='entropy_topsis') -> pd.DataFrame:
    df_copy = df.copy()
    cols = df_copy.columns[1:]  # x1 ~ x9
    norm_df = min_max_normalize(df_copy[cols])
    norm_df = reverse_columns(norm_df, ['x9_投诉率'])

    weights = calculate_entropy_weight(norm_df)
    score = topsis_score(norm_df, weights)

    df_copy['综合得分'] = score
    df_copy_sorted = df_copy.sort_values(by='综合得分', ascending=False).reset_index(drop=True)
    return df_copy_sorted.iloc[:top_n]
def calculate_scores(df: pd.DataFrame) -> dict:
    """
    输入企业指标 DataFrame（x1 ~ x9），输出 企业编号 => 综合得分 的字典
    """
    df_copy = df.copy()
    cols = df_copy.columns[1:]  # x1 ~ x9
    norm_df = min_max_normalize(df_copy[cols])
    norm_df = reverse_columns(norm_df, ['x9_投诉率'])

    weights = calculate_entropy_weight(norm_df)
    scores = topsis_score(norm_df, weights)
    return dict(zip(df_copy['企业编号'], scores))
