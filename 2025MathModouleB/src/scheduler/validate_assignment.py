from collections import defaultdict

def validate_schedule(assignment, enterprise_df):
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
        assert assigned_time[eid] >= min_required, f"企业{eid}分配不足：{assigned_time[eid]} < {min_required}"