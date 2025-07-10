# tests/test_scheduler.py
import os
import sys
import pytest
import pandas as pd
from collections import defaultdict

# 添加模块路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.scheduler.booth_data_loader import load_booth_schedule
from src.scheduler.booth_allocator import allocate_booths
from src.scheduler.validate_assignment import validate_schedule

# 准备测试数据路径
JSON_PATH = "../data/booth_schedule.json"
CSV_PATH = "../data/selected_enterprises.csv"

@pytest.fixture(scope="module")
def data():
    booth_info = load_booth_schedule(JSON_PATH)
    enterprise_df = pd.read_csv(CSV_PATH)
    return booth_info, enterprise_df

# 测试是否每天展位总数不超过12
def test_daily_slot_limit(data):
    booth_info, enterprise_df = data
    assignment = allocate_booths(booth_info, enterprise_df)
    for day in assignment:
        total = sum(len(assignment[day][area]) for area in assignment[day])
        assert total <= 12, f"{day} 超过最大展位数: {total} > 12"

# 测试企业总时长不低于最小可接受值
def test_enterprise_minimum_hours(data):
    booth_info, enterprise_df = data
    assignment = allocate_booths(booth_info, enterprise_df)
    assigned_time = defaultdict(float)
    for day in assignment:
        for area in assignment[day]:
            for booth in assignment[day][area]:
                assigned_time[booth['企业代号']] += booth['时长']
    for _, row in enterprise_df.iterrows():
        eid = row['企业代号']
        required = row['需求小时数']
        gap = row['可允许不足小时数']
        min_required = required - gap
        assert assigned_time[eid] >= min_required, f"企业{eid} 分配不足: {assigned_time[eid]} < {min_required}"

# 测试 validate_schedule 不抛出异常
def test_validate_assignment_passes(data):
    booth_info, enterprise_df = data
    assignment = allocate_booths(booth_info, enterprise_df)
    validate_schedule(assignment, enterprise_df)  # 不应抛出 AssertionError

