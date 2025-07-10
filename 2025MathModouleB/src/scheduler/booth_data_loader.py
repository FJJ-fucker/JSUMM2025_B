import json


def load_booth_schedule(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    days = ['周一', '周二', '周三', '周四', '周五']
    schedule = {}
    for i, day in enumerate(days):
        schedule[day] = {
            'A1': [{'时长': data[day][0]}] * data['展位数'][0],
            'A2': [{'时长': data[day][1]}] * data['展位数'][1],
            'B1': [{'时长': data[day][2]}] * data['展位数'][2],
            'B2': [{'时长': data[day][3]}] * data['展位数'][3]
        }
    return schedule