import requests
import json
import time
from datetime import datetime

# 🌟 在这里填入你们队员的 Codeforces Handle
HANDLES = ["ziyvoo", "biyuf", "lichenhao", "liyyuu", "zhangzhengzheng", "_HP", "Cutee", "zhengxiaomei", "wert2353", "DAIPUTAO", "warning...", "jim_jrodan", "Ljzmlx", "南海橘子", "yokin", "xing_he", "anoslide", "buhuizuo", "likunpeng", "monesytop1", "ANQILEI", "mky0800", "discovery…", "zygnb", "zxcbpoi123", "Ayake", "ttwansuiye", "iyu0", "XYZz-", "LHY0715", "anyudemao", "s1fzzz", "Tbat", "maj_22", "Yhh7.", "wwac", "zhaokx12.", "xtwaaa", "zwq123180", "changf", "w19511030691", "1122333423"] 

def get_user_data(handle):
    try:
        # 1. 获取基础信息 (当前分数、最高分数、段位)
        info_resp = requests.get(f"https://codeforces.com/api/user.info?handles={handle}", timeout=10).json()
        if info_resp['status'] != 'OK': 
            return None
        info = info_resp['result'][0]
        time.sleep(0.5) # 防止请求过快被封

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
                        # 用 比赛ID+题号 作为唯一标识，例如 "1234A"
                        solved.add(f"{prob['contestId']}{prob['index']}")
        time.sleep(0.5)

        return {
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
    for h in HANDLES:
        print(f"正在抓取 {h} 的数据...")
        data = get_user_data(h)
        if data:
            result_data.append(data)
            
    # 按照当前 Rating 从高到低排序
    result_data.sort(key=lambda x: x['rating'], reverse=True)

    # 导出为 JSON，并记录更新时间 (使用 ISO 格式方便前端处理)
    output = {
        "last_update": datetime.now().isoformat(),
        "users": result_data
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("数据更新完成并保存至 data.json")

if __name__ == "__main__":
    main()
