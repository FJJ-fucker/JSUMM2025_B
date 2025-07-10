# src/tests/test_selection.py

import pandas as pd
from  src.utils.selection import select_top_enterprises

def test_selection_top7_shape():
    df = pd.read_csv('../data/enterprise_info.csv')
    result = select_top_enterprises(df, top_n=7)
    assert result.shape[0] == 7

def test_selection_scores_descend():
    df = pd.read_csv('../data/enterprise_info.csv')
    result = select_top_enterprises(df, top_n=7)
    scores = result['综合得分'].values
    assert all(scores[i] >= scores[i+1] for i in range(len(scores)-1))

