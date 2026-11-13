import os
import zipfile
import xml.etree.ElementTree as ET
import re
import html
import json
import urllib.parse

DOC_DIR = '/Users/brainzhang/work/rootze/landingpage/resource/ProductBrochure/Special Purpose Vehicles/产品介绍文档'
IMG_DIR = '/Users/brainzhang/work/rootze/landingpage/images/products/vehicles'
OUT_DIR = '/Users/brainzhang/work/rootze/landingpage/products/vehicles'
MAIN_PAGE = '/Users/brainzhang/work/rootze/landingpage/products/special-vehicles.html'
I18N_FILE = '/Users/brainzhang/work/rootze/landingpage/js/i18n.js'

os.makedirs(OUT_DIR, exist_ok=True)

CATEGORIES = [
    {
        'id': 'cat-tanker-trucks',
        'heading_id': 'heading-tanker-trucks',
        'collapse_id': 'collapse-tanker-trucks',
        'title_en': 'Fuel & Fluid Tanker Trucks',
        'title_zh': '燃油及流体运输罐车',
        'icon': 'ion-ios-water',
        'badge_class': 'badge-primary',
        'badge_en': 'Fuel Tanker Truck',
        'badge_zh': '燃油运输罐车',
        'desc_en': 'Rigid commercial chassis tanker trucks (15.1 m³ – 30.3 m³) for gasoline, diesel, crude oil, and chemical fluids.',
        'desc_zh': '依托东风、欧曼、豪沃、汕德卡等商用车底盘打造的单桥至四桥运油车与危化品罐车（15.1 m³ – 30.3 m³），专用于汽油、柴油、原油及石脑油的高效合规运输。',
        'show': True
    },
    {
        'id': 'cat-tanker-semis',
        'heading_id': 'heading-tanker-semis',
        'collapse_id': 'collapse-tanker-semis',
        'title_en': 'Fuel & Fluid Tanker Semi-trailers',
        'title_zh': '燃油及流体运输半挂车',
        'icon': 'ion-ios-speedometer',
        'badge_class': 'badge-primary',
        'badge_en': 'Fuel Tanker Semi-trailer',
        'badge_zh': '燃油运输半挂车',
        'desc_en': 'High-capacity aluminum alloy and carbon steel semi-trailers (37.6 m³ – 49.9 m³) with gooseneck and straight frame designs.',
        'desc_zh': '大容量轻量化铝合金及碳钢方圆罐/圆罐半挂车（37.6 m³ – 49.9 m³），采用直梁及变截面鹅颈承载大梁设计，满足远途干线燃油与化工流体运输需求。',
        'show': False
    },
    {
        'id': 'cat-reefer',
        'heading_id': 'heading-reefer',
        'collapse_id': 'collapse-reefer',
        'title_en': 'Cold-Chain Refrigerated Trucks & Semi-trailers',
        'title_zh': '冷链冷藏运输车与冷藏半挂车',
        'icon': 'ion-ios-snow',
        'badge_class': 'badge-info',
        'badge_en': 'Refrigerated Vehicle',
        'badge_zh': '冷链冷藏车',
        'desc_en': 'Advanced polyurethane insulated reefers, 45ft semi-trailers (air suspension/leaf spring) and urban delivery box trucks.',
        'desc_zh': '采用无冷桥闭式聚氨酯一体发泡保温箱体与食品级复合蒙皮，涵盖 45 英尺一体式/分体式冷藏半挂车（空气悬架/重载板簧）及城配轻型冷藏车。',
        'show': False
    },
    {
        'id': 'cat-engineering',
        'heading_id': 'heading-engineering',
        'collapse_id': 'collapse-engineering',
        'title_en': 'Engineering Tipper Bodies & Special Vehicles',
        'title_zh': '重型工程自卸车与特种上装',
        'icon': 'ion-ios-construct',
        'badge_class': 'badge-secondary',
        'badge_en': 'Engineering Vehicle',
        'badge_zh': '工程特种车辆',
        'desc_en': 'Heavy-duty U-shaped tipper superstructures, wear-resistant alloy bodies, smart IoT covers, and municipal utility vehicles.',
        'desc_zh': '重型U型工程渣土自卸车上装、NM450/T700高强耐磨钢箱体、智能物联网（IoT）抑尘环保顶盖及定制化工程车底盘方案。',
        'show': False
    }
]

SPEC_KEYS = [
    ('spv_key.model', 'Product Model', '产品公告型号', ['model', '产品型号']),
    ('spv_key.dims', 'Overall Dimensions (L×W×H, mm)', '整车外形尺寸（长×宽×高，mm）', ['overall dimensions', '外形尺寸']),
    ('spv_key.tank_dims', 'Tank Dimensions (mm)', '罐体外形尺寸（mm）', ['tank dimensions', '罐体尺寸']),
    ('spv_key.box_dims', 'Cargo Box Dimensions (L×W×H, mm)', '货厢内部尺寸（长×宽×高，mm）', ['cargo box dimensions', '箱体尺寸']),
    ('spv_key.body_size', 'Cargo Body Dimensions (L×W×H, mm)', '车厢内部尺寸（长×宽×高，mm）', ['cargo body size', '车厢尺寸']),
    ('spv_key.gvw', 'Gross Vehicle Weight (GVW)', '整车总质量', ['gross vehicle weight', 'gvw', '总质量']),
    ('spv_key.curb', 'Curb Weight', '整备质量（自重）', ['curb weight', '整备质量']),
    ('spv_key.payload', 'Rated Payload', '额定载质量', ['rated payload', '额定载质量']),
    ('spv_key.wheelbase', 'Wheelbase (mm)', '轴距（mm）', ['wheelbase', '轴距']),
    ('spv_key.tank_total', 'Tank Total Capacity', '罐体总容量', ['tank total capacity', '罐体总容量']),
    ('spv_key.tank_eff', 'Effective Volume', '罐体有效容积', ['effective volume', '有效容积']),
    ('spv_key.max_density', 'Max. Density of Approved Medium', '准运介质最大允许密度', ['max. density', '准运介质最大密度']),
    ('spv_key.medium', 'Transported Medium', '运输介质', ['transported medium', '运输介质']),
    ('spv_key.tank_type', 'Tank Cross-Section & Structure', '罐体截面与结构型式', ['tank type', '罐体类型']),
    ('spv_key.design_code', 'Tank Design Code', '罐体设计代码', ['tank design code', '罐体设计代码']),
    ('spv_key.chassis', 'Chassis Model', '配套底盘型号', ['chassis', '底盘']),
    ('spv_key.engine', 'Engine Model / Power', '发动机型号/动力', ['engine model', '发动机型号']),
    ('spv_key.batch', 'MIIT Announcement Batch', '工信部公告批次', ['miit announcement batch', '公告批次']),
    ('spv_key.cert', '3C Certificate No.', '国家强制性3C认证编号', ['3c certificate', '3c证书编号']),
    ('spv_key.box_const', 'Box Construction', '厢体生产工艺', ['box construction', '箱体生产工艺']),
    ('spv_key.insulation', 'Insulation Material', '保温隔热材质', ['insulation material', '保温层材质']),
    ('spv_key.outer_skin', 'Outer Skin Material', '外蒙皮材质', ['outer skin', '外蒙皮材质']),
    ('spv_key.inner_skin', 'Inner Skin Material', '内蒙皮材质', ['inner skin', '内蒙皮材质']),
    ('spv_key.floor', 'Floor Type', '底板通风结构', ['floor type', '底板类型']),
    ('spv_key.suspension', 'Suspension System', '悬架承载系统', ['suspension', '悬架', '悬挂']),
    ('spv_key.plate', 'Plate Thickness (mm)', '板材厚度（mm）', ['plate thickness', '板厚']),
    ('spv_key.main_mat', 'Main Structural Material', '主要结构材料', ['main material', '主要材料']),
    ('spv_key.body_weight', 'Body Weight', '上装自重', ['body weight', '上装自重']),
    ('spv_key.closed_height', 'Closed Height (mm)', '闭合高度（mm）', ['closed height', '闭合高度']),
    ('spv_key.cylinder', 'Hydraulic Cylinder', '举升液压油缸', ['hydraulic cylinder', '油缸']),
    ('spv_key.body_struct', 'Body Structure', '车厢后门结构', ['body structure', '车厢结构'])
]

