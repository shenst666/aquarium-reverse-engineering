"""翻译 feeding.min.js 中的物种数据和 UI 文本"""
import re

fp = r'E:/SHEN/逆向/004/feeding.min.js'
with open(fp, 'r', encoding='utf-8') as f:
    js = f.read()

REPLACE = [
    # === 分类/食性 ===
    ("category: 'freshwater'", "category: '淡水'"),
    ("category: 'marine'", "category: '海水'"),
    ("category: 'pond'", "category: '池塘'"),
    ("diet: 'carnivore'", "diet: '肉食'"),
    ("diet: 'omnivore'", "diet: '杂食'"),
    ("diet: 'herbivore'", "diet: '草食'"),

    # === 生长阶段 ===
    ("Life stage", "生长阶段"),
    ("adult", "成鱼"),
    ("juvenile", "幼鱼"),
    ("Choose a species to see its feeding schedule", "选择鱼种查看喂食计划"),

    # === UI 标签 ===
    ("'Schedule'", "'喂食计划'"),
    ("'times per day'", "'次 / 天'"),
    ("'Per feeding'", "'每次喂量'"),
    ("'Daily total'", "'每日总量'"),
    ("'Recommended foods (priority order)'", "'推荐食物（按优先级）'"),
    ("'Foods to avoid'", "'需避免的食物'"),
    ("'Species notes'", "'品种备注'"),
    ("'Weekly fast day recommended'", "'建议每周停食一天'"),
    ("'Yes'", "'是'"),
    ("'No'", "'否'"),

    # === 物种名 ===
    ("Betta (Siamese fighting fish)", "斗鱼（泰国斗鱼）"),
    ("Guppy", "孔雀鱼"),
    ("Molly", "玛丽鱼"),
    ("Platy", "月光鱼"),
    ("Neon Tetra", "霓虹灯鱼"),
    ("Cardinal Tetra", "宝莲灯鱼"),
    ("Rummy Nose Tetra", "红鼻剪刀"),
    ("Ember Tetra", "琥珀灯鱼"),
    ("Harlequin Rasbora", "三角灯鱼"),
    ("Zebra Danio", "斑马鱼"),
    ("White Cloud Mountain Minnow", "白云金丝"),
    ("Cherry Barb", "樱桃灯"),
    ("Goldfish (Fancy varieties)", "金鱼（文种/蛋种）"),
    ("Goldfish (Common/Comet)", "金鱼（草金/彗星）"),
    ("Angelfish (Freshwater)", "神仙鱼（淡水）"),
    ("Discus", "七彩神仙"),
    ("German Blue Ram", "蓝宝石凤凰"),
    ("Apistogramma", "阿卡西短鲷"),
    ("Oscar", "地图鱼"),
    ("Convict Cichlid", "斑马慈鲷"),
    ("African Cichlids (Mbuna)", "非洲慈鲷（岩栖类）"),
    ("African Cichlids (Peacock/Hap)", "非洲慈鲷（孔雀/单色鲷）"),
    ("Corydoras Catfish", "鼠鱼"),
    ("Bristlenose Pleco", "红眼胡子异型"),
    ("Common Pleco", "普通异型"),
    ("Otocinclus", "小精灵"),
    ("Kuhli Loach", "蛇仔鱼"),
    ("Clown Loach", "小丑鳅"),
    ("Dwarf Gourami", "矮珍珠马甲"),
    ("Pearl Gourami", "珍珠马甲"),
    ("Honey Gourami", "蜂蜜马甲"),
    ("Swordtail", "剑尾鱼"),
    ("Endler's Livebearer", "安德拉斯孔雀"),
    ("Clownfish", "小丑鱼"),
    ("Royal Gramma", "皇家鲈"),
    ("Firefish Goby", "火鱼虾虎"),
    ("Yellow Tang", "黄倒吊"),
    ("Blue Tang", "蓝倒吊"),
    ("Cleaner Wrasse", "医生鱼"),
    ("Mandarin Dragonet", "青蛙鱼"),
    ("Six Line Wrasse", "六线龙"),
    ("Bangaii Cardinalfish", "巴厘天使"),
    ("Flame Angelfish", "火焰仙"),
    ("Coral Beauty Angelfish", "珊瑚美人神仙"),
    ("Pajama Cardinalfish", "睡衣天使"),
    ("Watchman Goby", "守望虾虎"),
    ("Lawnmower Blenny", "食藻鳚"),
    ("Anthias", "海金鱼"),

    # === 喂食模式 ===
    ("'3-4 pellets'", "'3-4 颗'"),
    ("'6-8 pellets'", "'6-8 颗'"),
    ("'2-3 pellets'", "'2-3 颗'"),
    ("'6-9 pellets'", "'6-9 颗'"),
    ("'Pinch of flakes'", "'一小撮薄片'"),
    ("'Crushed flakes'", "'碾碎的薄片'"),
    ("'What they eat in 30 sec'", "'30 秒内能吃完的量'"),
    ("'Small frequent feeds'", "'少量多次'"),
    ("'Generous pinch'", "'稍多的薄片'"),
    ("'30-second rule'", "'30 秒法则'"),
    ("'Small pinch'", "'一小撮'"),
    ("'20-30 sec consumption'", "'20-30 秒内吃完'"),
    ("'Tiny meals'", "'极小份'"),
    ("'Quarter block'", "'1/4 块'"),
    ("'Half block'", "'半块'"),
    ("'1-2 sinking wafers'", "'1-2 片沉底锭片'"),
    ("'1 sinking wafer'", "'1 片沉底锭片'"),
    ("'1-2 algae wafers'", "'1-2 片藻片'"),
    ("'1 algae wafer'", "'1 片藻片'"),
    ("'1-2 sinking pellets'", "'1-2 颗沉底颗粒'"),
    ("'1 sinking pellet'", "'1 颗沉底颗粒'"),
    ("'2-3 small sinking pellets'", "'2-3 颗小型沉底颗粒'"),
    ("'What they eat in 60 sec'", "'60 秒内能吃完的量'"),
    ("'What they consume in 2 min'", "'2 分钟内能吃完的量'"),
    ("'2 minutes worth'", "'2 分钟的量'"),
    ("'What they eat in 2 min'", "'2 分钟内能吃完的量'"),
    ("'Frozen cube (thawed)'", "'冷冻块（解冻后）'"),
    ("'Half frozen cube (thawed)'", "'半块冷冻（解冻后）'"),
    ("'Quarter frozen cube (thawed)'", "'1/4 冷冻块（解冻后）'"),
    ("'Small amount of gel food'", "'少量凝胶食物'"),
    ("'Pea-sized gel portion'", "'豌豆大的凝胶'"),
    ("'Nori sheet (1/4)'", "'1/4 张海苔'"),
    ("'Nori sheet (1/2)'", "'半张海苔'"),
    ("'Nori sheet (whole)'", "'整张海苔'"),

    # === 食物名 ===
    ("High-protein betta pellets", "高蛋白斗鱼颗粒"),
    ("Frozen bloodworms (2x/week)", "冷冻红虫（每周2次）"),
    ("Frozen brine shrimp", "冷冻丰年虾"),
    ("Live blackworms (treat)", "活黑虫（零食）"),
    ("Generic tropical flakes", "通用热带鱼薄片"),
    ("Dried bloodworms (cause bloat)", "干红虫（导致腹胀）"),
    ("Quality tropical flakes", "优质热带鱼薄片"),
    ("Crushed pellets", "碾碎的颗粒"),
    ("Frozen daphnia", "冷冻水蚤"),
    ("Spirulina flakes (1x/week)", "螺旋藻薄片（每周1次）"),
    ("Large pellets (mouth too small)", "大颗粒（嘴太小）"),
    ("Vegetable flakes", "蔬菜薄片"),
    ("Spirulina pellets", "螺旋藻颗粒"),
    ("Blanched spinach/courgette", "焯水菠菜/西葫芦"),
    ("Pure protein diets (cause bloat)", "纯蛋白饮食（导致腹胀）"),
    ("Tropical community flakes", "热带鱼通用薄片"),
    ("Blanched vegetables", "焯水蔬菜"),
    ("Micro-pellets", "微颗粒"),
    ("Frozen cyclops", "冷冻剑水蚤"),
    ("Bloodworms in excess", "过量红虫"),
    ("Sinking goldfish pellets", "沉底金鱼颗粒"),
    ("Blanched peas (deshelled)", "焯水豌豆（去壳）"),
    ("Gel food", "凝胶食物"),
    ("Spirulina", "螺旋藻"),
    ("Floating goldfish sticks", "浮性金鱼条"),
    ("Frozen bloodworms", "冷冻红虫"),
    ("Sinking carnivore pellets", "沉底肉食颗粒"),
    ("Frozen krill (2x/week)", "冷冻磷虾（每周2次）"),
    ("Frozen mussel (chopped)", "冷冻贻贝（切碎）"),
    ("Feeder fish (quarantine first)", "饲料鱼（先检疫）"),
    ("Beef heart mix (sparingly)", "牛心汉堡（偶尔）"),
    ("Algae wafers", "藻片"),
    ("Blanched courgette/cucumber", "焯水西葫芦/黄瓜"),
    ("Fresh vegetables (romaine, peas)", "新鲜蔬菜（生菜、豌豆）"),
    ("Meaty wafers", "荤食锭片"),
    ("Sinking omnivore pellets", "沉底杂食颗粒"),
    ("Frozen tubifex", "冷冻颤蚓"),
    ("Frozen mosquito larvae", "冷冻孑孓"),
    ("Live blackworms", "活黑虫"),
    ("Sinking micro-pellets", "沉底微颗粒"),
    ("Sinking herbivore pellets", "沉底草食颗粒"),
    ("Repashy gel food", "Repashy 凝胶"),
    ("Fresh spinach on a clip", "夹子上的新鲜菠菜"),
    ("Marine flake food", "海水鱼薄片"),
    ("Frozen mysis shrimp", "冷冻糠虾"),
    ("Marine pellets (small)", "海水鱼小颗粒"),
    ("Nori (dried seaweed on a clip)", "海苔（夹子上的干海藻）"),
    ("Marine algae sheets", "海水藻片"),
    ("Frozen marine mix", "冷冻海水鱼混合"),
    ("Frozen copepods", "冷冻桡足类"),
    ("Live copepods (ideal)", "活桡足类（理想）"),
    ("Frozen rotifers", "冷冻轮虫"),
    ("Frozen angel formula", "冷冻神仙鱼配方"),
    ("Frozen sponge-based food", "冷冻海绵食物"),
    ("Marine sinking pellets", "海水沉底颗粒"),
    ("Frozen chopped squid", "冷冻切碎鱿鱼"),

    # === 提示文本 ===
    ("No leftover food", "无残留食物"),
    ("What they eat in 60 seconds", "60 秒内能吃完的量"),
    ("For your group of", "对于你的"),
    ("multiply per-feed amounts above.", "条鱼，将上方每次喂量乘以相应倍数。"),
    ("Watch for leftover food after 60-90 seconds and reduce if needed.", "注意观察 60-90 秒后是否有剩余食物，如有则减少喂量。"),
    ("One fast day per week recommended.", "建议每周停食一天。"),
    ("Calculate first to export.", "请先计算再导出。"),
    ("Fishhear Feeding Plan", "Fishhear 喂食计划"),
    ("Generated", "生成时间"),
    ("Species", "品种"),
    ("Category", "分类"),
    ("Diet", "食性"),
    ("Number of fish", "鱼的数量"),
    ("Feedings per day", "每日喂食次数"),
    ("Per-feed amount", "每次喂量"),
    ("Daily total guideline", "每日总量建议"),
    ("Weekly fast day recommended", "建议每周停食"),
    ("Recommended foods (priority order)", "推荐食物（按优先级）"),
    ("Foods to avoid", "需避免的食物"),
    ("Species notes", "品种备注"),

    # === 物种备注 ===
    ("Bettas are surface feeders with small stomachs. One day of fasting per week prevents constipation, a leading cause of swim-bladder issues.",
     "斗鱼是上层进食者，胃很小。每周停食一天可预防便秘——便秘是导致鳔病的主要原因。"),
    ("Continuous feeders that benefit from small, varied meals. Include vegetable matter (spirulina) to prevent constipation in fancy strains.",
     "持续进食型，少量多样喂食效果好。加入植物性食物（螺旋藻）可预防品系变异种的便秘。"),
    ("Mollies are heavy on vegetable matter — at least 60% of diet should be plant-based. Algae grazing is natural and beneficial.",
     "玛丽鱼非常需要植物性食物——至少 60% 应为植物来源。啃藻是自然且有益的行为。"),
    ("Hardy and undemanding. Vary diet between protein and vegetable matter for best colour development.",
     "强壮且不挑剔。在蛋白和蔬菜之间轮换饮食可获得最佳体色。"),
    ("Mid-water feeders with small mouths. Food should sink slowly through the water column; sinking pellets get ignored.",
     "中层进食者，嘴小。食物应缓慢沉入水柱；沉底颗粒会被忽略。"),
    ("Visual feeders; need food that moves or drifts. Overfeeding causes rapid water fouling in small tanks.",
     "视觉进食者；需要活动或飘动的食物。小缸过度喂食会迅速污染水质。"),

    # === 常见错误 ===
    ("'Feeding plan for'", "'喂食计划：'"),
    ("' per feeding'", "' / 次'"),
    ("' daily total'", "' / 天总量'"),
    ("\"No leftover food\"", "\"无残留食物\""),
    ("\"What they eat in 60 seconds\"", "\"60 秒内能吃完的量\""),
    # Group-size 提示
    ("For your group of ", "对于你的 "),
    (" fish, multiply per-feed amounts above. Watch for leftover food and reduce if needed.", " 条鱼，将每次喂量乘上相应倍数。观察剩余食物情况，如有剩余则减少。"),
    ("One fast day per week recommended.", "建议每周停食一天。"),
]

for old, new in REPLACE:
    if old in js:
        js = js.replace(old, new)
        # print(f'✅ {old[:60]}')
    else:
        pass  # print(f'❌ {old[:60]}')

# 翻译剩余的模式匹配
# 通用的 leftover / fast 提示
js = js.replace('No leftover food', '无残留食物')
js = js.replace('What they eat in 60 seconds', '60 秒内能吃完的量')

# 兜底：把所有 "No leftover food" 和 "What they eat in 60 sec" 等模式替换
js = js.replace('\"What they eat in 60 seconds\"', '\"60 秒内能吃完的量\"')
js = js.replace('\"No leftover food\"', '\"无残留食物\"')
js = js.replace('\"What they eat in 60 sec\"', '\"60 秒内能吃完的量\"')
js = js.replace('\"What they consume in 2 min\"', '\"2 分钟内能吃完的量\"')
js = js.replace('\"30-second rule\"', '\"30 秒法则\"')
js = js.replace('\"2 minutes worth\"', '\"2 分钟的量\"')

with open(fp, 'w', encoding='utf-8') as f:
    f.write(js)

print('feeding.min.js 翻译完成')
