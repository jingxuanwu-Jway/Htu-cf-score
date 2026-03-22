import requests
import json
import time
from datetime import datetime

# 🌟 在这里配置你们队员的 真实姓名、年级 和 CF Handle
TEAM_MEMBERS = [
    {"name": "侯轶棠", "grade": "2025 级", "handle": "biyuf"},
    {"name": "栗晟皓", "grade": "2024 级", "handle": "lichenghao"},
    {"name": "李宇恒", "grade": "2025 级", "handle": "liyyuu"},
    {"name": "张正正", "grade": "2024 级", "handle": "zhangzhengzheng"},
    {"name": "李昶昊", "grade": "2024 级", "handle": "_HP"},
    {"name": "刘晓玲", "grade": "2023 级", "handle": "Cutee"},
    {"name": "郑于威", "grade": "2023 级", "handle": "zhengxiaomei"},
    {"name": "王义博", "grade": "2025 级", "handle": "wert2353"},
    {"name": "高耀", "grade": "2025 级", "handle": "DAIPUTAO"},
    {"name": "王思哲", "grade": "2025 级", "handle": "warning......"},
    {"name": "李忆恩", "grade": "2025 级", "handle": "jim_jrodan"},
    {"name": "梁敬泽", "grade": "2025 级", "handle": "Ljzmlx"},
    {"name": "赵庆淇", "grade": "2025 级", "handle": "nanhaijuzi"},
    {"name": "余锦昊", "grade": "2024 级", "handle": "yokin"},
    {"name": "朱宏璟", "grade": "2025 级", "handle": "xing_he"},
    {"name": "宁思禹", "grade": "2024 级", "handle": "anoslide"},
    {"name": "段荆玺", "grade": "2025 级", "handle": "buhuizuo"},
    {"name": "李昆鹏", "grade": "2025 级", "handle": "likunpeng"},
    {"name": "申海辰", "grade": "2024 级", "handle": "monesytop1"},
    {"name": "安齐镭", "grade": "2025 级", "handle": "ANQILEI"},
    {"name": "貌克宇", "grade": "2025 级", "handle": "mky0800"},
    {"name": "乔泉程", "grade": "2025 级", "handle": "discovery..."},
    {"name": "张玉桂", "grade": "2024 级", "handle": "zygnb"},
    {"name": "赵晨曦", "grade": "2024 级", "handle": "zxcbpoi123"},
    {"name": "强锦铭", "grade": "2024 级", "handle": "Ayake"},
    {"name": "石熙琛", "grade": "2025 级", "handle": "ttwansuiye"},
    {"name": "李海瑜", "grade": "2024 级", "handle": "iyu0"},
    {"name": "周佳影", "grade": "2025 级", "handle": "XYZz-"},
    {"name": "李昊洋", "grade": "2024 级", "handle": "LHY0715"},
    {"name": "秦旭阳", "grade": "2025 级", "handle": "oldust520"},
    {"name": "刘敬泽", "grade": "2025 级", "handle": "anyidemao"},
    {"name": "孙艺菲", "grade": "2025 级", "handle": "s1fzzz"},
    {"name": "吴静轩", "grade": "2024 级", "handle": "Tbat"},
    {"name": "马傲博", "grade": "2024 级", "handle": "maj_22"},
    {"name": "翟景旺", "grade": "2024 级", "handle": "Yhh7."},
    {"name": "王巍", "grade": "2024 级", "handle": "wwac"},
    {"name": "赵柯行", "grade": "2024 级", "handle": "zhaokx12."},
    {"name": "解天蔚", "grade": "2025 级", "handle": "xtwaaa"},
    {"name": "张稳泉", "grade": "2025 级", "handle": "zwq123180"},
    {"name": "靳宇翔", "grade": "2025 级", "handle": "changf"},
    {"name": "王金燕", "grade": "2025 级", "handle": "w19511030691"},
    {"name": "单鑫亮", "grade": "2024 级", "handle": "YellowDragon"},
    {"name": "李领玉", "grade": "2025 级", "handle": "lilingyu.."},
    {"name": "吴帅甫", "grade": "2023 级", "handle": "ziyvoo"},
    {"name": "曹继喆", "grade": "2024 级", "handle": "cola2100"}
]

def get_user_data(member_info):
    handle = member_info["handle"]
    try:
        # 1. 获取基础信息 (当前分数、最高分数、段位)
        info_resp = requests.get(f"https://codeforces.com/api/user.info?handles={handle}", timeout=10).json()
        if info_resp['status'] != 'OK': 
            return None
        info = info_resp['result'][0]
        time.sleep(0.5)

        # 2. 获取比赛记录 (找最近一场比赛和分数变化)
        rating_resp = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}", timeout=10).json()
        recent_contest = "无"
        rating_change = 0
        if rating_resp['status'] == 'OK' and len(rating_resp['result']) > 0:
            last_contest = rating_resp['result'][-1]
            recent_contest = last_contest['contestName']
            rating_change = last_contest['newRating'] - last_contest['oldRating']
        time.sleep(0.5)

        # 3. 获取提交记录 (统计 AC 题数，去重)
        status_resp = requests.get(f"https://codeforces.com/api/user.status?handle={handle}", timeout=10).json()
        solved = set()
        if status_resp['status'] == 'OK':
            for sub in status_resp['result']:
                if sub.get('verdict') == 'OK':
                    prob = sub.get('problem', {})
                    if 'contestId' in prob and 'index' in prob:
                        solved.add(f"{prob['contestId']}{prob['index']}")
        time.sleep(0.5)

        # 🌟 把姓名和年级一起打包返回
        return {
            "name": member_info["name"],
            "grade": member_info["grade"],
            "handle": handle,
            "rating": info.get('rating', 0),
            "maxRating": info.get('maxRating', 0),
            "rank": info.get('rank', 'unrated'),
            "recentContest": recent_contest,
            "ratingChange": rating_change,
            "solvedCount": len(solved)
        }
    except Exception as e:
        print(f"获取 {handle} 的数据时出错: {e}")
        return None

def main():
    result_data = []
    # 遍历字典列表
    for member in TEAM_MEMBERS:
        print(f"正在抓取 {member['name']} ({member['handle']}) 的数据...")
        data = get_user_data(member)
        if data:
            result_data.append(data)
            
    # 按照当前 Rating 从高到低排序
    result_data.sort(key=lambda x: x['rating'], reverse=True)

    output = {
        "last_update": datetime.now().isoformat(),
        "users": result_data
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("数据更新完成并保存至 data.json")

if __name__ == "__main__":
    main()
