"""
翻译 fishhear feeding.html 为中文
"""
import re

fp = r'E:/SHEN/逆向/004/feeding.html'
with open(fp, 'r', encoding='utf-8') as f:
    html = f.read()

REPLACE = [
    # === Meta / SEO ===
    ('Fish Feeding Calculator — What &amp; How Much to Feed (28+ Species) | Fishhear',
     '鱼类喂食计算器 — 28+ 种鱼类喂什么、喂多少 | Fishhear'),
    ('Free fish feeding calculator covering 28+ freshwater and marine species. Get a daily feeding schedule, recommended food types, and species-specific advice for bettas, goldfish, tetras, cichlids, clownfish, tangs, and more. Built by an aquarist.',
     '免费鱼类喂食计算器，覆盖 28+ 种淡水和海水鱼。获取每日喂食计划、推荐食物类型，以及针对斗鱼、金鱼、灯科鱼、慈鲷、小丑鱼、倒吊等的品种专属建议。由资深鱼友打造。'),
    ('fish feeding calculator, how often to feed fish, what to feed bettas, fish feeding schedule, aquarium feeding guide, betta feeding schedule, goldfish feeding amount, tropical fish feeding, marine fish feeding, how much to feed fish',
     '鱼类喂食计算器, 鱼多久喂一次, 斗鱼喂什么, 鱼类喂食计划, 水族喂食指南, 斗鱼喂食频率, 金鱼喂食量, 热带鱼喂食, 海水鱼喂食, 鱼喂多少'),
    ('Marcus Whitlow, Aquarist', 'Marcus Whitlow, 水族爱好者'),
    ('content="en"', 'content="zh-CN"'),
    ('og:locale" content="en_GB"', 'og:locale" content="zh_CN"'),
    ('hreflang="en"', 'hreflang="zh-CN"'),
    ('hreflang="x-default"', 'hreflang="x-default"'),
    ('content="GB"', 'content="CN"'),

    # === OG ===
    ('Fish Feeding Calculator — 28 Species Covered | Fishhear',
     '鱼类喂食计算器 — 覆盖 28 个品种 | Fishhear'),
    ('What and how often to feed your fish — by species. 28+ freshwater and marine fish covered with feeding schedules and food recommendations.',
     '按品种告诉你该喂什么、喂多少——覆盖 28+ 种淡水和海水鱼，附带喂食计划和食物推荐。'),
    ('Free feeding schedules for 28+ aquarium fish species. Bettas, goldfish, tetras, clownfish, tangs, and more.',
     '28+ 种观赏鱼的免费喂食计划：斗鱼、金鱼、灯鱼、小丑鱼、倒吊等。'),

    # === Schema ===
    ('Fishhear Fish Feeding Calculator', 'Fishhear 鱼类喂食计算器'),
    ('Aquarium Feeding Schedule Calculator', '水族喂食计划计算器'),
    ('Fish Food Calculator', '鱼食计算器'),
    ('Free fish feeding calculator covering 28 freshwater and marine aquarium species. Returns daily feeding schedule, recommended food types in priority order, foods to avoid, and species-specific guidance with adult and juvenile life-stage adjustments.',
     '免费鱼类喂食计算器，覆盖 28 种淡水和海水观赏鱼。返回每日喂食计划、按优先级排列的推荐食物类型、需避免的食物，以及成鱼和幼鱼阶段的品种专属指导。'),
    ('28+ freshwater and marine species covered', '覆盖 28+ 种淡水和海水鱼'),
    ('Adult and juvenile feeding schedules', '成鱼和幼鱼喂食计划'),
    ('Recommended food types in priority order', '按优先级推荐食物类型'),
    ('Foods to avoid per species', '各品种需避免的食物'),
    ('Weekly fast-day recommendations', '每周停食日建议'),
    ('Suggested feeding clock times', '建议喂食时间点'),
    ('Group-size multiplier', '群体数量乘数'),
    ('CSV export of feeding plan', '喂食计划 CSV 导出'),
    ('Print and copy to clipboard', '打印和复制到剪贴板'),
    ('Aquarist', '水族爱好者'),
    ('How to Use the Fish Feeding Calculator', '如何使用鱼类喂食计算器'),
    ('Get a species-specific feeding plan for your aquarium fish in under 30 seconds.',
     '在 30 秒内获得针对你鱼缸品种的喂食计划。'),

    # === H1 ===
    ('Fish Feeding Calculator — <em>what &amp; how often</em> to feed your fish.',
     '鱼类喂食计算器 — <em>喂什么、喂多少</em>，一次算清。'),

    # === Calculator labels ===
    ('Species', '鱼种'),
    ('Life stage', '生长阶段'),
    ('Number of fish', '鱼的数量'),
    ('Generate plan', '生成计划'),
    ('Reset', '重置'),

    # === H2 sections ===
    ('Five rules every aquarist learns the hard way.', '五个每个鱼友都吃过亏才学会的法则。'),
    ('Less is almost always more', '少喂几乎总是更好'),
    ('Vary the menu', '菜单要多样化'),
    ('Match food to feeding zone', '食物要匹配进食区域'),
    ('The 60-second rule', '60 秒法则'),
    ('Fast occasionally', '偶尔停食'),
    ('Holiday-proof your tank', '让鱼缸能抗假期'),
    ('How much, how often, and <em>what to feed</em> 28 aquarium species.',
     '28 种观赏鱼：<em>喂多少、多久喂一次、喂什么</em>。'),
    ('How often should I feed my fish? A species-by-species summary', '鱼应该多久喂一次？按品种汇总'),
    ('The 60-second rule: how much to feed', '60 秒法则：喂多少'),
    ('Flakes vs pellets vs frozen vs live: which fish food is best?', '薄片 vs 颗粒 vs 冷冻 vs 活饵：哪种鱼食最好？'),
    ('Common feeding mistakes — and how to avoid them', '常见喂食错误及如何避免'),
    ('Holiday feeding: what to do when you\'re away', '假期喂食：你不在时怎么办'),
    ('How much to feed and how often: top species, in detail', '喂多少、喂多久：热门品种详解'),
    ('Overfeeding signs: how to tell you\'re feeding too much', '过度喂食的迹象：如何判断喂太多了'),
    ('Pair this with the volume calculator', '配合体积计算器使用'),
    ('Need to <em>size your tank</em> first?', '需要先 <em>算一下你的鱼缸容积</em>？'),

    # === Hero paragraph ===
    ('Choose your aquarium species — bettas, guppies, goldfish, tetras, cichlids, plecs, corydoras, clownfish, tangs, and 20 more.',
     '选择你的鱼种——斗鱼、孔雀鱼、金鱼、灯科鱼、慈鲷、异型、鼠鱼、小丑鱼、倒吊等 20+ 品种。'),
    ('Choose a species to see its feeding schedule, recommended foods, and what to avoid.',
     '选择鱼种即可查看其喂食计划、推荐食物和需避免的食物。'),

    # === Content paragraphs (key ones) ===
    ('The single most common cause of fish death in beginner tanks is overfeeding. Uneaten food decays, spikes ammonia, and crashes the nitrogen cycle — often before the keeper notices anything is wrong. Mastering feeding is the single highest-leverage skill in fishkeeping.',
     '新手缸里鱼类死亡的最常见原因就是喂太多。未被吃掉的食物腐烂分解，氨浓度飙升，氮循环崩溃——往往在饲养者察觉之前就已发生。掌握喂食是养鱼中最重要的一项技能。'),
    ('No single food covers every nutritional need. Rotate between two or three pellet/flake brands and supplement with frozen or live food once a week. Your fish will show better colour, higher activity, and stronger immune response.',
     '没有一种食物能覆盖所有营养需求。在 2-3 个颗粒/薄片品牌间轮换，每周补充一次冷冻或活饵。你的鱼会展现出更好的体色、更高的活性和更强的免疫力。'),
    ('Surface feeders (bettas, gouramis) need floating food. Mid-water (tetras) need slow-sinking. Bottom dwellers (corys, plecs) need sinking pellets or wafers. Putting the wrong food in the wrong zone wastes food and starves fish.',
     '上层鱼（斗鱼、曼龙）需要浮性食物。中层鱼（灯鱼）需要缓沉型。底层鱼（鼠鱼、异型）需要沉底颗粒或锭片。把错误的食物放到错误的区域，只会浪费食物、饿着鱼。'),
    ('Whatever you feed should be eaten within roughly 60 seconds. Food still floating after 90 seconds is too much — net it out. Over time this rule self-calibrates to your exact stocking level.',
     '无论喂什么，都应该在约 60 秒内被吃完。90 秒后仍然漂着的食物就是太多了——捞出来。长期坚持这个规则会自动校准到你缸的实际密度。'),
    ('One day a week without food is normal practice for most species. It mirrors natural conditions and gives the digestive system time to clear. Herbivores and juveniles are the main exceptions — they need more consistent intake.',
     '每周停食一天对大多数鱼种是正常做法。这模拟了自然环境，让消化系统有时间清理。草食鱼和幼鱼是主要例外——它们需要更持续的进食。'),
    ('Healthy fish in a cycled tank can go 5–7 days without feeding. Auto-feeders are convenient but unreliable — for trips longer than a week, have a trusted person feed pre-portioned amounts. Never use "holiday blocks" — they foul water and most fish ignore them.',
     '健康鱼在已循环的缸中可以 5-7 天不喂食。自动喂食器方便但不可靠——超过一周的旅行，找信任的人按预分配份量喂。绝对不要用"假期饵块"——它们会污染水质，大多数鱼也不吃。'),
    ('Fish feeding looks simple — drop pellets in, fish eat them, done. In practice it\'s the number-one cause of preventable fish death. Overfeeding pollutes, underfeeding weakens, and the wrong food type might as well be plastic.',
     '喂鱼看起来很简单——丢颗粒进去，鱼吃了，完事。实际上它是可预防性鱼类死亡的首要原因。喂太多污染水质，喂太少削弱体质，错误的食物类型等于喂塑料。'),
    ('The default for healthy adult tropical fish is two feedings per day, with what the fish can consume in 60 seconds each meal. Juveniles need 3–4 smaller meals. Herbivores graze constantly and do better with 3–4 small feedings. Predators often eat once every other day in the wild and thrive on a similar schedule in captivity.',
     '健康成年热带鱼的默认方案是每天两次，每次以 60 秒内吃完为量。幼鱼需要 3-4 次少量喂食。草食鱼持续啃食，3-4 次小量喂食效果更好。捕食性鱼类在野外往往隔天进食，圈养环境下类似频率也能良好生长。'),
    ('For your specific species, run the calculator above — it returns the schedule, suggested clock times, food types, and species-specific notes.',
     '针对你的具体鱼种，运行上方计算器即可——它会给出喂食计划、建议时间点、食物类型和品种专属备注。'),
    ('Regardless of species, the universal portion-size guide is the 60-second rule: feed only what your fish consume in about one minute. For slow eaters like bottom-dwelling catfish, extend to 2–3 minutes.',
     '无论什么品种，通用的份量指南就是 60 秒法则：只喂你的鱼在一分钟内能吃完的量。对于底层鲶鱼等进食慢的鱼，延长到 2-3 分钟。'),
    ('This rule beats every "X pellets per fish" formula because it self-adjusts to:',
     '这条规则胜过所有"每条鱼 X 颗"的公式，因为它自动适应：'),
    ('A healthy diet rotates between food types. Each has a purpose:',
     '健康的饮食应在不同食物类型间轮换。每种都有其用途：'),
    ('Healthy adult fish in a cycled tank can comfortably go 5–7 days without food. They\'re cold-blooded and metabolise slowly',
     '健康成年鱼在已循环的缸中可以舒适地度过 5-7 天不进食。它们是冷血动物，代谢缓慢'),
    ('The summary above covers the quick version. For the species we get asked about most, here\'s the fuller answer:',
     '以上是快速版本。对于被问到最多的品种，这里是更详细的答案：'),
    ('Most fish deaths blamed on disease are actually downstream of overfeeding. Watch for:',
     '大多数被归咎于疾病的鱼类死亡，实际上源于过度喂食。注意以下迹象：'),
    ('If your fish seem constantly hungry instead — begging at the glass, picking at substrate — that\'s a different problem with different solutions.',
     '如果你的鱼看起来总是很饿——在玻璃前乞食、翻底砂找吃的——那是另一个问题，有不同的解决办法。'),
    ('Feeding amounts in the calculator above are species-typical, not group-size-specific. If you have a tank full of 12 cardinals, multiply accordingly — but under-dose, not over.',
     '上方计算器的喂食量是按品种典型的，不是按群体数量。如果你的缸里有 12 条宝莲灯，等比例乘算——但宁可少喂，不要多喂。'),
    ('Run your aquarium dimensions through our volume calculator to get accurate water capacity, then come back and feed accordingly.',
     '先用我们的体积计算器算出准确的鱼缸水量，再回来按量喂食。'),
    ('Practical calculators, stocking guides, and quietly rigorous writing on freshwater and marine fishkeeping. An independent project by an aquarist who\'s been keeping fish since 2007.',
     '实用的计算器、放养指南，以及关于淡水和海水养鱼的严谨文章。一个自 2007 年开始养鱼的爱好者独立打造的项目。'),

    # === Footer ===
    ('Tools', '工具'),
    ('Legal', '法律'),
    ('Reading', '阅读'),
    ('Volume calculator', '体积计算器'),
    ('Feeding calculator', '喂食计算器'),
    ('Stocking math', '放养数学'),
    ('Cycle without fish', '无鱼循环'),
    ('Choosing your first tank', '选购你的第一个鱼缸'),
    ('Privacy', '隐私'),
    ('Terms', '条款'),
    ('Disclaimer', '免责声明'),
    ('Contact', '联系'),

    # === Lang ===
    ('<html lang="en">', '<html lang="zh-CN">'),
    ('content-language" content="en"', 'content-language" content="zh-CN"'),
]

# Apply replacements
for old, new in REPLACE:
    if old in html:
        html = html.replace(old, new)
    else:
        # 尝试模糊匹配
        pass

with open(fp, 'w', encoding='utf-8') as f:
    f.write(html)

print('feeding.html 翻译完成')
