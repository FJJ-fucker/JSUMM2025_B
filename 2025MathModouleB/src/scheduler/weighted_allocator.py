def allocate_booths_weighted(booth_schedule, enterprise_df, score_map):
    """
    使用综合评分进行加权分配。
    分两步：
    - 先满足所有企业的最小需求
    - 剩余资源按企业评分比例分配
    """
    # 初始化
    demand = {
        row['企业代号']: {
            'remaining': row['需求小时数'],
            'min_required': row['需求小时数'] - row['可允许不足小时数'],
            'allocated': 0
        } for _, row in enterprise_df.iterrows()
    }

    assignment = {}
    # 第一步：先满足最低需求
    for day, areas in booth_schedule.items():
        assignment[day] = {area: [] for area in areas}
        for area, booths in areas.items():
            for booth in booths:
                # 寻找尚未满足最小需求的企业
                candidates = [eid for eid, info in demand.items() if info['allocated'] < info['min_required']]
                if not candidates:
                    break
                # 按照缺口大小分配
                candidates.sort(key=lambda eid: (demand[eid]['min_required'] - demand[eid]['allocated']), reverse=True)
                for eid in candidates:
                    if demand[eid]['remaining'] >= booth['时长']:
                        assignment[day][area].append({'企业代号': eid, '时长': booth['时长']})
                        demand[eid]['allocated'] += booth['时长']
                        demand[eid]['remaining'] -= booth['时长']
                        break

    # 第二步：剩余资源按得分加权分配
    for day, areas in booth_schedule.items():
        for area, booths in areas.items():
            for i, booth in enumerate(booths):
                if len(assignment[day][area]) > i:
                    continue  # 已被分配
                # 加权分配
                total_score = sum(score_map[eid] for eid in demand if demand[eid]['remaining'] > 0)
                if total_score == 0:
                    continue
                # 计算每个企业的加权分配意愿
                sorted_eids = sorted(demand.keys(), key=lambda eid: -score_map[eid])
                for eid in sorted_eids:
                    if demand[eid]['remaining'] >= booth['时长']:
                        assignment[day][area].append({'企业代号': eid, '时长': booth['时长']})
                        demand[eid]['allocated'] += booth['时长']
                        demand[eid]['remaining'] -= booth['时长']
                        break
    return assignment