PRODUCTS = [
    # Fuel Tanker Trucks (9 models)
    ('15.1立方欧曼牌运油车_15.1m3 Auman Fuel Tanker Truck.docx', 'fuel-tanker-15m3-auman', 'fuel-tanker-15m3-auman.jpg', 'cat-tanker-trucks', '15.1m³ Auman Fuel Tanker Truck', '15.1m³ 欧曼运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('18.1立方易燃液体罐式运输车_18.1m3 Flammable Liquid Tank Truck.docx', 'fuel-tanker-18m3-flammable', 'fuel-tanker-18m3-flammable.jpg', 'cat-tanker-trucks', '18.1m³ Flammable Liquid Tank Truck (Crude Oil)', '18.1m³ 易燃液体运输罐车 (原油)', 'badge-primary', 'Flammable Liquid Tank Truck'),
    ('21.4立方易燃液体罐式运输车_21.4m3 Flammable Liquid Tank Truck.docx', 'fuel-tanker-21m3-flammable', 'fuel-tanker-21m3-flammable.jpg', 'cat-tanker-trucks', '21.4m³ Flammable Liquid Tank Truck (Naphtha)', '21.4m³ 易燃液体运输罐车 (石脑油)', 'badge-primary', 'Flammable Liquid Tank Truck'),
    ('21立方东风易燃液体罐式运输车_21m3 Dongfeng Flammable Liquid Tank Truck.docx', 'fuel-tanker-21m3-dongfeng', 'fuel-tanker-21m3-dongfeng.png', 'cat-tanker-trucks', '21m³ Dongfeng Flammable Liquid Tank Truck (Naphtha)', '21m³ 东风易燃液体运输罐车 (石脑油)', 'badge-primary', 'Flammable Liquid Tank Truck'),
    ('25.8立方欧曼牌铝合金运油车_25.8m3 Auman Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-258m3-auman-alloy', 'fuel-tanker-258m3-auman-alloy.png', 'cat-tanker-trucks', '25.8m³ Auman Aluminum Alloy Fuel Tanker Truck', '25.8m³ 欧曼铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('26.5立方欧曼牌运油车_26.5m3 Auman Fuel Tanker Truck.docx', 'fuel-tanker-265m3-auman', 'fuel-tanker-265m3-auman.jpg', 'cat-tanker-trucks', '26.5m³ Auman Fuel Tanker Truck', '26.5m³ 欧曼运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('26立方东风牌铝合金运油车_26m3 Dongfeng Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-26m3-dongfeng-alloy', 'fuel-tanker-26m3-dongfeng-alloy.jpg', 'cat-tanker-trucks', '26m³ Dongfeng Aluminum Alloy Fuel Tanker Truck', '26m³ 东风铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('26立方铝合金运油车_26m3 Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-26m3-alloy', 'fuel-tanker-26m3-alloy.jpg', 'cat-tanker-trucks', '26m³ Sitrak Aluminum Alloy Fuel Tanker Truck', '26m³ 汕德卡铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('30.3立方东风牌铝合金运油车_30.3m3 Dongfeng Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-303m3-dongfeng-alloy', 'fuel-tanker-303m3-dongfeng-alloy.jpg', 'cat-tanker-trucks', '30.3m³ Dongfeng Aluminum Alloy Fuel Tanker Truck', '30.3m³ 东风铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    
    # Fuel Tanker Semi-trailers (11 models)
    ('37.6立方欧曼牌铝合金运油半挂车_37.6m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-376m3-auman-alloy', 'semi-tanker-376m3-auman-alloy.png', 'cat-tanker-semis', '37.6m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '37.6m³ 欧曼铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('38.5立方欧曼牌铝合金运油半挂车_38.5m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-385m3-auman', 'semi-tanker-385m3-auman.jpg', 'cat-tanker-semis', '38.5m³ Auman Fuel Tanker Semi-trailer', '38.5m³ 欧曼运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('40.4立方欧曼牌铝合金运油半挂车_40.4m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-404m3-auman-alloy', 'semi-tanker-404m3-auman-alloy.jpg', 'cat-tanker-semis', '40.4m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '40.4m³ 欧曼铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('42立方铝合金运油半挂车_42m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-42m3-alloy', 'semi-tanker-42m3-alloy.png', 'cat-tanker-semis', '42m³ Aluminum Alloy Fuel Tanker Semi-trailer', '42m³ 铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('43立方铝合金易燃液体罐式运输半挂车_43m3 Aluminum Alloy Flammable Liquid Tank Semi-trailer(2).docx', 'semi-tanker-43m3-flammable-a', 'semi-tanker-43m3-flammable-a.jpg', 'cat-tanker-semis', '43m³ Aluminum Alloy Flammable Liquid Tank Semi-trailer (Model A: Ethanol/Solvent)', '43m³ 铝合金易燃液体运输半挂车 (A型 乙醇/溶剂油)', 'badge-primary', 'Flammable Liquid Semi-trailer'),
    ('43立方铝合金易燃液体罐式运输半挂车_43m3 Aluminum Alloy Flammable Liquid Tank Semi-trailer.docx', 'semi-tanker-43m3-flammable-b', 'semi-tanker-43m3-flammable-b.png', 'cat-tanker-semis', '43m³ Aluminum Alloy Flammable Liquid Tank Semi-trailer (Model B: Methanol/Ethanol)', '43m³ 铝合金易燃液体运输半挂车 (B型 甲醇/乙醇)', 'badge-primary', 'Flammable Liquid Semi-trailer'),
    ('45立方铝合金运油半挂车_45m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-45m3-alloy', 'semi-tanker-45m3-alloy.jpg', 'cat-tanker-semis', '45m³ Aluminum Alloy Fuel Tanker Semi-trailer', '45m³ 铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('46.1立方铝合金运油半挂车_46.1m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-461m3-alloy', 'semi-tanker-461m3-alloy.jpg', 'cat-tanker-semis', '46.1m³ Aluminum Alloy Fuel Tanker Semi-trailer (Jet Fuel)', '46.1m³ 铝合金运油半挂车 (航空煤油)', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('47立方欧曼牌铝合金运油半挂车_47m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-47m3-auman-alloy', 'semi-tanker-47m3-auman-alloy.jpg', 'cat-tanker-semis', '47m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '47m³ 欧曼铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('48立方铝合金运油半挂车_48m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-48m3-alloy', 'semi-tanker-48m3-alloy.png', 'cat-tanker-semis', '48m³ Aluminum Alloy Fuel Tanker Semi-trailer', '48m³ 铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('49.9立方欧曼牌铝合金运油半挂车_49.9m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-499m3-auman-alloy', 'semi-tanker-499m3-auman-alloy.jpg', 'cat-tanker-semis', '49.9m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '49.9m³ 欧曼铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    
    # Refrigerated Vehicles (5 models)
    ('欧曼牌冷藏车_Auman Refrigerated Truck.docx', 'reefer-truck-auman', 'reefer-truck-auman.jpg', 'cat-reefer', '4.5T Light-Duty Urban Refrigerated Truck', '4.5吨级 轻型城配冷藏车', 'badge-info', 'Refrigerated Truck'),
    ('8米五十铃冷藏车_8m Isuzu Refrigerated Truck.docx', 'reefer-truck-8m-isuzu', 'reefer-truck-8m-isuzu.jpg', 'cat-reefer', '8m Isuzu Medium-Duty Refrigerated Truck', '8米 五十铃冷藏运输车', 'badge-info', 'Refrigerated Truck'),
    ('45英尺一体式冷藏半挂车（板簧）_45ft Integrated Refrigerated Semi-trailer (Leaf Spring).docx', 'reefer-semi-45ft-leaf-spring', 'reefer-semi-45ft-leaf-spring.jpg', 'cat-reefer', '45ft Integrated Refrigerated Semi-trailer (Leaf Spring)', '45英尺 一体式干线冷藏半挂车 (板簧悬架)', 'badge-info', 'Refrigerated Semi-trailer'),
    ('45英尺一体式冷藏半挂车（空悬）_45ft Integrated Refrigerated Semi-trailer (Air Suspension).docx', 'reefer-semi-45ft-air-suspension', 'reefer-semi-45ft-air-suspension.png', 'cat-reefer', '45ft Integrated High-End Refrigerated Semi-trailer (Air Suspension)', '45英尺 一体式高端冷藏半挂车 (空气悬架)', 'badge-info', 'Refrigerated Semi-trailer'),
    ('45英尺分体式冷藏半挂车_45ft Split-type Refrigerated Semi-trailer.docx', 'reefer-semi-45ft-split', 'reefer-semi-45ft-split.jpg', 'cat-reefer', '45ft Split-Type Multi-Temperature Refrigerated Semi-trailer', '45英尺 分体式多温区冷藏半挂车', 'badge-info', 'Refrigerated Semi-trailer'),
    
    # Engineering Vehicles (3 models)
    ('工程车1_Engineering Vehicle 1.docx', 'engineering-vehicle-1', 'engineering-vehicle-1.png', 'cat-engineering', 'Heavy-Duty U-Box Tipper Superstructure (510L Steel / Electric Cover)', '重型U型自卸车上装 (510L特钢 / 电动密闭顶盖)', 'badge-secondary', 'Engineering Vehicle'),
    ('工程车2_Engineering Vehicle 2.docx', 'engineering-vehicle-2', 'engineering-vehicle-2.jpg', 'cat-engineering', 'Heavy-Duty Engineering Tipper Truck (Custom Chassis & Body)', '重型工程自卸车 (定制底盘与上装工程方案)', 'badge-secondary', 'Engineering Vehicle'),
    ('工程车3_Engineering Vehicle 3.docx', 'engineering-vehicle-3', 'engineering-vehicle-3.jpg', 'cat-engineering', 'Smart Eco U-Box Tipper Superstructure (T700 High-Strength Steel / IoT Cover)', '智能环保U型自卸车上装 (T700高强钢 / 物联网顶盖)', 'badge-secondary', 'Engineering Vehicle')
]

POLISHED_OVERVIEWS = {
    'fuel-tanker-15m3-auman': {
        'zh': '本款 15.1m³ 欧曼运油车（型号 HFV5180GJYBJ15）基于成熟商用车底盘打造，配备高品质碳钢方圆形截面罐体，罐体总容量 15.1 m³（有效容积 14.39 m³）。整车总质量 18,000 kg，额定载重 10,075 kg，专为汽油等轻质燃油的合规安全道路转运而研制。罐内设有多道加强型防荡隔板，整车重心低、行驶稳定性好，全面满足道路危险货物运输标准规范。',
        'en': 'Commercial 15.1m³ fuel tanker truck (Model HFV5180GJYBJ15) engineered on an Auman chassis, equipped with a high-strength carbon steel rounded-rectangular tank with a total capacity of 15.1 m³ (effective volume 14.39 m³). With a gross vehicle weight of 18,000 kg and rated payload of 10,075 kg, it is optimized for safe, compliant highway distribution of gasoline and refined fuels.'
    },
    'fuel-tanker-18m3-flammable': {
        'zh': '本款 18.1m³ 易燃液体运输罐车（型号 HFV5261GRYZZ18）搭载中国重汽豪沃三桥商用车底盘，配备承压耐冲击碳钢方圆形截面罐体，罐体总容量 18.1 m³（有效容积 17.59 m³）。整车总质量 26,000 kg，额定载重达 13.2 吨，专用于原油等重质易燃液体的高可靠性运输，具备优异的抗颠簸性与长途运输安全性。',
        'en': 'Heavy-duty 18.1m³ flammable liquid tank truck (Model HFV5261GRYZZ18) built on a Sinotruk Howo 6x4 chassis with a high-strength carbon steel rounded-rectangular tank. Features a total capacity of 18.1 m³ (effective volume 17.59 m³), a gross vehicle weight of 26,000 kg, and a rated payload of up to 13,260 kg, dedicated to the secure transit of crude oil and viscous flammable liquids.'
    },
    'fuel-tanker-21m3-flammable': {
        'zh': '本款 21.4m³ 易燃液体运输罐车（型号 HFV5260GRYZZ21）采用中国重汽豪沃重卡底盘与高强度碳钢方圆罐结构，总容量 21.4 m³（有效容积 20.78 m³）。整车总质量 26,000 kg，额定载重 13,370 kg，专为石脑油等易燃化工流体安全储运设计，罐顶设防护走台与欧标密封人孔，符合严苛的道路危化品运输技术标准。',
        'en': 'Commercial 21.4m³ flammable liquid tank truck (Model HFV5260GRYZZ21) engineered on a Sinotruk Howo chassis with a reinforced carbon steel tank. Total capacity reaches 21.4 m³ (effective volume 20.78 m³) with a gross vehicle weight of 26,000 kg and rated payload of 13,370 kg, specially configured for naphtha and volatile petrochemical transport.'
    },
    'fuel-tanker-21m3-dongfeng': {
        'zh': '本款 21m³ 东风易燃液体运输罐车（型号 HFV5261GRYEQ6）基于东风三桥重载商用车底盘研制，罐体总容量 21 m³（有效容积 20.4 m³）。整车总质量 26,000 kg，额定载重达 13,870 kg，专用于石脑油及易燃液体原料的中长途转运。底盘性能皮实耐用，罐体管路系统密封可靠，具备卓越的承载力与高经济性运维优势。',
        'en': 'Commercial 21m³ flammable liquid tank truck (Model HFV5261GRYEQ6) engineered on a Dongfeng 6x4 chassis with a carbon steel rounded-rectangular tank. Boasting a total capacity of 21 m³ (effective volume 20.4 m³), gross vehicle weight of 26,000 kg, and rated payload of 13,870 kg, it provides dependable transport for naphtha and petrochemical feedstocks.'
    },
    'fuel-tanker-258m3-auman-alloy': {
        'zh': '本款 25.8m³ 欧曼铝合金运油车（型号 HFV5321GYYBJ6A）采用欧曼四桥高配底盘与 5182/5083 高性能轻量化铝合金方圆截面罐体，总容量 25.8 m³（有效容积 25.1 m³）。整车总质量 32,000 kg，额定载重突破 20.6 吨，适用于柴油、煤油、汽油等多介质多仓运输，罐体自重轻、耐腐蚀性强，实现运力与燃油经济性的最大化。',
        'en': 'Premium 25.8m³ aluminum alloy fuel tanker truck (Model HFV5321GYYBJ6A) built on an Auman 8x4 chassis. Total capacity is 25.8 m³ (effective volume 25.1 m³) with a gross vehicle weight of 32,000 kg and rated payload of 20,620 kg. Designed for multi-compartment haulage of diesel, kerosene, and gasoline, delivering superior fuel economy and corrosion resistance.'
    },
    'fuel-tanker-265m3-auman': {
        'zh': '本款 26.5m³ 欧曼运油车（型号 HFV5320GYYBJ6）搭载欧曼前四后八重型工程底盘，罐体采用优质高强度碳钢方圆截面工艺成型，总容量 26.5 m³（有效容积 25.8 m³）。整车总质量 32,000 kg，额定载重 18,070 kg，专为汽油等石化油品的大批量干线中转打造，结构扎实稳重，底盘通过性与抗扭性能出众。',
        'en': 'Heavy-duty 26.5m³ fuel tanker truck (Model HFV5320GYYBJ6) built on an Auman 8x4 commercial chassis. Outfitted with a durable carbon steel rounded-rectangular tank with a total capacity of 26.5 m³ (effective volume 25.8 m³), gross vehicle weight of 32,000 kg, and rated payload of 18,070 kg for high-volume gasoline and refined petroleum distribution.'
    },
    'fuel-tanker-26m3-dongfeng-alloy': {
        'zh': '本款 26m³ 东风铝合金运油车（型号 HFV5320GYYD6A）选用东风天龙旗舰四桥底盘，搭载优质铝合金方圆形轻量化罐体，总容量 26 m³（有效容积 24.8 m³）。整车总质量 32,000 kg，额定载重量达 20.7 吨，获批运输柴油、煤油及汽油。配置气动海底紧急切断阀与防溢流探头，大幅提升单车运营收益并降低长途运输油耗。',
        'en': 'High-efficiency 26m³ aluminum alloy fuel tanker truck (Model HFV5320GYYD6A) based on the Dongfeng Tianlong 8x4 chassis platform. Featuring a 26 m³ capacity (effective volume 24.8 m³), gross vehicle weight of 32,000 kg, and payload of up to 20,705 kg, it is certified for diesel, kerosene, and gasoline with pneumatic emergency shut-off valves and vapor recovery.'
    },
    'fuel-tanker-26m3-alloy': {
        'zh': '本款 26m³ 汕德卡铝合金运油车（型号 HFV5320GYYZZ6A）基于高端商用重卡中国重汽汕德卡底盘平台研发，匹配 5083/5182 级铝合金方圆罐，总容量 26 m³（有效容积 24.7 m³）。整车总质量 32,000 kg，额定载重高达 20.3 吨，适配汽油、柴油及航空煤油多功能运输，具有极高的出勤可靠性、轻量化减重效益与舒适的驾乘体验。',
        'en': 'Premium 26m³ aluminum alloy fuel tanker truck (Model HFV5320GYYZZ6A) engineered on the Sinotruk Sitrak 8x4 platform. With a total capacity of 26 m³ (effective volume 24.7 m³), gross vehicle weight of 32,000 kg, and rated payload of 20,370 kg, it provides exceptional long-haul reliability and payload efficiency for refined fuel logistics.'
    },
    'fuel-tanker-303m3-dongfeng-alloy': {
        'zh': '本款 30.3m³ 东风铝合金运油车（型号 HFV5321GYYD6A）是单车底盘系列中容积最大的旗舰级运油车，总容量达 30.3 m³（有效容积 28.9 m³）。依托东风天龙重载底盘与轻量化铝合金罐体设计，总质量 32,000 kg，额定载荷 20.2 吨，专为大规模汽油成品油高效直运设计，在法规限定内实现了装载容积的极致利用。',
        'en': 'Flagship 30.3m³ aluminum alloy fuel tanker truck (Model HFV5321GYYD6A), the highest-capacity rigid chassis model in our fleet. Powered by a Dongfeng Tianlong 8x4 chassis with a 30.3 m³ tank (effective volume 28.9 m³), gross vehicle weight of 32,000 kg, and rated payload of 20,265 kg, it maximizes revenue per haul for large-scale refined fuel distribution.'
    },
    'semi-tanker-376m3-auman-alloy': {
        'zh': '本款 37.6m³ 欧曼铝合金运油半挂车（型号 HFV9404GYYB）采用直梁式承载大梁与优质铝合金方圆形截面罐体，罐体总容量 37.6 m³（有效容积 36.5 m³）。整车总质量 40,000 kg，额定载重高达 33.8 吨，获批运载柴油、煤油及汽油。自动化激光拼接罐体焊缝饱满平整，兼备超低整备质量与卓越的抗疲劳抗冲击性能。',
        'en': 'Heavy-duty 37.6m³ aluminum alloy fuel tanker semi-trailer (Model HFV9404GYYB) engineered with a straight-frame chassis and rounded-rectangular tank. Featuring a total capacity of 37.6 m³ (effective volume 36.5 m³), gross vehicle weight of 40,000 kg, and rated payload of 33,800 kg for high-volume diesel, kerosene, and gasoline transport.'
    },
    'semi-tanker-385m3-auman': {
        'zh': '本款 38.5m³ 欧曼运油半挂车（型号 HFV9401GYYB）采用变截面鹅颈承载大梁与高强度碳钢方圆罐结构，总容量 38.5 m³（有效容积 37.4 m³）。整车总质量 40,000 kg，额定载重突破 30 吨，专用于柴油、煤油的大批量长途运输。鹅颈梁结构大幅压低整车重心与迎风阻力，重载高速行驶稳定性尤为突出。',
        'en': 'High-capacity 38.5m³ carbon steel fuel tanker semi-trailer (Model HFV9401GYYB) featuring a gooseneck chassis frame and rounded-rectangular tank. With a total capacity of 38.5 m³ (effective volume 37.4 m³), gross vehicle weight of 40,000 kg, and rated payload of 30,200 kg, it provides a low center of gravity and high highway stability.'
    },
    'semi-tanker-404m3-auman-alloy': {
        'zh': '本款 40.4m³ 欧曼铝合金运油半挂车（型号 HFV9400GYYB）应用轻量化高刚度等高直梁车架，罐体总容量 40.4 m³（有效容积达 40.3 m³）。整车总质量 40,000 kg，额定载重 33.8 吨，专为成品油干线物流深度优化。全铝合金轻量化设计大幅削减自重，实现单趟运载效能与燃油经济性的双重提升。',
        'en': 'High-efficiency 40.4m³ aluminum alloy fuel tanker semi-trailer (Model HFV9400GYYB) built with a straight-frame design and rounded-rectangular tank. Features a total capacity of 40.4 m³ (effective volume 40.3 m³), gross vehicle weight of 40,000 kg, and rated payload of 33,800 kg, delivering optimal payload and reduced tare weight.'
    },
    'semi-tanker-42m3-alloy': {
        'zh': '本款 42m³ 铝合金运油半挂车（型号 HFV9405GYYA）选用耐腐蚀特种铝合金材料成型，采用等高度直梁受力大梁，罐体总容量 42 m³（有效容积 40 m³）。整车总质量 40,000 kg，额定载重达 33.5 吨，可混装或专装汽油、柴油及煤油，安全防爆设施齐全，适用于跨省长途石化干线高频次转运。',
        'en': 'Long-haul 42m³ aluminum alloy fuel tanker semi-trailer (Model HFV9405GYYA) engineered with a straight-frame chassis and corrosion-resistant alloy tank. Total capacity reaches 42 m³ (effective volume 40 m³), with a gross vehicle weight of 40,000 kg and rated payload of 33,500 kg, optimized for multi-product fuel transit.'
    },
    'semi-tanker-43m3-flammable-a': {
        'zh': '本款 43m³ 铝合金易燃液体运输半挂车（A型，型号 HFV9409GRYA）专为乙醇（酒精）、丁醇、丙酮、异丙醇及溶剂油等中低密度易燃有机溶剂研制。采用高强度铝合金圆形承压截面与变截面鹅颈大梁，总容量 43 m³（有效容积 40.9 m³），额定载重 33.6 吨，配备多级阻火器、气动海底切断阀与防静电接地装置，符合危化品 Class 3 极高安全防护等级。',
        'en': 'Specialized 43m³ aluminum alloy flammable liquid tank semi-trailer (Model A, HFV9409GRYA) designed for ethanol, butanol, acetone, isopropanol, and solvent oils. Features a cylindrical pressure-rated tank with a gooseneck frame, total capacity of 43 m³ (effective volume 40.9 m³), gross vehicle weight of 40,000 kg, and rated payload of 33,600 kg.'
    },
    'semi-tanker-43m3-flammable-b': {
        'zh': '本款 43m³ 铝合金易燃液体运输半挂车（B型，型号 HFV9407GRYA）针对甲醇、乙醇、二异丙胺及有机溶剂的化学特性定制，有效容积达 42 m³。罐体采用防腐防渗透特种铝合金圆形截面结构，总质量 40,000 kg，额定载重 33.7 吨。鹅颈梁布局有效降低质心，多道防荡隔板大幅抑制液体冲击惯性，提供一流的危险化学品干线运输保障。',
        'en': 'Heavy-duty 43m³ aluminum alloy flammable liquid tank semi-trailer (Model B, HFV9407GRYA) tailored for methanol, ethanol, isopropanol, and diisopropylamine. Built with a cylindrical tank on a gooseneck frame, it delivers 43 m³ capacity (effective volume 42 m³), gross vehicle weight of 40,000 kg, and rated payload of 33,700 kg.'
    },
    'semi-tanker-45m3-alloy': {
        'zh': '本款 45m³ 铝合金运油半挂车（型号 HFV9404GYYA）为大容积干线成品油运输主流畅销车型，总容量 45 m³（有效容积达 44.9 m³）。整车总质量 40,000 kg，额定载质量 33.3 吨，采用变截面鹅颈大梁与铝合金方圆罐完美融合，既保证了大容量低密度的汽油装载需求，又兼具良好的过弯通过性与高速行驶风阻表现。',
        'en': 'Commercial 45m³ aluminum alloy fuel tanker semi-trailer (Model HFV9404GYYA), a premier choice for high-volume gasoline transit. Features a gooseneck frame with a rounded-rectangular tank, total capacity of 45 m³ (effective volume 44.9 m³), gross vehicle weight of 40,000 kg, and rated payload of 33,300 kg, combining low tare with superior stability.'
    },
    'semi-tanker-461m3-alloy': {
        'zh': '本款 46.1m³ 铝合金运油半挂车（型号 HFV9407GYYA）专为航空煤油（Jet Fuel）严苛的洁净度与防静电标准设计制造。罐体总容量 46.1 m³（有效容积 44 m³），采用高纯度食品及航空级防氧化铝合金方圆截面，等高直梁车架承载力强，总质量 40,000 kg，额定载重 33.5 吨，是机场供油与特种航空燃料干线转运的标杆车型。',
        'en': 'Dedicated 46.1m³ aluminum alloy fuel tanker semi-trailer (Model HFV9407GYYA) specialized for aviation kerosene (jet fuel). Features a straight-frame chassis with a high-purity alloy tank of 46.1 m³ capacity (effective volume 44 m³), gross vehicle weight of 40,000 kg, and rated payload of 33,500 kg, meeting strict aviation fuel purity standards.'
    },
    'semi-tanker-47m3-auman-alloy': {
        'zh': '本款 47m³ 欧曼铝合金运油半挂车（型号 HFV9406GYYB）采用低质心鹅颈车架架构与 47 m³ 超大容积铝合金方圆罐（有效容积 45.5 m³）。整车总质量 40,000 kg，额定载重最高达 34 吨，专用于汽油大规模跨省调拨。配置全套欧标下装油接口、油气回收阀与高精度液位传感系统，作业快捷且零挥发泄漏。',
        'en': 'High-capacity 47m³ aluminum alloy fuel tanker semi-trailer (Model HFV9406GYYB) designed with a gooseneck frame and rounded-rectangular tank. Features a total capacity of 47 m³ (effective volume 45.5 m³), gross vehicle weight of 40,000 kg, and payload of up to 34,000 kg, equipped with European-standard bottom loading and vapor recovery.'
    },
    'semi-tanker-48m3-alloy': {
        'zh': '本款 48m³ 铝合金运油半挂车（型号 HFV9400GYYA）为轻质汽油超大吨位运输标杆，罐体总容量达 48 m³（有效容积 47.1 m³）。半挂车总质量 40,000 kg，额定载重高达 34 吨。结构上选用加固型变截面鹅颈大梁，配合先进的有限元拓扑优化设计，在实现极限容积载运的同时，确保车架结构在重载冲击下依然具备持久疲劳寿命。',
        'en': 'Ultra-high-capacity 48m³ aluminum alloy fuel tanker semi-trailer (Model HFV9400GYYA) engineered for high-efficiency gasoline transport. Equipped with a gooseneck chassis frame and rounded-rectangular tank, total capacity reaches 48 m³ (effective volume 47.1 m³), gross vehicle weight of 40,000 kg, and rated payload of 34,000 kg.'
    },
    'semi-tanker-499m3-auman-alloy': {
        'zh': '本款 49.9m³ 欧曼铝合金运油半挂车（型号 HFV9409GYYA）是目前公告合规范围内装载容积最大的旗舰级运油半挂车，总容量达 49.9 m³（有效容积 47.5 m³）。总质量 40,000 kg，额定载重 33.5 吨。全车采用航空级 5182 铝合金精密自动化焊接，集成下装油系统、海底紧急切断系统及智能防溢流探头，是大规模物流车队追求单趟极值运能的最佳选择。',
        'en': 'Flagship 49.9m³ aluminum alloy fuel tanker semi-trailer (Model HFV9409GYYA), representing the maximum legally compliant tank capacity in our line. Features a 49.9 m³ tank (effective volume 47.5 m³), gooseneck frame, gross vehicle weight of 40,000 kg, and rated payload of 33,500 kg, delivering maximum volumetric capacity for fleet operators.'
    },
    'reefer-truck-auman': {
        'zh': '本款 4.5 吨级轻型冷藏保温车（型号 HFV5040XLCJXW6）专为生鲜果蔬、医药制剂及冷链生鲜的城市高效快配而设计。基于成熟商用轻卡底盘，整车总质量 4,495 kg（符合蓝牌轻卡法规标准），搭载高热阻聚氨酯整体发泡保温箱体与食品级复合蒙皮，隔热性能优异，提供多种货厢容积规格与冷机选装方案。',
        'en': 'High-efficiency 4.5-ton light-duty refrigerated box truck (Model HFV5040XLCJXW6) optimized for fresh produce, pharmaceutical distribution, and urban cold-chain logistics. Engineered on a proven commercial chassis with a gross vehicle weight of 4,495 kg, it features a seamless sandwich polyurethane foam insulated body, food-grade antimicrobial composite liners, and versatile refrigeration unit options.'
    },
    'reefer-truck-8m-isuzu': {
        'zh': '本款 8 米中重型冷链冷藏运输车（型号 HFV5180XLCQL6）基于五十铃高可靠性商用车底盘打造，总质量 18,000 kg，额定载重 9,305 kg。货厢长达 8 米，采用高压硬质聚氨酯整体发泡结合 XPS 复合保温工艺，内外蒙皮支持食品级玻璃钢（FRP）或热塑板（CFRTP）定制，隔热保温性能达行业领先水平，特别适用于城际长途冷鲜、冷冻食品及医药干线温控运输。',
        'en': 'Medium-duty 8-meter refrigerated transport truck (Model HFV5180XLCQL6) built on an authentic Isuzu 4x2 commercial chassis. Features an 18,000 kg gross vehicle weight and 9,305 kg rated payload. The 8m cargo box utilizes closed-cell polyurethane foam with XPS composite bonding, food-grade FRP/CFRTP skins, and heavy-duty refrigeration units for intercity cold-chain logistics.'
    },
    'reefer-semi-45ft-leaf-spring': {
        'zh': '本款 45 英尺一体式干线冷藏半挂车（型号 HFV9401XLC）采用高刚性重载板簧悬架与双胎承载桥，总质量 40,000 kg，额定载重达 31.5 吨。箱体应用行业领先的三明治闭式高压发泡工艺与一体成型复合箱板，保温层选用高密度阻燃聚氨酯，结合食品级内蒙皮与铝合金通风底板，结构牢固抗冲击，气密性及保温系数达国际冷链优级标准。',
        'en': 'Heavy-duty 45ft integrated cold-chain semi-trailer (Model HFV9401XLC) equipped with high-durability multi-leaf spring suspension and dual wheels. Gross vehicle weight is 40,000 kg with a rated payload of up to 31,520 kg. Features seamless sandwich closed-cell polyurethane insulation, pre-coated aluminum outer skin, and food-grade interior walls, delivering exceptional thermal retention for long-haul perishables.'
    },
    'reefer-semi-45ft-air-suspension': {
        'zh': '本款 45 英尺一体式轻量化高端冷藏半挂车（型号 HFV9400XLC）搭载多轴高性能空气悬架系统，总质量 40,000 kg，整备质量仅 8.1 吨，额定载重高达 31.9 吨。箱体采用三明治无冷桥整体成型工艺，保温层为高密度聚氨酯，内蒙皮升级为连续纤维增强热塑性复合板（CFRTP），具有极高的抗冲击、耐腐蚀及食品卫生级别，空气悬挂可大幅过滤道路颠簸，是高端水果、疫苗药品及精密温控干线货运的首选车型。',
        'en': 'Premium 45ft integrated refrigerated semi-trailer (Model HFV9400XLC) featuring an advanced multi-axle air suspension system and single super-single tires. Gross vehicle weight is 40,000 kg with an ultra-low tare weight of 8,100 kg and high payload of 31,900 kg. Outfitted with high-density polyurethane insulation and CFRTP thermoplastic composite lining, offering superior vibration isolation and thermal efficiency for premium perishables and pharmaceuticals.'
    },
    'reefer-semi-45ft-split': {
        'zh': '本款 45 英尺分体式多温区冷藏半挂车（型号 HFV9402XLC）采用高承载板簧悬架（可选装高端空气悬挂），总质量 40,000 kg，额定载质量 31,520 kg。箱体采用模块化三明治闭式发泡一体板工艺，分体式承载结构更适应复杂多变的干线转运环境，可按需选装冷机油箱与双开/单开侧门布局，隔热密封优异，兼顾大容量长途冷链运输与高经济性运维需求。',
        'en': 'Versatile 45ft split-type refrigerated semi-trailer (Model HFV9402XLC) built with leaf-spring suspension (air suspension optional). Total gross vehicle weight is 40,000 kg with a rated payload of 31,520 kg. Features modular sandwich foam construction, flexible side-door access, and dual-evaporator zoning options, ideally suited for multi-stop cold-chain distribution across diverse regional climates.'
    },
    'engineering-vehicle-1': {
        'zh': '专为城市渣土、碎石及建筑工程废料清运打造的高可靠性重型自卸车上装。箱体采用 510L 特种高强度钢板精心成型，U型截面结构有效消除卸料死角并防止物料粘结附着；配备电机驱动环保密闭顶盖，显著降低车辆重心与道路侧翻风险，完美适配各大主流商用车重载底盘。',
        'en': 'Heavy-duty U-box tipper superstructure engineered for muck, aggregate, and construction material haulage. Fabricated from 510L high-strength alloy steel, the aerodynamic U-shaped body prevents material adhesion and enables rapid dumping. Features an electric motor-driven environmental sealing cover and a low center-of-gravity architecture for superior rollover resistance across tough job sites.'
    },
    'engineering-vehicle-2': {
        'zh': '重型工程自卸车，依托成熟工程车底盘打造，适用于矿山开采、水利土石方清运及市政基础工程建设。高强度耐磨钢车厢配合多级强劲举升液压系统，具备优异的抗冲击性与抗扭刚度。本车型技术参数与上装货箱尺寸支持按实际工程工况定制，欢迎联系我司工程团队索取详细技术规格书与商务报价。',
        'en': 'Heavy-duty engineering tipper truck engineered on robust commercial chassis platforms for mining, earthmoving, quarrying, and large-scale infrastructure projects. Features high-rigidity wear-resistant body construction and multi-stage hydraulic dumping hydraulics. Technical configurations and box dimensions can be custom-tailored to site conditions; contact our export engineering team for the full technical datasheet and quotation.'
    },
    'engineering-vehicle-3': {
        'zh': '新一代高端智能环保自卸车上装，采用 T700 超高强度钢材打造，侧板前后贯通一体冲压成型，彻底消除内部凹凸立柱与挂料积土问题。整车搭载轻量化液压随动密闭顶盖，开闭顺畅且不占用货箱有效容积；可选装智能物联网（IoT）工况监控系统与高压喷雾抑尘装置，全面满足绿色城市工程运输与智能车队严苛合规要求。',
        'en': 'Next-generation intelligent eco-tipper superstructure engineered with T700 ultra-high-strength steel. Features full-length seamless side panels that eliminate internal rib protrusions and prevent muck buildup. Equipped with a lightweight hydraulic articulated sealing cover, and optional IoT fleet telematics with high-pressure dust-suppression misting systems, meeting stringent green city regulations.'
    }
}

POLISHED_SHORT_DESCS = {
    'fuel-tanker-15m3-auman': {
        'zh': '成熟商用车底盘与碳钢方圆罐，总容量 15.1m³，专为汽油等轻质燃油的高效合规道路转运设计。',
        'en': 'Commercial chassis with 15.1m³ carbon steel tank, optimized for compliant highway gasoline distribution.'
    },
    'fuel-tanker-18m3-flammable': {
        'zh': '中国重汽豪沃三桥底盘与碳钢耐压方圆罐，总容量 18.1m³，专用于原油等重质易燃液体安全储运。',
        'en': 'Sinotruk Howo 6x4 chassis with 18.1m³ carbon steel tank, engineered for crude oil and flammable liquids.'
    },
    'fuel-tanker-21m3-flammable': {
        'zh': '中国重汽豪沃底盘与高强度碳钢方圆罐，总容量 21.4m³，专为石脑油及易燃化工流体安全转运定制。',
        'en': 'Sinotruk Howo chassis with 21.4m³ tank, configured for naphtha and volatile petrochemical transport.'
    },
    'fuel-tanker-21m3-dongfeng': {
        'zh': '东风三桥商用车底盘与 21m³ 碳钢方圆罐，额定载重达 13.8 吨，专用于石脑油原料中长途转运。',
        'en': 'Dongfeng 6x4 chassis with 21m³ tank and 13.8T payload, suited for naphtha and chemical feedstocks.'
    },
    'fuel-tanker-258m3-auman-alloy': {
        'zh': '欧曼四桥高配底盘与轻量化铝合金方圆罐，总容量 25.8m³，额定载重超 20.6 吨，多仓多介质运输。',
        'en': 'Auman 8x4 chassis with 25.8m³ alloy tank, 20.6T payload, multi-compartment fuel delivery.'
    },
    'fuel-tanker-265m3-auman': {
        'zh': '欧曼四桥重载底盘与高强度碳钢方圆截面罐，总容量 26.5m³，专用于汽油成品油大批量干线调拨。',
        'en': 'Auman 8x4 chassis with 26.5m³ carbon steel tank for high-volume gasoline and fuel distribution.'
    },
    'fuel-tanker-26m3-dongfeng-alloy': {
        'zh': '东风天龙旗舰四桥底盘与 26m³ 铝合金方圆罐，额定载重 20.7 吨，获批柴油、煤油及汽油运输。',
        'en': 'Dongfeng Tianlong 8x4 with 26m³ alloy tank, 20.7T payload for diesel, kerosene, and gasoline.'
    },
    'fuel-tanker-26m3-alloy': {
        'zh': '中国重汽汕德卡高端重卡底盘与 26m³ 铝合金方圆罐，额定载重 20.3 吨，出勤可靠、驾乘舒适。',
        'en': 'Sinotruk Sitrak 8x4 with 26m³ alloy tank, 20.3T payload, offering premier reliability and efficiency.'
    },
    'fuel-tanker-303m3-dongfeng-alloy': {
        'zh': '单车系列最大容积旗舰：东风天龙 30.3m³ 铝合金运油车，额定载重 20.2 吨，单趟运载效益极值。',
        'en': 'Flagship 30.3m³ alloy tank on Dongfeng 8x4, maximizing payload and revenue per haul.'
    },
    'semi-tanker-376m3-auman-alloy': {
        'zh': '直梁式承载大梁与优质铝合金方圆罐，总容量 37.6m³，额定载重达 33.8 吨，柴油汽油干线物流。',
        'en': 'Straight-frame 37.6m³ aluminum semi-trailer with 33.8T payload for multi-fuel long-haul logistics.'
    },
    'semi-tanker-385m3-auman': {
        'zh': '低质心变截面鹅颈大梁与碳钢方圆罐，总容量 38.5m³，额定载重达 30.2 吨，重载长途稳定性好。',
        'en': 'Gooseneck 38.5m³ carbon steel semi-trailer, 30.2T payload, low center of gravity for stable transit.'
    },
    'semi-tanker-404m3-auman-alloy': {
        'zh': '轻量化高刚度等高直梁车架与 40.4m³ 铝合金方圆罐，有效容积达 40.3m³，额定载重 33.8 吨。',
        'en': 'Lightweight 40.4m³ aluminum semi-trailer with straight frame, 33.8T payload for trunkline fuel logistics.'
    },
    'semi-tanker-42m3-alloy': {
        'zh': '耐腐蚀特种铝合金材料与等高直梁车架，总容量 42m³，额定载重 33.5 吨，跨省石化干线高频调拨。',
        'en': 'Corrosion-resistant 42m³ alloy semi-trailer with straight frame, 33.5T payload for high-frequency fuel transfer.'
    },
    'semi-tanker-43m3-flammable-a': {
        'zh': '高强铝合金圆罐与鹅颈大梁，43m³ 大容积，专为乙醇、丁醇、丙酮及溶剂油危化品运输研制。',
        'en': 'Gooseneck 43m³ cylindrical alloy semi-trailer, engineered for ethanol, acetone, and volatile solvents.'
    },
    'semi-tanker-43m3-flammable-b': {
        'zh': '耐腐铝合金圆罐与鹅颈大梁，有效容积 42m³，针对甲醇、乙醇及有机溶剂定制，抑浪安全可靠。',
        'en': 'Gooseneck 43m³ cylindrical alloy semi-trailer tailored for methanol, ethanol, and chemical solutions.'
    },
    'semi-tanker-45m3-alloy': {
        'zh': '干线成品油主流畅销车型：变截面鹅颈与 45m³ 铝合金方圆罐，额定载重 33.3 吨，高通过性。',
        'en': 'Premier 45m³ alloy gooseneck semi-trailer, 33.3T payload, ideal balance of capacity and road handling.'
    },
    'semi-tanker-461m3-alloy': {
        'zh': '专为航空煤油（Jet Fuel）严苛洁净度打造：46.1m³ 铝合金方圆截面，等高直梁，机场供油标杆。',
        'en': 'Dedicated 46.1m³ alloy jet-fuel semi-trailer with straight frame, meeting strict aviation cleanliness standards.'
    },
    'semi-tanker-47m3-auman-alloy': {
        'zh': '低质心鹅颈车架与 47m³ 超大容积铝合金方圆罐，额定载重达 34 吨，全套欧标下装油与油气回收。',
        'en': 'High-capacity 47m³ alloy gooseneck semi-trailer, up to 34T payload, equipped with European bottom loading.'
    },
    'semi-tanker-48m3-alloy': {
        'zh': '轻质汽油超大吨位标杆：48m³ 铝合金方圆罐与加固鹅颈梁，额定载重 34 吨，拓扑优化抗疲劳。',
        'en': 'Ultra-high-capacity 48m³ alloy semi-trailer, 34T payload, topology-optimized for high-load durability.'
    },
    'semi-tanker-499m3-auman-alloy': {
        'zh': '合规容积极值旗舰：49.9m³ 欧曼铝合金方圆罐半挂车，额定载重 33.5 吨，追求单趟极值运能首选。',
        'en': 'Maximum-capacity 49.9m³ alloy semi-trailer, 33.5T payload, the ultimate volume carrier for fleet operators.'
    },
    'reefer-truck-auman': {
        'zh': '4.5吨级合规蓝牌城配冷藏车，无冷桥三明治闭式高压发泡工艺与食品级内蒙皮，城市生鲜快配首选。',
        'en': '4.5-ton light-duty refrigerated truck with seamless sandwich foam insulation, ideal for urban fresh distribution.'
    },
    'reefer-truck-8m-isuzu': {
        'zh': '五十铃成熟商用车底盘与 8 米保温货厢，总质量 18 吨，聚氨酯硬质发泡与 XPS 粘接，干线冷链标杆。',
        'en': 'Authentic Isuzu 4x2 chassis with 8m cargo box, 18T GVW, polyurethane/XPS insulation for cold-chain haulage.'
    },
    'reefer-semi-45ft-leaf-spring': {
        'zh': '45英尺一体式重载冷藏半挂车，多片钢板弹簧悬架与双胎承载桥，额定载重达 31.5 吨，气密保温优异。',
        'en': 'Heavy-duty 45ft cold-chain semi-trailer with leaf springs and dual tires, 31.5T payload for long-haul cargo.'
    },
    'reefer-semi-45ft-air-suspension': {
        'zh': '45英尺高端冷藏半挂车，多轴空气悬架，CFRTP连续纤维热塑内蒙皮，精密温控与高端果蔬医药首选。',
        'en': 'High-end 45ft refrigerated semi-trailer with air suspension and CFRTP composite liner for sensitive cargo.'
    },
    'reefer-semi-45ft-split': {
        'zh': '45英尺分体式多温区冷藏半挂车，重载悬架与模块化三明治一体板，兼顾大容量与高经济性运维。',
        'en': 'Versatile 45ft split-type refrigerated semi-trailer with multi-temp capability for regional cold logistics.'
    },
    'engineering-vehicle-1': {
        'zh': '重型U型城市渣土自卸车上装，510L高强耐磨钢打造，低重心防侧翻设计，配备电机驱动环保密闭顶盖。',
        'en': 'Heavy-duty U-box tipper body in 510L steel with low center of gravity and electric sealing cover.'
    },
    'engineering-vehicle-2': {
        'zh': '重型工程自卸车，依托成熟工程车底盘打造，高强度耐磨钢货箱，参数与车厢尺寸支持按工况定制。',
        'en': 'Heavy-duty engineering tipper truck on commercial chassis; box dimensions and specs custom-tailored on request.'
    },
    'engineering-vehicle-3': {
        'zh': '新一代智能环保自卸车上装，T700高强钢通体侧板，液压随动密闭顶盖，可选装物联网与高压喷雾抑尘。',
        'en': 'Next-gen eco-tipper body with T700 seamless side panels, hydraulic cover, and optional IoT telematics.'
    }
}

POLISHED_FEATURES = {
    'engineering-vehicle-1': [
        {
            'zh': '流线型U型货箱截面：边角过渡圆润平滑，倾卸顺畅不积料、不挂渣，具备优异的环保抑尘特性。',
            'en': 'Streamlined U-shaped box geometry: Smooth rounded transitions ensure clean, rapid dumping without spoil buildup.'
        },
        {
            'zh': '超低质心工程结构：有效降低整车装载重心，大幅提升重载转弯与颠簸路面的横向抗侧翻稳定性。',
            'en': 'Ultra-low center-of-gravity engineering: Substantially reduces loading height and improves lateral rollover stability.'
        },
        {
            'zh': '高冗余重载液压系统：额定设计压力 25 MPa，日常作业工作压力仅 15 MPa，抗过载储备充裕，使用寿命长。',
            'en': 'High-redundancy hydraulic system: 25 MPa rated pressure operating at 15 MPa, offering abundant overload capacity and durability.'
        },
        {
            'zh': '电动驱动环保密闭顶盖：电机强劲平稳驱动，支持钢丝绳或高强度链条传动定制，实现渣土运输全程密封无抛撒。',
            'en': 'Motor-driven environmental sealing cover: Powered by electric drive with wire-rope or chain transmission for spillage-free hauling.'
        }
    ],
    'engineering-vehicle-3': [
        {
            'zh': '高刚性U型复合截面结构：物料顺畅倾卸不残留，车厢密闭性极佳，符合国家严苛环保运输标准。',
            'en': 'High-rigidity U-shaped composite structure: Ensures clean cargo discharge and superior environmental sealing.'
        },
        {
            'zh': '低重心抗倾覆底盘匹配：显著降低重载工况下的整车重心，极大增强多轴工程车在非铺装路面的横向抗侧翻能力。',
            'en': 'Low center-of-gravity rollover prevention: Enhances lateral stability of multi-axle dump chassis over unpaved job sites.'
        },
        {
            'zh': '前拉式多级重载液压油缸：油缸受力方向经过科学力学仿真优化，杜绝举升砸伤隐患，大幅延长密封与活动副寿命。',
            'en': 'Front-pull multi-stage hydraulic cylinder: Optimized geometric force angles eliminate impact damage and extend seal life.'
        },
        {
            'zh': '轻量化液压随动环保顶盖：小盖板联动折叠机构，液压平稳闭合，杜绝卸货干涉卡滞，且不侵占货箱内部装载容积。',
            'en': 'Lightweight hydraulic articulated cover: Linked folding panels prevent jamming during discharge and preserve internal box volume.'
        },
        {
            'zh': '侧板前后贯通一体冲压工艺：整板一体成型无拼接立柱，彻底消除箱体内部凸出死角与挂泥积渣现象。',
            'en': 'Full-length seamless one-piece side panels: Integrally molded without vertical interior ribs, completely eliminating mud entrapment.'
        },
        {
            'zh': '智能车联网与高压抑尘喷雾系统：可选装车载智能物联网监控终端（实时定位/载重/举升监测）及微米级喷雾抑尘装置。',
            'en': 'Optional IoT fleet telematics & misting system: Real-time payload/lift monitoring combined with high-pressure dust suppression.'
        }
    ]
}

def extract_docx_runs(filepath):
    with zipfile.ZipFile(filepath) as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in tree.findall('.//w:p', ns):
                texts = [t.text.strip() for t in p.findall('.//w:t', ns) if t.text and t.text.strip()]
                if texts:
                    paragraphs.append(texts)
            return paragraphs

def sanitize_text(text):
    if not text:
        return ''
    text = re.sub(r'Manufactured by Hubei Forze Motor Co\.,Ltd\s*\(Model\s*[^)]+\)\.\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Manufactured by Hubei Forze Motor Co\.,Ltd\.\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bForze\b', 'Rootze Partner Coalition', text, flags=re.IGNORECASE)
    text = re.sub(r'\bHubei Forze\b', 'Xiangyang Automotive Manufacturing Base', text, flags=re.IGNORECASE)
    text = re.sub(r'该车由湖北福智汽车有限公司生产，\s*', '该车', text)
    text = re.sub(r'由湖北福智汽车有限公司生产，\s*', '', text)
    text = re.sub(r'湖北福智汽车有限公司', '', text)
    text = re.sub(r'福智汽车', '', text)
    text = re.sub(r'福智', '', text)
    return text.strip()

def match_spec_key(line):
    line_lower = line.lower()
    for sk_id, en_name, zh_name, patterns in SPEC_KEYS:
        if any(p in line_lower for p in patterns):
            return sk_id, en_name, zh_name
    return None

def normalize_spec_val(sk_id, v_zh, v_en):
    # Clean any OEM factory mentions
    v_zh = sanitize_text(v_zh)
    v_en = sanitize_text(v_en)
    
    # Clean domestic "牌" in brands
    v_zh = re.sub(r'欧曼牌\s*', '欧曼 ', v_zh)
    v_zh = re.sub(r'东风牌\s*', '东风 ', v_zh)
    v_zh = re.sub(r'豪沃牌\s*', '中国重汽豪沃 ', v_zh)
    v_zh = re.sub(r'汕德卡牌\s*', '中国重汽汕德卡 ', v_zh)
    v_zh = re.sub(r'五十铃牌\s*', '五十铃 ', v_zh)
    v_zh = re.sub(r'江西五十铃牌\s*', '江西五十铃 ', v_zh)

    v_en = re.sub(r'\bHowo\b', 'Sinotruk Howo', v_en)
    v_en = re.sub(r'\bSitrak\b', 'Sinotruk Sitrak', v_en)

    # Tank cross-section & structure normalization
    if sk_id == 'spv_key.tank_type':
        if '铝合金方圆' in v_zh and '鹅颈' in v_zh:
            v_zh = '铝合金方圆形截面，变截面鹅颈承载大梁'
            v_en = 'Aluminum alloy rounded-rectangular tank, gooseneck frame'
        elif '铝合金方圆' in v_zh and '直梁' in v_zh:
            v_zh = '铝合金方圆形截面，等高直梁承载车架'
            v_en = 'Aluminum alloy rounded-rectangular tank, straight frame'
        elif '铝合金圆罐' in v_zh and '鹅颈' in v_zh:
            v_zh = '铝合金圆柱形截面，变截面鹅颈承载大梁'
            v_en = 'Aluminum alloy round cylindrical tank, gooseneck frame'
        elif '碳钢方圆' in v_zh and '鹅颈' in v_zh:
            v_zh = '高强度碳钢方圆形截面，变截面鹅颈承载大梁'
            v_en = 'High-strength carbon steel rounded-rectangular tank, gooseneck frame'
        elif '碳钢方圆' in v_zh:
            v_zh = '高强度碳钢方圆形截面罐体'
            v_en = 'High-strength carbon steel rounded-rectangular tank'
        elif '铝合金方圆' in v_zh:
            v_zh = '5083/5182特种铝合金方圆形截面罐体'
            v_en = '5083/5182 aluminum alloy rounded-rectangular tank'

    # Suspension normalization
    if sk_id == 'spv_key.suspension':
        if '空气' in v_zh or '空悬' in v_zh:
            v_zh = '多轴高性能空气悬架系统（配备大单胎）'
            v_en = 'Multi-axle air suspension system (single tires)'
        elif '板簧' in v_zh:
            v_zh = '重载多片钢板弹簧悬架系统（配备双胎）'
            v_en = 'Heavy-duty multi-leaf spring suspension system (dual tires)'

    # Floor normalization
    if sk_id == 'spv_key.floor':
        if '保型' in v_zh and 'T型' in v_zh:
            v_zh = '铝合金T型导轨通风地板（高承载保型结构）'
            v_en = 'Aluminum alloy T-section air-duct ventilation floor'
        elif '通风槽' in v_zh:
            v_zh = '铝合金T型通风导轨地板、防滑花纹铝板、波纹钢板可选'
            v_en = 'Aluminum T-duct floor, checkered aluminum floor, or corrugated steel floor optional'

    # Box construction normalization
    if sk_id == 'spv_key.box_const':
        if '三明治' in v_zh:
            v_zh = '无冷桥三明治闭式高压发泡工艺、一体成型复合箱板'
            v_en = 'Sandwich closed-cell high-pressure foaming, integrally molded composite panels'
        elif '聚氨酯发泡' in v_zh:
            v_zh = '高压聚氨酯发泡与XPS挤塑板复合高强粘接工艺'
            v_en = 'High-pressure polyurethane foaming with XPS composite bonding'

    # Insulation material normalization
    if sk_id == 'spv_key.insulation':
        if '挤塑板' in v_zh or 'XPS' in v_zh:
            v_zh = '高密度阻燃硬质聚氨酯（PU）与高强度XPS挤塑板复合隔热层'
            v_en = 'High-density flame-retardant polyurethane (PU) and XPS composite insulation'
        elif '聚氨酯' in v_zh:
            v_zh = '高密度阻燃硬质发泡聚氨酯（PU），导热系数极低'
            v_en = 'High-density flame-retardant rigid polyurethane (PU) foam'

    # Inner skin normalization
    if sk_id == 'spv_key.inner_skin':
        if 'CFRTP' in v_zh or '热塑' in v_zh:
            v_zh = 'CFRTP 连续纤维增强热塑性复合板（食品级卫生材质）'
            v_en = 'CFRTP continuous fiber-reinforced thermoplastic composite panel (food-grade)'
        elif '不锈钢' in v_zh or '玻璃钢' in v_zh:
            v_zh = '食品级玻璃钢（FRP）、SUS304不锈钢板、耐候铝合金板可选'
            v_en = 'Food-grade FRP, SUS304 stainless steel, or aluminum alloy plate optional'

    # Outer skin normalization
    if sk_id == 'spv_key.outer_skin':
        if '预涂铝板' in v_zh or '铝板' in v_zh:
            v_zh = '预涂防腐铝合金板（表面平整光洁，耐候抗老化）'
            v_en = 'Pre-coated corrosion-resistant aluminum alloy plate'
        elif '预涂钢板' in v_zh:
            v_zh = '高强度耐候预涂彩钢板、耐蚀铝合金板、高光玻璃钢（FRP）可选'
            v_en = 'High-strength pre-coated steel plate, aluminum alloy plate, or high-gloss FRP optional'

    # Tipper plate thickness
    if sk_id == 'spv_key.plate':
        if '底10' in v_zh or '10' in v_zh:
            v_zh = '底板 10mm / 边板 8mm（可选装 底板 12mm / 边板 10mm 特重工况配置）'
            v_en = 'Floor 10mm / Side 8mm (Optional: Floor 12mm / Side 10mm heavy-duty configuration)'
        elif '底8' in v_zh or '8' in v_zh:
            v_zh = '底板 8mm / 边板 6mm'
            v_en = 'Floor 8mm / Side 6mm'

    # Tipper cylinder
    if sk_id == 'spv_key.cylinder':
        if '海沃' in v_zh or '157' in v_zh:
            v_zh = 'Φ157 / Φ179 前顶多级工程液压油缸（海沃HYVA或知名品牌），或 T式中顶 220×910'
            v_en = 'Φ157 / Φ179 front-mount multi-stage hydraulic cylinder (Hyva / OEM brand), or T-type mid-mount 220×910'
        elif '5TG' in v_zh:
            v_zh = '5TG157×4280 前拉式多级重载工程液压油缸'
            v_en = '5TG157×4280 front-pull multi-stage heavy-duty hydraulic cylinder'

    # Tipper body structure
    if sk_id == 'spv_key.body_struct':
        if '后开门' in v_zh:
            v_zh = '机械连杆/液压自锁密闭后开门结构'
            v_en = 'Mechanical linkage / hydraulic self-locking sealed tailgate'

    return v_zh.strip(), v_en.strip()

def extract_val_pair(texts, sk_id=None):
    # Specific known fixes for multi-part runs
    join_all = ' '.join(texts)
    if 'QL5180XXYAJRHY' in join_all:
        return '五十铃 QL5180XXYAJRHY', 'Isuzu QL5180XXYAJRHY'
    if 'Polyurethane foaming, XPS bonding' in join_all:
        return '高压聚氨酯发泡、XPS挤塑板复合粘接工艺', 'Polyurethane foaming, XPS composite bonding'

    if len(texts) == 1:
        s = texts[0]
        m = re.match(r'^([\u4e00-\u9fff\uff08\uff09\u3001\uff0c\s]+)([A-Za-z].*)$', s)
        if m:
            v_zh = m.group(1).strip()
            v_en = m.group(2).strip()
            return normalize_spec_val(sk_id, v_zh, v_en)
        return normalize_spec_val(sk_id, s, s)

    zh_parts = []
    en_parts = []
    for t in texts:
        if re.search(r'[\u4e00-\u9fff]', t):
            zh_parts.append(t)
        else:
            en_parts.append(t)
    if zh_parts and en_parts:
        v_zh = ' '.join(zh_parts).strip()
        v_en = ' '.join(en_parts).strip()
        return normalize_spec_val(sk_id, v_zh, v_en)

    val_str = ' '.join(texts).strip()
    return normalize_spec_val(sk_id, val_str, val_str)

def parse_docx_full(paras, slug):
    data = {
        'specs': [],
        'optional_zh': '',
        'optional_en': '',
        'features': []
    }
    
    i = 2
    while i < len(paras):
        p_join = ''.join(paras[i])
        
        if any(h in p_join for h in ['主要参数', 'Key Specifications', '上装技术参数', 'Body Technical Parameters']):
            i += 1
            while i < len(paras):
                cur_join = ''.join(paras[i])
                if any(h in cur_join for h in ['可选配置', 'Optional', '产品特点', 'Features', '注：', 'Specifications are as published', '官网暂未公布']):
                    break
                match = match_spec_key(cur_join)
                if match:
                    sk_id, def_en, def_zh = match
                    val_texts = paras[i+1] if i + 1 < len(paras) else []
                    v_zh, v_en = extract_val_pair(val_texts, sk_id)
                    data['specs'].append({
                        'sk_id': sk_id,
                        'key_en': def_en,
                        'key_zh': def_zh,
                        'val_en': v_en,
                        'val_zh': v_zh
                    })
                i += 2
            continue
            
        if 'Optional Configurations' in p_join or '可选配置' in p_join:
            i += 1
            if i < len(paras):
                data['optional_zh'] = ''.join(paras[i])
            if i + 1 < len(paras) and not paras[i+1][0].startswith('注：'):
                data['optional_en'] = ' '.join(paras[i+1])
                i += 2
                continue
            i += 1
            continue
            
        if 'Features' in p_join or '产品特点' in p_join:
            i += 1
            while i < len(paras):
                cur_join = ''.join(paras[i])
                if cur_join.startswith('注：') or 'Specifications are as published' in cur_join:
                    break
                feat_zh = ''.join(paras[i])
                feat_en = ' '.join(paras[i+1]) if i + 1 < len(paras) and not paras[i+1][0].startswith('注：') else feat_zh
                data['features'].append({
                    'zh': feat_zh,
                    'en': feat_en
                })
                i += 2
            continue
            
        i += 1

    # Apply curated overviews & short descs
    if slug in POLISHED_OVERVIEWS:
        data['overview_zh'] = POLISHED_OVERVIEWS[slug]['zh']
        data['overview_en'] = POLISHED_OVERVIEWS[slug]['en']
    if slug in POLISHED_SHORT_DESCS:
        data['short_zh'] = POLISHED_SHORT_DESCS[slug]['zh']
        data['short_en'] = POLISHED_SHORT_DESCS[slug]['en']

    # Apply curated features for engineering vehicles
    if slug in POLISHED_FEATURES:
        data['features'] = POLISHED_FEATURES[slug]

    data['optional_en'] = sanitize_text(data['optional_en'])
    data['optional_zh'] = sanitize_text(data['optional_zh'])
    return data

def build_bilingual_dictionary(parsed_products):
    en_dict = {}
    zh_dict = {}

    # Global UI keys
    en_dict['catalog.spv.section_badge'] = 'Factory Direct Product Matrix'
    zh_dict['catalog.spv.section_badge'] = '原厂直供产品矩阵'

    en_dict['catalog.spv.section_title'] = 'Commercial Special Purpose Vehicles & Fleet Catalog'
    zh_dict['catalog.spv.section_title'] = '商用特种专用汽车与车队产品目录'

    en_dict['catalog.spv.section_desc'] = 'Export-certified special utility and transport vehicles engineered on Dongfeng, Auman, Howo, and Sitrak chassis. Click on any category to browse our 28 models, or view individual product pages for complete specifications.'
    zh_dict['catalog.spv.section_desc'] = '依托东风、欧曼、豪沃及汕德卡等成熟底盘打造的高品质特种商用改装车辆。点击分类即可浏览全部28款车型，或进入单车详情页查看完整工程规格参数。'

    en_dict['catalog.spv.btn_specs'] = 'Full Specs'
    zh_dict['catalog.spv.btn_specs'] = '规格详情'

    en_dict['catalog.spv.btn_rfq'] = 'RFQ'
    zh_dict['catalog.spv.btn_rfq'] = '在线询价'

    en_dict['catalog.spv.btn_back'] = 'Back to Vehicle Catalog'
    zh_dict['catalog.spv.btn_back'] = '返回车辆目录'

    en_dict['catalog.spv.btn_quote'] = 'Request a Factory Quote'
    zh_dict['catalog.spv.btn_quote'] = '索取原厂报价'

    en_dict['catalog.spv.tech_data_badge'] = 'Technical Data'
    zh_dict['catalog.spv.tech_data_badge'] = '技术参数'

    en_dict['catalog.spv.specs_heading'] = 'Key Specifications & Engineering Parameters'
    zh_dict['catalog.spv.specs_heading'] = '关键技术参数与工程规格表'

    en_dict['catalog.spv.opt_heading'] = 'Optional Configurations Available on Request'
    zh_dict['catalog.spv.opt_heading'] = '支持按需选装配置'

    en_dict['catalog.spv.features_heading'] = 'Key Product Features & Engineering Advantages'
    zh_dict['catalog.spv.features_heading'] = '核心产品特点与工程优势'

    en_dict['catalog.spv.specs_on_request_title'] = 'Technical Specifications On Request'
    zh_dict['catalog.spv.specs_on_request_title'] = '按需索取技术规格书'

    en_dict['catalog.spv.specs_on_request_desc'] = 'Official engineering specifications, payload capacities, and customized superstructure layouts for this model are available directly from our engineering and export team.'
    zh_dict['catalog.spv.specs_on_request_desc'] = '本车型的详细工程技术参数、额定载重能力及定制化上装方案可直接联系我们的外贸与工程团队获取。'

    en_dict['catalog.spv.specs_on_request_btn'] = 'Contact Sales for Spec Sheet'
    zh_dict['catalog.spv.specs_on_request_btn'] = '联系业务获取参数表'

    en_dict['catalog.spv.disclaimer_text'] = 'Note: Specifications are as published by the manufacturer; multiple values indicate different available configurations. Please confirm exact technical parameters and chassis options with our export team before ordering.'
    zh_dict['catalog.spv.disclaimer_text'] = '注：以上技术参数供参考，多个数值代表不同选配规格；具体参数及底盘配置以商务合同与技术协议为准。'

    en_dict['catalog.spv.btn_expand_all'] = 'Expand All'
    zh_dict['catalog.spv.btn_expand_all'] = '展开全部'

    en_dict['catalog.spv.btn_collapse_all'] = 'Collapse All'
    zh_dict['catalog.spv.btn_collapse_all'] = '折叠全部'

    en_dict['catalog.spv.nav_prev'] = 'Previous Model'
    zh_dict['catalog.spv.nav_prev'] = '上一款车型'

    en_dict['catalog.spv.nav_next'] = 'Next Model'
    zh_dict['catalog.spv.nav_next'] = '下一款车型'

    en_dict['catalog.spv.total_models_label'] = '4 Vehicle Categories · 28 Export Models'
    zh_dict['catalog.spv.total_models_label'] = '4 大专用车分类 · 28 款出口车型'

    en_dict['catalog.spv.click_to_zoom'] = 'Click to zoom'
    zh_dict['catalog.spv.click_to_zoom'] = '点击查看高清大图'

    # Categories
    for c in CATEGORIES:
        cid = c['id']
        en_dict[f'catalog.spv.{cid}_title'] = c['title_en']
        zh_dict[f'catalog.spv.{cid}_title'] = c['title_zh']
        en_dict[f'catalog.spv.{cid}_desc'] = c['desc_en']
        zh_dict[f'catalog.spv.{cid}_desc'] = c['desc_zh']
        en_dict[f'catalog.spv.{cid}_badge'] = c['badge_en']
        zh_dict[f'catalog.spv.{cid}_badge'] = c['badge_zh']

    # Spec keys
    for sk_id, en_name, zh_name, _ in SPEC_KEYS:
        en_dict[sk_id] = en_name
        zh_dict[sk_id] = zh_name

    # Per-product entries
    for p in parsed_products:
        meta = p['meta']
        data = p['data']
        slug = meta[1]
        title_en = meta[4]
        title_zh = meta[5]
        
        en_dict[f'spv.{slug}.title'] = title_en
        zh_dict[f'spv.{slug}.title'] = title_zh
        
        en_dict[f'spv.{slug}.overview'] = data['overview_en']
        zh_dict[f'spv.{slug}.overview'] = data['overview_zh']
        
        en_dict[f'spv.{slug}.short_desc'] = data['short_en']
        zh_dict[f'spv.{slug}.short_desc'] = data['short_zh']
        
        if data['optional_en']:
            en_dict[f'spv.{slug}.opt'] = data['optional_en']
            zh_dict[f'spv.{slug}.opt'] = data['optional_zh']
            
        for f_idx, feat in enumerate(data['features']):
            en_dict[f'spv.{slug}.feat_{f_idx}'] = feat['en']
            zh_dict[f'spv.{slug}.feat_{f_idx}'] = feat['zh']
            
        for s_idx, spec in enumerate(data['specs']):
            if spec['val_en'] != spec['val_zh']:
                en_dict[f'spv.{slug}.val_{s_idx}'] = spec['val_en']
                zh_dict[f'spv.{slug}.val_{s_idx}'] = spec['val_zh']

    return en_dict, zh_dict

def update_i18n_js(en_dict, zh_dict):
    print("Updating js/i18n.js with bilingual SPV dictionaries...")
    with open(I18N_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    if '"catalog.spv.btn_expand_all"' in content:
        print("js/i18n.js already contains SPV dictionaries, skipping duplicate injection.")
        return

    en_lines = []
    for k, v in sorted(en_dict.items()):
        v_clean = v.replace('\n', ' ').strip()
        en_lines.append(f'      {json.dumps(k)}: {json.dumps(v_clean, ensure_ascii=False)},')
    en_block = '\n' + '\n'.join(en_lines)

    zh_lines = []
    for k, v in sorted(zh_dict.items()):
        v_clean = v.replace('\n', ' ').strip()
        zh_lines.append(f'      {json.dumps(k)}: {json.dumps(v_clean, ensure_ascii=False)},')
    zh_block = '\n' + '\n'.join(zh_lines)

    old_en_last = '"catalog.spv.tbl_r4_superstructure": "Hardox 450 wear steel U-dump body, Hyva hydraulic lift cylinder"'
    old_zh_last = '"catalog.spv.tbl_r4_superstructure": "瑞典Hardox 450高耐磨U型矿山车厢、海沃(Hyva)前置多级举升油缸"'

    if old_en_last not in content or old_zh_last not in content:
        raise ValueError("Could not find anchor lines in i18n.js")

    content = content.replace(old_en_last, old_en_last + ',' + en_block)
    content = content.replace(old_zh_last, old_zh_last + ',' + zh_block)

    with open(I18N_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"js/i18n.js successfully updated! Injected {len(en_dict)} EN keys and {len(zh_dict)} ZH keys.")

def build_detail_page_i18n(prod_meta, doc_data, all_parsed):
    doc_file, slug, img, cat_id, display_title, display_title_zh, badge_class, category_name = prod_meta
    
    cat_obj = next(c for c in CATEGORIES if c['id'] == cat_id)
    cat_badge_key = f"catalog.spv.{cat_id}_badge"
    
    # Adjacent products in same category
    cat_products = [p for p in all_parsed if p['meta'][3] == cat_id]
    curr_idx = next(i for i, p in enumerate(cat_products) if p['meta'][1] == slug)
    prev_prod = cat_products[(curr_idx - 1) % len(cat_products)]
    next_prod = cat_products[(curr_idx + 1) % len(cat_products)]
    
    prev_slug = prev_prod['meta'][1]
    prev_title = prev_prod['meta'][4]
    next_slug = next_prod['meta'][1]
    next_title = next_prod['meta'][4]
    
    model_no = ''
    for s in doc_data['specs']:
        if 'model' in s['key_en'].lower():
            model_no = s['val_en']
            break
            
    url_title = urllib.parse.quote(display_title)
    url_model = urllib.parse.quote(model_no)
    quote_url = f"../special-vehicles.html?inquire={url_title}&model={url_model}#contact"
            
    # Highlight badges
    badges = []
    for s in doc_data['specs']:
        k_lower = s['key_en'].lower()
        if 'total capacity' in k_lower or 'effective volume' in k_lower:
            badges.append(s['val_en'])
        elif 'gross vehicle weight' in k_lower or 'gvw' in k_lower:
            badges.append(f"GVW: {s['val_en']}")
        elif 'rated payload' in k_lower:
            badges.append(f"Payload: {s['val_en']}")
        elif 'transported medium' in k_lower:
            badges.append(s['val_en'])
        elif 'cargo box dimensions' in k_lower:
            badges.append(f"Box: {s['val_en']}")
        elif 'cargo body size' in k_lower:
            badges.append(f"Body: {s['val_en']}")
        elif 'main material' in k_lower:
            badges.append(f"Material: {s['val_en']}")
            
    badges_html = ''
    for b in badges[:4]:
        badges_html += f'<span class="spec-badge mr-1 mb-1">{html.escape(b)}</span>\n                    '

    model_badge_html = ''
    if model_no:
        model_badge_html = f'<span class="badge badge-dark px-2 py-1 font-weight-bold" style="font-size: 13px;">Model: {html.escape(model_no)}</span>'

    spec_rows_html = ''
    if doc_data['specs']:
        for s_idx, s in enumerate(doc_data['specs']):
            sk_id = s['sk_id']
            k_en = html.escape(s['key_en'])
            v_en = html.escape(s['val_en'])
            
            val_attr = ''
            if s['val_en'] != s['val_zh']:
                val_attr = f' data-i18n="spv.{slug}.val_{s_idx}"'
                
            spec_rows_html += f'''                <tr>
                  <th style="width: 38%; background-color: #f8f9fa; color: #495057; font-weight: 600;" data-i18n="{sk_id}">{k_en}</th>
                  <td style="color: #212529;"{val_attr}>{v_en}</td>
                </tr>\n'''
    
    if doc_data['specs']:
        specs_section_html = f'''      <!-- Technical Specifications Table -->
      <div class="row mt-5">
        <div class="col-12">
          <div class="d-flex align-items-center mb-3">
            <span class="subheading mr-2" style="color: var(--rootze-primary); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; font-size: 13px;" data-i18n="catalog.spv.tech_data_badge">Technical Data</span>
            <h3 class="font-weight-bold mb-0" style="font-size: 20px;" data-i18n="catalog.spv.specs_heading">Key Specifications & Engineering Parameters</h3>
          </div>
          <div class="table-responsive shadow-sm border rounded bg-white">
            <table class="table table-bordered table-hover mb-0" style="font-size: 14px;">
              <tbody>
{spec_rows_html}              </tbody>
            </table>
          </div>
        </div>
      </div>'''
    else:
        specs_section_html = '''      <!-- Technical Specifications On Request -->
      <div class="row mt-5">
        <div class="col-12">
          <div class="alert alert-info p-4 border rounded shadow-sm bg-white">
            <h5 class="font-weight-bold mb-2 text-primary" data-i18n="catalog.spv.specs_on_request_title"><i class="ion-ios-information-circle mr-2"></i>Technical Specifications On Request</h5>
            <p class="mb-3 text-muted" style="line-height: 1.7;" data-i18n="catalog.spv.specs_on_request_desc">Official engineering specifications, payload capacities, and customized superstructure layouts for this model are available directly from our engineering and export team.</p>
            <a href="../special-vehicles.html#contact" class="btn btn-primary btn-sm px-4 font-weight-bold" data-i18n="catalog.spv.specs_on_request_btn">Contact Sales for Spec Sheet</a>
          </div>
        </div>
      </div>'''

    optional_section_html = ''
    if doc_data['optional_en']:
        opt_text = html.escape(doc_data['optional_en'])
        optional_section_html = f'''      <!-- Optional Configurations -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card border-0 bg-light p-4 rounded shadow-sm">
            <h5 class="font-weight-bold mb-2" style="color: var(--rootze-dark); font-size: 16px;" data-i18n="catalog.spv.opt_heading"><i class="ion-ios-options mr-2 text-primary"></i>Optional Configurations Available on Request</h5>
            <p class="mb-0 text-muted" style="font-size: 14px; line-height: 1.7;" data-i18n="spv.{slug}.opt">{opt_text}</p>
          </div>
        </div>
      </div>'''

    features_section_html = ''
    if doc_data['features']:
        feat_lis = ''
        for f_idx, f in enumerate(doc_data['features']):
            feat_lis += f'              <li class="mb-2" data-i18n="spv.{slug}.feat_{f_idx}">{html.escape(f["en"])}</li>\n'
        features_section_html = f'''      <!-- Product Features -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card border-0 bg-light p-4 rounded shadow-sm">
            <h5 class="font-weight-bold mb-3" style="color: var(--rootze-dark); font-size: 16px;" data-i18n="catalog.spv.features_heading"><i class="ion-ios-checkmark-circle-outline mr-2 text-primary"></i>Key Product Features & Engineering Advantages</h5>
            <ul class="mb-0 text-muted pl-3" style="font-size: 14px; line-height: 1.8;">
{feat_lis}            </ul>
          </div>
        </div>
      </div>'''

    page_html = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <title>{html.escape(display_title)} — Special Purpose Vehicles | Rootze Global</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="{html.escape(display_title)} export specifications, dimensions, payload, and technical data from Xiangyang automotive hub.">
    <meta name="keywords" content="{html.escape(display_title)}, Special Purpose Vehicles, Tank Truck, Refrigerated Truck, Dump Truck, Rootze Global">
    
    <!-- OpenGraph & Twitter Card SEO Meta Tags -->
    <meta property="og:title" content="{html.escape(display_title)} — Rootze Global">
    <meta property="og:description" content="{html.escape(display_title)} export specifications, dimensions, payload, and technical data.">
    <meta property="og:image" content="../../images/products/vehicles/{img}">
    <meta property="og:type" content="product">
    
    <link href="https://fonts.googleapis.com/css?family=Poppins:200,300,400,500,600,700,800&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../../css/open-iconic-bootstrap.min.css">
    <link rel="stylesheet" href="../../css/animate.css">
    <link rel="stylesheet" href="../../css/owl.carousel.min.css">
    <link rel="stylesheet" href="../../css/owl.theme.default.min.css">
    <link rel="stylesheet" href="../../css/magnific-popup.css">
    <link rel="stylesheet" href="../../css/aos.css">
    <link rel="stylesheet" href="../../css/ionicons.min.css">
    <link rel="stylesheet" href="../../css/flaticon.css">
    <link rel="stylesheet" href="../../css/icomoon.css">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="stylesheet" href="../../css/rootze.css">
  </head>
  <body>
    
    <!-- Top Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark ftco_navbar bg-dark ftco-navbar-light fixed-top" id="ftco-navbar">
      <div class="container-fluid px-3 px-md-4 px-lg-5">
        <a class="navbar-brand d-flex align-items-center" href="../../index.html#home" style="text-decoration: none;">
          <img src="../../images/logo-horizontal.png" alt="Rootze Logo" style="height: 42px; width: auto; object-fit: contain;">
        </a>

        <!-- Mobile controls (Language + Toggle) -->
        <div class="d-flex align-items-center d-lg-none">
          <div class="lang-switch mr-2">
            <button type="button" class="lang-btn active" data-lang="en">EN</button>
            <button type="button" class="lang-btn" data-lang="zh">中文</button>
          </div>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#ftco-nav" aria-controls="ftco-nav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="oi oi-menu"></span>
          </button>
        </div>

        <div class="collapse navbar-collapse" id="ftco-nav">
          <ul class="navbar-nav ml-auto align-items-lg-center">
            <li class="nav-item"><a href="../../index.html#home" class="nav-link" data-i18n="nav.home">Home</a></li>
            <li class="nav-item dropdown active">
              <a class="nav-link dropdown-toggle" href="../../index.html#products" id="navbarDropdownProducts" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" data-i18n="nav.products">Products</a>
              <div class="dropdown-menu shadow border-0" aria-labelledby="navbarDropdownProducts">
                <a class="dropdown-item py-2" href="../../index.html#products" data-i18n="products.title">All Sectors Overview</a>
                <div class="dropdown-divider"></div>
                <a class="dropdown-item py-2" href="../electrical-systems.html" data-i18n="products.cat1_title">Industrial Electrical Systems</a>
                <a class="dropdown-item py-2" href="../railway-equipment.html" data-i18n="products.cat2_title">Railway Track Equipment</a>
                <a class="dropdown-item py-2" href="../special-vehicles.html" data-i18n="products.cat3_title">Special Purpose Vehicles</a>
                <a class="dropdown-item py-2" href="../brake-pad-lines.html" data-i18n="products.cat4_title">Turnkey Brake Pad Lines</a>
              </div>
            </li>
            <li class="nav-item"><a href="../../index.html#about" class="nav-link" data-i18n="nav.about">About Us</a></li>
            <li class="nav-item"><a href="../../news.html" class="nav-link" data-i18n="nav.news">News</a></li>
            <li class="nav-item"><a href="../special-vehicles.html#contact" class="nav-link" data-i18n="nav.contact">Contact</a></li>
            <li class="nav-item d-none d-lg-block">
              <div class="lang-switch">
                <button type="button" class="lang-btn active" data-lang="en">EN</button>
                <button type="button" class="lang-btn" data-lang="zh">中文</button>
              </div>
            </li>
            <li class="nav-item cta ml-lg-3">
              <a href="../special-vehicles.html#contact" class="btn btn-primary py-2 px-3 btn-glow" data-i18n="nav.quote">Request Quote</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- END nav -->

    <!-- Breadcrumb Hero Header -->
    <section class="hero-wrap hero-wrap-2" style="background-image: url('../../images/products/vehicles/hero-vehicles.jpg'); background-size: cover; background-position: center; padding-top: 130px; padding-bottom: 50px; position: relative;">
      <div class="overlay" style="background: rgba(11, 19, 37, 0.88); position: absolute; top: 0; left: 0; right: 0; bottom: 0;"></div>
      <div class="container" style="position: relative; z-index: 2;">
        <div class="row no-gutters slider-text align-items-end justify-content-start">
          <div class="col-md-11 ftco-animate pb-3">
            <p class="breadcrumbs mb-2">
              <span class="mr-2"><a href="../../index.html" class="text-white"><span data-i18n="nav.home">Home</span> <i class="ion-ios-arrow-forward"></i></a></span>
              <span class="mr-2"><a href="../../index.html#products" class="text-white"><span data-i18n="nav.products">Products</span> <i class="ion-ios-arrow-forward"></i></a></span>
              <span class="mr-2"><a href="../special-vehicles.html" class="text-white"><span data-i18n="products.cat3_title">Special Purpose Vehicles</span> <i class="ion-ios-arrow-forward"></i></a></span>
              <span class="text-primary font-weight-bold" data-i18n="spv.{slug}.title">{html.escape(display_title)}</span>
            </p>
            <h1 class="mb-2 text-white font-weight-bold" style="font-size: 2rem;" data-i18n="spv.{slug}.title">{html.escape(display_title)}</h1>
            <p class="text-light mb-0" style="font-size: 1rem; opacity: 0.9;" data-i18n="products.spv_hero_subtitle">Export-grade commercial utility and transport vehicle from Xiangyang manufacturing base.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Product Detail Section -->
    <section class="ftco-section bg-white py-5">
      <div class="container">
        <div class="row align-items-start">
          <!-- Left: Product Image with Magnific Popup -->
          <div class="col-lg-5 mb-4 mb-lg-0">
            <div class="border rounded p-3 bg-white shadow-sm text-center position-relative">
              <a href="../../images/products/vehicles/{img}" class="image-popup d-block" title="{html.escape(display_title)}">
                <img src="../../images/products/vehicles/{img}" alt="{html.escape(display_title)}" class="img-fluid rounded" style="width: 100%; max-height: 420px; object-fit: contain; background: #fdfdfd; transition: transform 0.3s ease;">
                <div class="position-absolute" style="bottom: 18px; right: 24px; background: rgba(11, 19, 37, 0.75); color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 11px; pointer-events: none;">
                  <i class="ion-ios-search mr-1"></i><span data-i18n="catalog.spv.click_to_zoom">Click to zoom</span>
                </div>
              </a>
            </div>
          </div>
          
          <!-- Right: Overview & Badges -->
          <div class="col-lg-7">
            <div class="d-flex flex-wrap align-items-center mb-2" style="gap: 8px;">
              <span class="badge {badge_class} px-3 py-1 font-weight-bold" style="font-size: 13px;" data-i18n="{cat_badge_key}">{cat_obj['badge_en']}</span>
              {model_badge_html}
            </div>
            <h2 class="font-weight-bold mb-3" style="font-size: 24px; color: var(--rootze-dark);" data-i18n="spv.{slug}.title">{html.escape(display_title)}</h2>
            <div class="product-overview mb-4" style="line-height: 1.7; font-size: 15px; color: #555;">
              <p data-i18n="spv.{slug}.overview">{html.escape(doc_data['overview_en'])}</p>
            </div>
            
            <!-- Quick Highlight Badges -->
            <div class="spec-badge-wrap d-flex flex-wrap mb-4" style="gap: 6px;">
              {badges_html}
            </div>
            
            <!-- CTA Buttons -->
            <div class="d-flex flex-wrap gap-2 pt-3 border-top">
              <a href="{quote_url}" class="btn btn-primary py-2 px-4 font-weight-bold mr-2"><i class="ion-ios-paper-plane mr-1"></i> <span data-i18n="catalog.spv.btn_quote">Request a Factory Quote</span></a>
              <a href="../special-vehicles.html" class="btn btn-outline-secondary py-2 px-3 font-weight-bold"><i class="ion-ios-arrow-back mr-1"></i> <span data-i18n="catalog.spv.btn_back">Back to Vehicle Catalog</span></a>
            </div>
          </div>
        </div>

{specs_section_html}

{optional_section_html}

{features_section_html}

        <!-- Adjacent Models Navigation (Within Same Category) -->
        <div class="row mt-5 pt-4 border-top">
          <div class="col-6 text-left">
            <a href="{prev_slug}.html" class="d-inline-flex align-items-center text-dark text-decoration-none py-2 px-3 border rounded bg-light hover-shadow" style="transition: all 0.2s ease;">
              <span class="mr-2 text-primary" style="font-size: 22px;"><i class="ion-ios-arrow-dropleft-circle"></i></span>
              <div class="d-none d-sm-block">
                <small class="text-muted d-block font-weight-bold text-uppercase" style="font-size: 11px;" data-i18n="catalog.spv.nav_prev">Previous Model</small>
                <span class="font-weight-bold" style="font-size: 13.5px;" data-i18n="spv.{prev_slug}.title">{html.escape(prev_title)}</span>
              </div>
              <div class="d-block d-sm-none">
                <span class="font-weight-bold" style="font-size: 12px;" data-i18n="catalog.spv.nav_prev">Previous</span>
              </div>
            </a>
          </div>
          <div class="col-6 text-right">
            <a href="{next_slug}.html" class="d-inline-flex align-items-center justify-content-end text-dark text-decoration-none py-2 px-3 border rounded bg-light hover-shadow ml-auto" style="transition: all 0.2s ease;">
              <div class="d-none d-sm-block text-right">
                <small class="text-muted d-block font-weight-bold text-uppercase" style="font-size: 11px;" data-i18n="catalog.spv.nav_next">Next Model</small>
                <span class="font-weight-bold" style="font-size: 13.5px;" data-i18n="spv.{next_slug}.title">{html.escape(next_title)}</span>
              </div>
              <div class="d-block d-sm-none text-right">
                <span class="font-weight-bold" style="font-size: 12px;" data-i18n="catalog.spv.nav_next">Next</span>
              </div>
              <span class="ml-2 text-primary" style="font-size: 22px;"><i class="ion-ios-arrow-dropright-circle"></i></span>
            </a>
          </div>
        </div>

        <!-- Disclaimer -->
        <div class="row mt-4">
          <div class="col-12">
            <p class="text-muted" style="font-size: 12.5px; line-height: 1.6;">
              <i class="ion-ios-alert mr-1"></i><span data-i18n="catalog.spv.disclaimer_text">Note: Specifications are as published by the manufacturer; multiple values indicate different available configurations. Please confirm exact technical parameters and chassis options with our export team before ordering.</span>
            </p>
          </div>
        </div>

      </div>
    </section>

    <!-- Floating WhatsApp Button -->
    <a href="https://wa.me/8615168203740?text=Hello%20Rootze%20Team%2C%20I%20am%20interested%20in%20{html.escape(display_title)}." target="_blank" rel="noopener" class="whatsapp-float" title="Chat with Rootze Export Team on WhatsApp">
      <span class="ion-logo-whatsapp"></span>
    </a>

    <!-- Footer -->
    <footer class="ftco-footer ftco-bg-dark ftco-section" style="background: var(--rootze-dark); padding: 70px 0 30px;">
      <div class="container">
        <div class="row mb-5">
          <div class="col-md">
            <div class="ftco-footer-widget mb-4">
              <div class="mb-3">
                <img src="../../images/logo-white.png" alt="Rootze Logo" style="height: 38px; width: auto; object-fit: contain;">
              </div>
              <h5 class="text-white font-weight-bold mb-2" style="font-size: 15px;" data-i18n="brand.legal_name">襄阳如志进出口有限公司</h5>
              <p class="text-light" style="opacity: 0.8; font-size: 13.5px; line-height: 1.7;" data-i18n="footer.about_text">Rootze operates as the authorized international export arm for an equity-partnered coalition of specialized industrial equipment, railway tools, special purpose vehicles, and automotive manufacturing lines in Xiangyang, Hubei, China.</p>
            </div>
          </div>

          <div class="col-md">
            <div class="ftco-footer-widget mb-4 ml-md-5">
              <h2 class="ftco-heading-2 text-white" data-i18n="footer.quick_links">Quick Links</h2>
              <ul class="list-unstyled">
                <li><a href="../../index.html#home" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="nav.home">Home</a></li>
                <li><a href="../../index.html#products" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="nav.products">Products</a></li>
                <li><a href="../../index.html#about" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="nav.about">About Us</a></li>
                <li><a href="../../news.html" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="nav.news">News</a></li>
                <li><a href="../special-vehicles.html#contact" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="nav.contact">Contact</a></li>
              </ul>
            </div>
          </div>

          <div class="col-md">
            <div class="ftco-footer-widget mb-4">
              <h2 class="ftco-heading-2 text-white" data-i18n="footer.products_title">Product Catalogs</h2>
              <ul class="list-unstyled">
                <li><a href="../special-vehicles.html" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="products.cat3_title">Special Purpose Vehicles</a></li>
                <li><a href="../railway-equipment.html" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="products.cat2_title">Railway Equipment & Maintenance Tools</a></li>
                <li><a href="../brake-pad-lines.html" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="products.cat4_title">Brake Pad Manufacturing Equipment</a></li>
                <li><a href="../electrical-systems.html" class="py-1 d-block text-light" style="opacity: 0.8;" data-i18n="products.cat1_title">Industrial Electrical Systems</a></li>
              </ul>
            </div>
          </div>

          <div class="col-md">
            <div class="ftco-footer-widget mb-4">
              <h2 class="ftco-heading-2 text-white" data-i18n="contact.direct_info_title">Contact Information</h2>
              <div class="block-23 mb-3">
                <ul class="list-unstyled">
                  <li class="mb-2"><span class="icon icon-map-marker text-primary mr-2"></span><span class="text text-light" style="opacity: 0.8;" data-i18n="contact.office_val">Dongfeng Automotive & Heavy Machinery Corridor, Xiangyang, Hubei, China</span></li>
                  <li class="mb-2"><a href="https://wa.me/8615168203740" target="_blank" rel="noopener" class="text-light" style="opacity: 0.8;"><span class="icon icon-phone text-primary mr-2"></span><span class="text">+86 151 6820 3740</span></a></li>
                  <li class="mb-2"><a href="mailto:sales@rootzeglobal.com" class="text-light" style="opacity: 0.8;"><span class="icon icon-envelope text-primary mr-2"></span><span class="text">sales@rootzeglobal.com</span></a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="row pt-4 border-top" style="border-color: rgba(255,255,255,0.1) !important;">
          <div class="col-md-12 text-center">
            <p class="text-muted mb-0" style="font-size: 13px;">
              Copyright &copy; <script>document.write(new Date().getFullYear());</script> <span data-i18n="brand.legal_name">襄阳如志进出口有限公司</span> (Xiangyang Rootze Import & Export Co., Ltd.). All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>

    <!-- Scripts -->
    <script src="../../js/jquery.min.js"></script>
    <script src="../../js/popper.min.js"></script>
    <script src="../../js/bootstrap.min.js"></script>
    <script src="../../js/jquery.easing.1.3.js"></script>
    <script src="../../js/jquery.waypoints.min.js"></script>
    <script src="../../js/owl.carousel.min.js"></script>
    <script src="../../js/jquery.magnific-popup.min.js"></script>
    <script src="../../js/aos.js"></script>
    <script src="../../js/jquery.animateNumber.min.js"></script>
    <script src="../../js/i18n.js"></script>
    <script src="../../js/main.js"></script>
  </body>
</html>
'''
    return page_html

def build_card_html_i18n(prod_meta, doc_data):
    doc_file, slug, img, cat_id, display_title, display_title_zh, badge_class, category_name = prod_meta
    
    cat_badge_key = f"catalog.spv.{cat_id}_badge"
    
    model_no = ''
    for s in doc_data['specs']:
        if 'model' in s['key_en'].lower():
            model_no = s['val_en']
            break

    badges = []
    for s in doc_data['specs']:
        k_lower = s['key_en'].lower()
        if 'total capacity' in k_lower or 'effective volume' in k_lower:
            badges.append(s['val_en'])
        elif 'gross vehicle weight' in k_lower or 'gvw' in k_lower:
            badges.append(f"GVW: {s['val_en']}")
        elif 'rated payload' in k_lower:
            badges.append(f"Payload: {s['val_en']}")
        elif 'transported medium' in k_lower:
            badges.append(s['val_en'])
        elif 'cargo box dimensions' in k_lower:
            badges.append(f"Box: {s['val_en']}")
        elif 'cargo body size' in k_lower:
            badges.append(f"Body: {s['val_en']}")
            
    badges_html = ''
    for b in badges[:3]:
        badges_html += f'<span class="spec-badge">{html.escape(b)}</span>\n                      '

    model_badge = ''
    if model_no:
        model_badge = f'<span class="badge badge-dark ml-auto" style="font-size: 11px;">{html.escape(model_no)}</span>'

    short_desc = doc_data['short_en']

    card = f'''          <!-- Card: {html.escape(display_title)} -->
          <div class="col-md-6 col-lg-4 mb-4 ftco-animate">
            <div class="car-wrap rounded h-100 d-flex flex-column bg-white shadow-sm border">
              <a href="vehicles/{slug}.html" class="d-block overflow-hidden rounded-top" style="height: 200px;">
                <div class="img rounded-top" style="background-image: url('../images/products/vehicles/{img}'); height: 200px; background-size: cover; background-position: center; transition: transform 0.3s ease;"></div>
              </a>
              <div class="text p-3 d-flex flex-column flex-grow-1">
                <div class="d-flex align-items-center mb-2">
                  <span class="badge {badge_class}" style="font-size: 11px;" data-i18n="{cat_badge_key}">{category_name}</span>
                  {model_badge}
                </div>
                <h4 class="font-weight-bold mb-2" style="font-size: 15.5px; line-height: 1.4;">
                  <a href="vehicles/{slug}.html" class="text-dark" data-i18n="spv.{slug}.title">{html.escape(display_title)}</a>
                </h4>
                <div class="spec-badge-wrap d-flex flex-wrap mb-2" style="gap: 4px;">
                  {badges_html}
                </div>
                <p class="text-muted mb-3 flex-grow-1" style="font-size: 12.5px; line-height: 1.5;" data-i18n="spv.{slug}.short_desc">
                  {html.escape(short_desc)}
                </p>
                <div class="d-flex mt-auto pt-2 border-top" style="gap: 6px;">
                  <a href="vehicles/{slug}.html" class="btn btn-outline-primary btn-sm flex-grow-1 font-weight-bold py-1">
                    <i class="ion-ios-eye mr-1"></i> <span data-i18n="catalog.spv.btn_specs">Full Specs</span>
                  </a>
                  <a href="#contact" class="btn btn-primary btn-sm font-weight-bold py-1 px-3" data-inquire-cat="{html.escape(display_title)}">
                    <i class="ion-ios-mail mr-1"></i> <span data-i18n="catalog.spv.btn_rfq">RFQ</span>
                  </a>
                </div>
              </div>
            </div>
          </div>\n'''
    return card

def build_main_catalog_section_i18n(parsed_products):
    accordion_items_html = ''
    
    for cat in CATEGORIES:
        cat_id = cat['id']
        cat_products = [p for p in parsed_products if p['meta'][3] == cat_id]
        cat_count = len(cat_products)
        
        cards_html = ''
        for p in cat_products:
            cards_html += build_card_html_i18n(p['meta'], p['data'])
            
        is_show = 'show' if cat['show'] else ''
        aria_expanded = 'true' if cat['show'] else 'false'
        collapsed_class = '' if cat['show'] else 'collapsed'
        
        accordion_items_html += f'''        <!-- Category Item: {cat['title_en']} -->
        <div class="card mb-3 border-0 shadow-sm rounded overflow-hidden">
          <div class="card-header bg-white py-3 px-4 border-bottom-0 {collapsed_class}" id="{cat['heading_id']}" style="cursor: pointer;" data-toggle="collapse" data-target="#{cat['collapse_id']}" aria-expanded="{aria_expanded}" aria-controls="{cat['collapse_id']}">
            <div class="d-flex align-items-center justify-content-between flex-wrap">
              <div class="d-flex align-items-center mb-1 mb-md-0">
                <div class="mr-3 text-primary" style="font-size: 26px; width: 32px;"><i class="{cat['icon']}"></i></div>
                <div>
                  <h3 class="mb-0 font-weight-bold" style="font-size: 18px; color: var(--rootze-dark);" data-i18n="catalog.spv.{cat_id}_title">{cat['title_en']}</h3>
                  <p class="text-muted mb-0" style="font-size: 13px;" data-i18n="catalog.spv.{cat_id}_desc">{cat['desc_en']}</p>
                </div>
              </div>
              <div class="d-flex align-items-center ml-auto">
                <span class="badge {cat['badge_class']} px-3 py-2 mr-3 font-weight-bold" style="font-size: 13px;">{cat_count} Models</span>
                <span class="text-muted font-weight-bold" style="font-size: 18px;"><i class="ion-ios-arrow-down"></i></span>
              </div>
            </div>
          </div>
          <div id="{cat['collapse_id']}" class="collapse {is_show}" aria-labelledby="{cat['heading_id']}">
            <div class="card-body p-3 p-md-4 bg-light">
              <div class="row">
{cards_html}              </div>
            </div>
          </div>
        </div>\n'''

    catalog_section = f'''    <!-- Product Showcase Catalog Accordion (Plan B) -->
    <section class="ftco-section bg-light py-5" id="catalog-section">
      <div class="container">
        <div class="row justify-content-center mb-4">
          <div class="col-md-9 text-center heading-section ftco-animate">
            <span class="subheading" style="color: var(--rootze-primary); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;" data-i18n="catalog.spv.section_badge">Factory Direct Product Matrix</span>
            <h2 class="mb-3" data-i18n="catalog.spv.section_title">Commercial Special Purpose Vehicles & Fleet Catalog</h2>
            <p class="text-muted" data-i18n="catalog.spv.section_desc">Export-certified special utility and transport vehicles engineered on Dongfeng, Auman, Howo, and Sitrak chassis (LHD / RHD). Click on any category to browse our 28 models, or view individual product pages for complete specifications.</p>
          </div>
        </div>

        <!-- Expand / Collapse All Controls & Total Count -->
        <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap" style="gap: 10px;">
          <div class="text-muted font-weight-bold" style="font-size: 14px;">
            <i class="ion-ios-car mr-1 text-primary"></i> <span data-i18n="catalog.spv.total_models_label">4 Vehicle Categories · 28 Export Models</span>
          </div>
          <div class="btn-group" role="group" aria-label="Accordion controls">
            <button type="button" id="btnExpandAll" class="btn btn-sm btn-outline-primary font-weight-bold py-1 px-3" style="font-size: 12.5px;">
              <i class="ion-ios-arrow-down mr-1"></i><span data-i18n="catalog.spv.btn_expand_all">Expand All</span>
            </button>
            <button type="button" id="btnCollapseAll" class="btn btn-sm btn-outline-secondary font-weight-bold py-1 px-3" style="font-size: 12.5px;">
              <i class="ion-ios-arrow-up mr-1"></i><span data-i18n="catalog.spv.btn_collapse_all">Collapse All</span>
            </button>
          </div>
        </div>

        <div class="accordion" id="spvAccordion">
{accordion_items_html}        </div>
      </div>
    </section>'''
    return catalog_section

def rebuild_main_page_i18n(parsed_products):
    print("Rebuilding special-vehicles.html with full data-i18n attributes...")
    with open(MAIN_PAGE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    start_tag = '<!-- Product Showcase Catalog Accordion (Plan B) -->'
    end_tag = '<!-- RFQ Inquiry Form -->'
    
    if start_tag not in content or end_tag not in content:
        start_tag = '<!-- Product Showcase Grid -->'
        
    before = content.split(start_tag)[0]
    after = content.split(end_tag)[1]
    
    catalog_section = build_main_catalog_section_i18n(parsed_products)
    new_content = before + catalog_section + '\n\n    ' + end_tag + after
    
    with open(MAIN_PAGE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("special-vehicles.html successfully updated with data-i18n bindings!")

def sync_all():
    print("Parsing all 28 products with bilingual data and polished translations...")
    parsed_products = []
    
    for meta in PRODUCTS:
        doc_file = meta[0]
        slug = meta[1]
        paras = extract_docx_runs(os.path.join(DOC_DIR, doc_file))
        doc_data = parse_docx_full(paras, slug)
        parsed_products.append({
            'meta': meta,
            'data': doc_data
        })
        
    en_dict, zh_dict = build_bilingual_dictionary(parsed_products)
    update_i18n_js(en_dict, zh_dict)
    
    print("Regenerating 28 detail pages with full data-i18n attributes...")
    for p in parsed_products:
        meta = p['meta']
        slug = meta[1]
        page_html = build_detail_page_i18n(meta, p['data'], parsed_products)
        out_file = os.path.join(OUT_DIR, f"{slug}.html")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
            
    rebuild_main_page_i18n(parsed_products)
    print("Bilingual synchronization and terminology polish complete!")

if __name__ == '__main__':
    sync_all()
