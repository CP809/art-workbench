# -*- coding: utf-8 -*-
"""画画工作台 · 每日内容生成器
GitHub Actions 每天北京时间 07:30 运行：
  1. 按日期轮换生成「每日一练」画题
  2. 从四级词库按天轮换取 30 个单词
  3. 写入 daily.js（window.DAILY_DATA）
手机端 PWA 缓存旧数据，用户点「更新」按钮才拉取新版。
"""
import json
import time
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
WORDS_PER_DAY = 30

# ---------------- 四级高频词库（word|词性|释义） ----------------
WORD_BANK = """
abandon|v.|放弃，抛弃
ability|n.|能力，才能
abnormal|adj.|不正常的
aboard|adv./prep.|在船（车、机）上
absorb|v.|吸收；使专心
abstract|adj.|抽象的 n.摘要
abundant|adj.|丰富的，充裕的
accelerate|v.|加速，促进
accent|n.|口音；重音
access|n.|接近；通道 v.存取
accompany|v.|陪伴，伴随
accomplish|v.|完成，实现
account|n.|账户；描述 v.解释
accurate|adj.|准确的，精确的
accuse|v.|指责，控告
achieve|v.|达到，完成
acknowledge|v.|承认；答谢
acquire|v.|获得，学到
adapt|v.|适应；改编
addition|n.|加，加法；增加物
adequate|adj.|足够的，适当的
adjust|v.|调整，调节
admire|v.|钦佩，赞赏
admit|v.|承认；准许进入
adopt|v.|采用；收养
advance|v./n.|前进；预付
advantage|n.|优势，有利条件
adventure|n.|冒险，奇遇
advertise|v.|为……做广告
advocate|v./n.|提倡；拥护者
affect|v.|影响；感动
afford|v.|买得起；负担得起
agency|n.|代理处，机构
aggressive|adj.|侵略的；好斗的
agreement|n.|协议，一致
agriculture|n.|农业
aircraft|n.|飞机，航空器
alarm|n.|警报；闹钟 v.使惊恐
album|n.|相册；专辑
alcohol|n.|酒精，酒
alike|adj./adv.|相似的（地）
allocate|v.|分配，拨给
allowance|n.|津贴，零用钱
alter|v.|改变，更改
alternative|n./adj.|替代方案（的）
ambition|n.|雄心，抱负
amount|n.|数量，总额
analyze|v.|分析
ancestor|n.|祖先，祖宗
ancient|adj.|古代的，古老的
angle|n.|角度，角
anniversary|n.|周年纪念日
announce|v.|宣布，宣告
annual|adj.|每年的，年度的
anticipate|v.|预期，预料
anxiety|n.|焦虑，忧虑
anxious|adj.|焦虑的；渴望的
apart|adv.|分开，相隔
apartment|n.|公寓
apologize|v.|道歉
apparent|adj.|显然的；表面上的
appeal|v./n.|呼吁；吸引力
appearance|n.|出现；外貌
appetite|n.|食欲，胃口
applaud|v.|鼓掌，喝彩
appliance|n.|（家用）电器
applicant|n.|申请人
application|n.|申请；应用
appoint|v.|任命，指定
appreciate|v.|欣赏；感激
approach|v./n.|接近；方法
appropriate|adj.|适当的
approve|v.|批准；赞成
approximately|adv.|大约，近似
architect|n.|建筑师
argue|v.|争论；主张
arise|v.|出现，产生
arrange|v.|安排，整理
arrest|v./n.|逮捕
artificial|adj.|人工的，人造的
assemble|v.|集合；装配
assess|v.|评估，评定
asset|n.|资产；宝贵的人（物）
assign|v.|分配，指派
assist|v.|协助，帮助
assume|v.|假定；承担
assure|v.|保证，确保
astonish|v.|使惊讶
athlete|n.|运动员
atmosphere|n.|大气；气氛
attach|v.|附上；使依恋
attain|v.|达到，获得
attitude|n.|态度，看法
attorney|n.|律师
attract|v.|吸引
attribute|v./n.|归因于；属性
audience|n.|观众，听众
author|n.|作者
authority|n.|权威；当局
automatic|adj.|自动的
available|adj.|可获得的；有空的
avenue|n.|大街；途径
average|adj./n.|平均的（数）
avoid|v.|避免，躲开
award|n./v.|奖赏；授予
aware|adj.|意识到的
awful|adj.|可怕的，极坏的
awkward|adj.|尴尬的；笨拙的
bachelor|n.|单身汉；学士
background|n.|背景
bacteria|n.|细菌
balance|n./v.|平衡
ban|v./n.|禁止
bare|adj.|赤裸的；仅有的
bargain|n./v.|便宜货；讨价还价
barrier|n.|障碍，屏障
basis|n.|基础，根据
battery|n.|电池
battle|n./v.|战斗，斗争
beam|n.|横梁；光束
behalf|n.|代表（on behalf of）
behave|v.|表现，举止
behavior|n.|行为，举止
belief|n.|信念，信仰
belong|v.|属于（belong to）
bend|v./n.|弯曲
benefit|n./v.|利益；有益于
bet|v./n.|打赌
betray|v.|背叛，出卖
beyond|prep.|超出；在……那边
bid|v./n.|出价；投标
billion|num.|十亿
bind|v.|捆绑，束缚
bitter|adj.|苦的；痛苦的
blade|n.|刀刃，叶片
blame|v./n.|责备
blank|adj./n.|空白的（处）
blanket|n.|毛毯，毯子
blast|n./v.|爆炸
bleed|v.|流血
blend|v./n.|混合
bloom|v./n.|开花
boast|v./n.|自夸，夸耀
boil|v.|煮沸，沸腾
bold|adj.|大胆的；粗体的
bomb|n./v.|炸弹；轰炸
bond|n.|纽带；债券
bonus|n.|奖金，红利
boom|n./v.|繁荣，激增
border|n.|边界，边缘
bore|v.|使厌烦
bother|v.|打扰，麻烦
bounce|v.|弹跳，反弹
boundary|n.|边界，分界线
branch|n.|树枝；分支
brand|n.|品牌
breed|v.|繁殖；饲养 n.品种
breeze|n.|微风
brief|adj.|简短的
brilliant|adj.|才华横溢的；明亮的
broad|adj.|宽的，广阔的
browse|v.|浏览
budget|n./v.|预算
bulk|n.|巨大体积；大部分
bunch|n.|束，串，一群
burden|n.|负担
burst|v./n.|爆发，爆裂
cabinet|n.|橱柜；内阁
cable|n.|电缆；有线电视
calculate|v.|计算，估计
campaign|n./v.|运动，战役
cancel|v.|取消
candidate|n.|候选人，应试者
capability|n.|能力，才能
capacity|n.|容量；能力
capture|v./n.|捕获，夺取
carbon|n.|碳
career|n.|职业，生涯
cargo|n.|货物
carpet|n.|地毯
carriage|n.|四轮马车；车厢
carrier|n.|运输公司；带菌者
casual|adj.|随意的；偶然的
catalog|n.|目录
category|n.|种类，类别
cease|v./n.|停止，终止
cell|n.|细胞；小房间；电池
cement|n.|水泥 v.巩固
ceremony|n.|典礼，仪式
certain|adj.|确定的；某一
chain|n.|链条；连锁
challenge|n./v.|挑战
chamber|n.|房间；议院
champion|n.|冠军
channel|n.|频道；海峡；途径
character|n.|性格；角色；汉字
characteristic|n./adj.|特征（的）
charge|v./n.|收费；指控；充电
charity|n.|慈善，慈善机构
charm|n.|魅力 v.使陶醉
chart|n.|图表，海图
chase|v./n.|追逐，追赶
cheat|v./n.|欺骗；作弊
cheer|v.|欢呼；使振奋
chemical|adj./n.|化学的（制品）
chess|n.|国际象棋
chew|v.|咀嚼
chief|adj./n.|首要的；首领
choke|v.|窒息，噎住
circuit|n.|电路；环行
circulate|v.|循环，流通
circumstance|n.|环境，情况
cite|v.|引用，举例
civil|adj.|公民的；国内的
claim|v./n.|声称；索赔
clarify|v.|澄清，阐明
classic|adj./n.|经典的（作品）""".strip()

BANK = []
for line in WORD_BANK.splitlines():
    w, pos, mean = line.split("|")
    BANK.append({"w": w, "pos": pos, "mean": mean})

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

def pick_words():
    start = (day_index() * WORDS_PER_DAY) % len(BANK)
    group = []
    for i in range(WORDS_PER_DAY):
        group.append(BANK[(start + i) % len(BANK)])
    return group

def pick_prompt():
    return PROMPTS[day_index() % len(PROMPTS)]

def build():
    now = datetime.now(TZ)
    data = {
        "date": now.strftime("%Y-%m-%d"),
        "updateTime": now.strftime("%Y-%m-%d %H:%M"),
        "updateTs": int(time.time()),
        "prompt": pick_prompt(),
        "words": pick_words(),
        "wordsTotal": len(BANK),
    }
    js = "/* 画画工作台 · 每日数据（由 daily_update.py 生成，勿手改） */\n"
    js += "window.DAILY_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n"
    with open("daily.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("已生成 daily.js：", data["date"], "画题：", data["prompt"]["title"], "单词：", WORDS_PER_DAY, "个")

if __name__ == "__main__":
    build()
