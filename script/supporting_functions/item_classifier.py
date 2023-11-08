
# This supporting function classifies item type and reduces manual workload.
# However, the final item type used will be manually screened and corrected for accuracies.
# NEVER RELY ON this function to automatically classify Chinese art items without proper domain knowledge.

calligraphy_primary = [
    "书法",
    "篆书",
    "行书",
    "草书",
    "楷书",
    "隶书",
    "五言",
    "七言",
    "八言",
    "诗句",
    "序",
    "题跋",
    "行草",
    "福字",

]

drawing_primary = [
    "图",
    "画",
    "扇骨",
    "人物",
    "山水",
    "花",
    "四屏",

]

drawing_secondary = [
    "牡丹",
    "塔",
    "秋",
    "菊",
    "荷",
    "鸟",
    "虫",
    "岁",
    "鸡",
    "女",
    "山",
    "溪",
    "松",
    "石",
    "泉",
    "鹰",
    "雪",
    "鸳",
    "罗汉",
    "风",
    "涧",
    "竹",
    "马",
    "红",
    "梅",
    "塘",
    "香",
    "少",
    "林",
    "气",
    "柳",
    "蝉",
    "春",
    "帆",
    "作",
    "湖",
    "蜻",
    "蜓",
    "荷",
    "鹤",
    "鹂",
    "藤",
    "景",
    "富",
    "牛",
    "鱼",
    "乡",
    "江",
    "岩",
    "翠",
    "桃",
    "雨",
    "暮",
    "驼",
    "塘",
    "烟",
    "枝",
    "烟",
    "雀",
    "乾坤",
    "仙",
    "蔷薇",
    "鸦",
    "木",
    "野",
    "亭",
    "秋",
    "鹅",
    "冬",
    "夏",
    "雪",
    "猫",
    "瀑",
    "禽",
    "像"

]

ancient_literature_primary = [
    "贴",
    "本",
    "集",
    "藏",
    "册",
    "文稿",
    "院藏",
    "展",
    "初印本",
    "卷",
    "志",
    "纸",
    "书",
    "经",
    "稿",
    "诗稿",
    "珍",
    "信札",
    "帖",
    "印谱",
    "期刊",
    "碑",
    "札",
    "出版",

]


# classifies items according to the keyword lists and scores
def item_classifier(item_name):
    calligraphy_score = 0
    drawing_score = 0
    ancient_literature_score = 0
    for i in calligraphy_primary:
        if i in item_name:
            calligraphy_score += 15

    for i in drawing_primary:
        if i in item_name:
            drawing_score += 8

    for i in drawing_secondary:
        if i in item_name:
            drawing_score += 5

    for i in ancient_literature_primary:
        if i in item_name:
            ancient_literature_score += 11

    if max(calligraphy_score, drawing_score, ancient_literature_score) < 5:
        return "others"
    elif calligraphy_score > drawing_score:
        if calligraphy_score > ancient_literature_score:
            return "calligraphy"
        else:
            return "ancient_literature"
    elif drawing_score > ancient_literature_score:
        return "drawing"
    else:
        return "ancient_literature"
