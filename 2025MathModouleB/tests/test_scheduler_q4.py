import pytest
import pandas as pd
from collections import defaultdict
from src.scheduler.booth_data_loader import load_booth_schedule
from src.scheduler.weighted_allocator import allocate_booths_weighted
from src.utils.selection import calculate_scores
from src.scheduler.validate_assignment import validate_schedule
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
@pytest.fixture(scope="module")
def q4_data():
    enterprise_df = pd.read_csv("../data/selected_enterprises.csv")
    booth_schedule = load_booth_schedule("../data/booth_schedule.json")
    enterprise_info = pd.read_csv("../data/enterprise_info.csv")
    selected_ids = enterprise_df["企业编号"].tolist()
    filtered_info = enterprise_info[enterprise_info["企业编号"].isin(selected_ids)]
    score_map = calculate_scores(filtered_info)
    code_to_id = dict(zip(enterprise_df['企业代号'], enterprise_df['企业编号']))
    score_map_code = {
        code: score_map[code_to_id[code]]
        for code in enterprise_df['企业代号']
    }
    return booth_schedule, enterprise_df,score_map_code

def test_total_booths_limit(q4_data):
    schedule, enterprise_df, score_map_code = q4_data
    assignment = allocate_booths_weighted(schedule, enterprise_df, score_map_code)
    for day in assignment:
        total = sum(len(assignment[day][area]) for area in assignment[day])
        assert total <= 12, f"{day} 展位超过12个"

def test_meet_min_requirements(q4_data):
    schedule, enterprise_df, score_map = q4_data
    assignment = allocate_booths_weighted(schedule, enterprise_df, score_map)
    validate_schedule(assignment, enterprise_df)

