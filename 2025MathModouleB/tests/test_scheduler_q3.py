# tests/test_scheduler_q3.py

import os
import sys
import pytest
import pandas as pd
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.scheduler.booth_data_loader import load_booth_schedule
from src.scheduler.booth_allocator import allocate_booths_optimized
from src.scheduler.validate_assignment import validate_schedule

JSON_PATH = "../data/booth_schedule.json"
CSV_PATH = "../data/selected_enterprises.csv"

@pytest.fixture(scope="module")
def increased_demand_data():
    booth_info = load_booth_schedule(JSON_PATH)
    enterprise_df = pd.read_csv(CSV_PATH)
    enterprise_df['需求小时数'] = (enterprise_df['需求小时数'] * 1.10).round(2)
    return booth_info, enterprise_df

def test_daily_limit_q3(increased_demand_data):
    booth_info, enterprise_df = increased_demand_data
    assignment = allocate_booths_optimized(booth_info, enterprise_df)
    for day in assignment:
        total = sum(len(assignment[day][area]) for area in assignment[day])
        assert total <= 12, f"{day} 分配展位数超过限制: {total}"

def test_enterprise_min_hours_q3(increased_demand_data):
    booth_info, enterprise_df = increased_demand_data
    assignment = allocate_booths_optimized(booth_info, enterprise_df)
    assigned_time = defaultdict(float)
    for day in assignment:
        for area in assignment[day]:
            for booth in assignment[day][area]:
                assigned_time[booth['企业代号']] += booth['时长']
    for _, row in enterprise_df.iterrows():
        eid = row['企业代号']
        min_required = row['需求小时数'] - row['可允许不足小时数']
        assert assigned_time[eid] >= min_required, f"企业 {eid} 分配不足: {assigned_time[eid]} < {min_required}"

def test_validate_passes_q3(increased_demand_data):
    booth_info, enterprise_df = increased_demand_data
    assignment = allocate_booths_optimized(booth_info, enterprise_df)
    validate_schedule(assignment, enterprise_df)

