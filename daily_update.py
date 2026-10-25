# -*- coding: utf-8 -*-
"""美术台 · 每日内容生成器
GitHub Actions 每天北京时间 07:30 运行：
  1. 按日期轮换生成「每日一练」画题
  2. 写入 daily.js（window.DAILY_DATA）
手机端 PWA 缓存旧数据，用户点「更新」按钮才拉取新版。
"""
import json
import time
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))

# ---------------- 每日一练（按天轮换） ----------------
PROMPTS = [
    {"tag": "动态速写", "title": "30 秒 × 10 张，只画动态线", "detail": "不看细节，一笔概括人物运动趋势，画完挑出最有动感的一张。"},
    {"tag": "光影素描", "title": "一个白瓷杯的五大调子", "detail": "重点找明暗交界线，反光不许超过灰面，画完眯眼检查暗部是否统一。"},
    {"tag": "头发分组", "title": "3 组不同发型的分组示意", "detail": "先画头球体，再罩 5~7 个大组，用 Z 字形穿插表现前后遮挡。"},
    {"tag": "布料褶皱", "title": "搭在椅背上的外套", "detail": "先标出受力点和支撑点，再画 3 组大褶皱 + 2 组小褶皱，其余省略。"},
    {"tag": "手专项", "title": "自己的左手，3 个角度", "detail": "手掌看成盒子、四指看成圆柱，先画剪影判断好不好看，再填结构。"},
    {"tag": "色彩练习", "title": "同一静物换暖调画一张", "detail": "限定 3 色：1 主色 + 2 邻近色，收尾用 1 个点缀色，面积不超过 10%。"},
    {"tag": "色彩练习", "title": "逆光小场景 15 分钟", "detail": "主体压暗、边缘留一条亮边光、背景提亮，只靠明度差把形立起来。"},
    {"tag": "构图", "title": "同一物体画 3 个明度小稿", "detail": "拇指大的黑白稿，只管构图和明暗分布，选最抓眼的一张。"},
    {"tag": "角色设计", "title": "纯黑剪影设计一个角色", "detail": "涂黑后还能认出职业和性格才算成立，夸张一个标志性特征就够。"},
    {"tag": "氛围感", "title": "给旧图加光斑和环境色", "detail": "逆光处加浮尘光斑、暗部加环境色反光、受光面带光源色，前后对比存档。"},
    {"tag": "审美提升", "title": "看 10 张图，各写一句好在哪", "detail": "问三个问题：视线先落在哪、为什么被吸引、用了什么对比。"},
    {"tag": "速写练习", "title": "课间 / 通勤随手速写 3 张", "detail": "画身边的人和物，每张不超过 3 分钟，练观察不练完成度。"},
]

def day_index():
    now = datetime.now(TZ)
    epoch = datetime(2026, 1, 1, tzinfo=TZ)
    return (now - epoch).days

def build():
    now = datetime.now(TZ)
    data = {
        "date": now.strftime("%Y-%m-%d"),
        "updateTime": now.strftime("%Y-%m-%d %H:%M"),
        "updateTs": int(time.time()),
        "prompt": PROMPTS[day_index() % len(PROMPTS)],
    }
    js = "/* 美术台 · 每日数据（由 daily_update.py 生成，勿手改） */\n"
    js += "window.DAILY_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n"
    with open("daily.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("已生成 daily.js：", data["date"], "画题：", data["prompt"]["title"])

if __name__ == "__main__":
    build()
