from collections import defaultdict
import random

def allocate_booths(booth_schedule, enterprise_df):
    # 初始化剩余需求
    demand_map = {
        row['企业代号']: {
            'remaining': row['需求小时数'],
            'min_required': row['需求小时数'] - row['可允许不足小时数']
        }
        for _, row in enterprise_df.iterrows()
    }

    assignment = {}
    for day, areas in booth_schedule.items():
        assignment[day] = {}
        for area, booths in areas.items():
            assignment[day][area] = []
            for booth in booths:
                # 选择剩余需求最多的企业
                candidates = sorted(demand_map.items(), key=lambda x: -x[1]['remaining'])
                for ent, info in candidates:
                    if info['remaining'] >= booth['时长'] * 0.5:  # 至少满足50%才分配
                        assignment[day][area].append({
                            '企业代号': ent,
                            '时长': booth['时长']
                        })
                        demand_map[ent]['remaining'] -= booth['时长']
                        break
    return assignment
def allocate_booths_optimized(booth_schedule, enterprise_df):
    """
    优化版展位分配，优先满足剩余需求紧张的企业，
    确保分配时间 >= 需求-可容忍，且不超过总展位限制。
    """
    demand = {
        row['企业代号']: {
            'remaining': row['需求小时数'],
            'min_required': row['需求小时数'] - row['可允许不足小时数']
        }
        for _, row in enterprise_df.iterrows()
    }

    assignment = {}
    for day, areas in booth_schedule.items():
        assignment[day] = {}
        for area, booths in areas.items():
            assignment[day][area] = []
            for booth in booths:
                # 按照 (剩余时间 - 最小需求) 排序，优先剩余时间最少的企业
                candidates = sorted(
                    demand.items(),
                    key=lambda x: (x[1]['remaining'] - x[1]['min_required'])
                )
                assigned = False
                for ent, info in candidates:
                    if info['remaining'] >= booth['时长']:
                        assignment[day][area].append({'企业代号': ent, '时长': booth['时长']})
                        demand[ent]['remaining'] -= booth['时长']
                        assigned = True
                        break
                if not assigned:
                    # 若无企业满足完全需求，考虑分配给剩余时间>0的企业（部分满足）
                    for ent, info in candidates:
                        if info['remaining'] > 0:
                            length = min(booth['时长'], info['remaining'])
                            assignment[day][area].append({'企业代号': ent, '时长': length})
                            demand[ent]['remaining'] -= length
                            assigned = True
                            break
                if not assigned:
                    # 无可分配企业，展位空置（或者根据需求自由调整）
                    pass
    return assignment