import os
import zipfile
import xml.etree.ElementTree as ET
import re
import html
import json

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
        'title_zh': '燃油及液体运输罐车',
        'icon': 'ion-ios-water',
        'badge_class': 'badge-primary',
        'badge_en': 'Fuel Tanker Truck',
        'badge_zh': '燃油运输罐车',
        'desc_en': 'Rigid commercial chassis tanker trucks (15.1 m³ – 30.3 m³) for gasoline, diesel, crude oil, and chemical fluids.',
        'desc_zh': '单桥至四桥商用车底盘运油车（15.1m³ - 30.3m³），适用于汽油、柴油、原油及石脑油运输。',
        'show': True
    },
    {
        'id': 'cat-tanker-semis',
        'heading_id': 'heading-tanker-semis',
        'collapse_id': 'collapse-tanker-semis',
        'title_en': 'Fuel & Fluid Tanker Semi-trailers',
        'title_zh': '燃油及液体运输半挂车',
        'icon': 'ion-ios-speedometer',
        'badge_class': 'badge-primary',
        'badge_en': 'Fuel Tanker Semi-trailer',
        'badge_zh': '燃油运输半挂车',
        'desc_en': 'High-capacity aluminum alloy and carbon steel semi-trailers (37.6 m³ – 49.9 m³) with gooseneck and straight frame designs.',
        'desc_zh': '高容积铝合金及碳钢方圆/圆罐半挂车（37.6m³ - 49.9m³），直梁与鹅颈结构设计。',
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
        'desc_zh': '先进聚氨酯发泡保温箱体，45英尺一体式/分体式冷藏半挂车（空气悬架/板簧）及城配轻型冷藏车。',
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
        'desc_zh': '重型U型自卸车上装、NM450/T700耐磨高强钢箱体、智能物联网抑尘环保顶盖及市政车辆。',
        'show': False
    }
]

SPEC_KEYS = [
    ('spv_key.model', 'Product Model', '产品型号', ['model', '产品型号']),
    ('spv_key.dims', 'Overall Dimensions (L×W×H, mm)', '外形尺寸（长×宽×高，mm）', ['overall dimensions', '外形尺寸']),
    ('spv_key.tank_dims', 'Tank Dimensions (mm)', '罐体尺寸（mm）', ['tank dimensions', '罐体尺寸']),
    ('spv_key.box_dims', 'Cargo Box Dimensions (L×W×H, mm)', '箱体尺寸（长×宽×高，mm）', ['cargo box dimensions', '箱体尺寸']),
    ('spv_key.body_size', 'Cargo Body Dimensions (L×W×H, mm)', '车厢尺寸（mm）', ['cargo body size', '车厢尺寸']),
    ('spv_key.gvw', 'Gross Vehicle Weight (GVW)', '总质量', ['gross vehicle weight', 'gvw', '总质量']),
    ('spv_key.curb', 'Curb Weight', '整备质量', ['curb weight', '整备质量']),
    ('spv_key.payload', 'Rated Payload', '额定载质量', ['rated payload', '额定载质量']),
    ('spv_key.wheelbase', 'Wheelbase', '轴距', ['wheelbase', '轴距']),
    ('spv_key.tank_total', 'Tank Total Capacity', '罐体总容量', ['tank total capacity', '罐体总容量']),
    ('spv_key.tank_eff', 'Effective Volume', '罐体有效容积', ['effective volume', '有效容积']),
    ('spv_key.max_density', 'Max. Density of Approved Medium', '准运介质最大密度', ['max. density', '准运介质最大密度']),
    ('spv_key.medium', 'Transported Medium', '运输介质', ['transported medium', '运输介质']),
    ('spv_key.tank_type', 'Tank Type', '罐体类型', ['tank type', '罐体类型']),
    ('spv_key.design_code', 'Tank Design Code', '罐体设计代码', ['tank design code', '罐体设计代码']),
    ('spv_key.chassis', 'Chassis Platform', '底盘型号', ['chassis', '底盘']),
    ('spv_key.engine', 'Engine Model', '发动机型号', ['engine model', '发动机型号']),
    ('spv_key.batch', 'MIIT Announcement Batch', '工信部公告批次', ['miit announcement batch', '公告批次']),
    ('spv_key.cert', '3C Certificate No.', '3C证书编号', ['3c certificate', '3c证书编号']),
    ('spv_key.box_const', 'Box Construction', '箱体生产工艺', ['box construction', '箱体生产工艺']),
    ('spv_key.insulation', 'Insulation Material', '保温层材质', ['insulation material', '保温层材质']),
    ('spv_key.outer_skin', 'Outer Skin', '外蒙皮材质', ['outer skin', '外蒙皮材质']),
    ('spv_key.inner_skin', 'Inner Skin', '内蒙皮材质', ['inner skin', '内蒙皮材质']),
    ('spv_key.floor', 'Floor Type', '底板类型', ['floor type', '底板类型']),
    ('spv_key.suspension', 'Suspension', '悬架系统', ['suspension', '悬架', '悬挂']),
    ('spv_key.plate', 'Plate Thickness (mm)', '板厚（mm）', ['plate thickness', '板厚']),
    ('spv_key.main_mat', 'Main Material', '主要材料', ['main material', '主要材料']),
    ('spv_key.body_weight', 'Body Weight', '上装自重', ['body weight', '上装自重']),
    ('spv_key.closed_height', 'Closed Height (mm)', '闭合高度（mm）', ['closed height', '闭合高度']),
    ('spv_key.cylinder', 'Hydraulic Cylinder', '举升油缸', ['hydraulic cylinder', '油缸']),
    ('spv_key.body_struct', 'Body Structure', '车厢结构', ['body structure', '车厢结构'])
]

PRODUCTS = [
    # Fuel Tanker Trucks (9 models)
    ('15.1立方欧曼牌运油车_15.1m3 Auman Fuel Tanker Truck.docx', 'fuel-tanker-15m3-auman', 'fuel-tanker-15m3-auman.jpg', 'cat-tanker-trucks', '15.1m³ Auman Fuel Tanker Truck', '15.1立方欧曼牌运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('18.1立方易燃液体罐式运输车_18.1m3 Flammable Liquid Tank Truck.docx', 'fuel-tanker-18m3-flammable', 'fuel-tanker-18m3-flammable.jpg', 'cat-tanker-trucks', '18.1m³ Flammable Liquid Tank Truck', '18.1立方易燃液体罐式运输车', 'badge-primary', 'Flammable Liquid Tank Truck'),
    ('21.4立方易燃液体罐式运输车_21.4m3 Flammable Liquid Tank Truck.docx', 'fuel-tanker-21m3-flammable', 'fuel-tanker-21m3-flammable.jpg', 'cat-tanker-trucks', '21.4m³ Flammable Liquid Tank Truck', '21.4立方易燃液体罐式运输车', 'badge-primary', 'Flammable Liquid Tank Truck'),
    ('21立方东风易燃液体罐式运输车_21m3 Dongfeng Flammable Liquid Tank Truck.docx', 'fuel-tanker-21m3-dongfeng', 'fuel-tanker-21m3-dongfeng.png', 'cat-tanker-trucks', '21m³ Dongfeng Flammable Liquid Tank Truck', '21立方东风易燃液体罐式运输车', 'badge-primary', 'Flammable Liquid Tank Truck'),
    ('25.8立方欧曼牌铝合金运油车_25.8m3 Auman Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-258m3-auman-alloy', 'fuel-tanker-258m3-auman-alloy.png', 'cat-tanker-trucks', '25.8m³ Auman Aluminum Alloy Fuel Tanker Truck', '25.8立方欧曼牌铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('26.5立方欧曼牌运油车_26.5m3 Auman Fuel Tanker Truck.docx', 'fuel-tanker-265m3-auman', 'fuel-tanker-265m3-auman.jpg', 'cat-tanker-trucks', '26.5m³ Auman Fuel Tanker Truck', '26.5立方欧曼牌运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('26立方东风牌铝合金运油车_26m3 Dongfeng Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-26m3-dongfeng-alloy', 'fuel-tanker-26m3-dongfeng-alloy.jpg', 'cat-tanker-trucks', '26m³ Dongfeng Aluminum Alloy Fuel Tanker Truck', '26立方东风牌铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('26立方铝合金运油车_26m3 Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-26m3-alloy', 'fuel-tanker-26m3-alloy.jpg', 'cat-tanker-trucks', '26m³ Aluminum Alloy Fuel Tanker Truck', '26立方铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    ('30.3立方东风牌铝合金运油车_30.3m3 Dongfeng Aluminum Alloy Fuel Tanker Truck.docx', 'fuel-tanker-303m3-dongfeng-alloy', 'fuel-tanker-303m3-dongfeng-alloy.jpg', 'cat-tanker-trucks', '30.3m³ Dongfeng Aluminum Alloy Fuel Tanker Truck', '30.3立方东风牌铝合金运油车', 'badge-primary', 'Fuel Tanker Truck'),
    
    # Fuel Tanker Semi-trailers (11 models)
    ('37.6立方欧曼牌铝合金运油半挂车_37.6m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-376m3-auman-alloy', 'semi-tanker-376m3-auman-alloy.png', 'cat-tanker-semis', '37.6m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '37.6立方欧曼牌铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('38.5立方欧曼牌铝合金运油半挂车_38.5m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-385m3-auman', 'semi-tanker-385m3-auman.jpg', 'cat-tanker-semis', '38.5m³ Auman Fuel Tanker Semi-trailer', '38.5立方欧曼牌铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('40.4立方欧曼牌铝合金运油半挂车_40.4m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-404m3-auman-alloy', 'semi-tanker-404m3-auman-alloy.jpg', 'cat-tanker-semis', '40.4m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '40.4立方欧曼牌铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('42立方铝合金运油半挂车_42m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-42m3-alloy', 'semi-tanker-42m3-alloy.png', 'cat-tanker-semis', '42m³ Aluminum Alloy Fuel Tanker Semi-trailer', '42立方铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('43立方铝合金易燃液体罐式运输半挂车_43m3 Aluminum Alloy Flammable Liquid Tank Semi-trailer(2).docx', 'semi-tanker-43m3-flammable-a', 'semi-tanker-43m3-flammable-a.jpg', 'cat-tanker-semis', '43m³ Aluminum Alloy Flammable Liquid Tank Semi-trailer (Model A)', '43立方铝合金易燃液体罐式半挂车 (A型 乙醇/溶剂油)', 'badge-primary', 'Flammable Liquid Semi-trailer'),
    ('43立方铝合金易燃液体罐式运输半挂车_43m3 Aluminum Alloy Flammable Liquid Tank Semi-trailer.docx', 'semi-tanker-43m3-flammable-b', 'semi-tanker-43m3-flammable-b.png', 'cat-tanker-semis', '43m³ Aluminum Alloy Flammable Liquid Tank Semi-trailer (Model B)', '43立方铝合金易燃液体罐式半挂车 (B型 甲醇/乙醇)', 'badge-primary', 'Flammable Liquid Semi-trailer'),
    ('45立方铝合金运油半挂车_45m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-45m3-alloy', 'semi-tanker-45m3-alloy.jpg', 'cat-tanker-semis', '45m³ Aluminum Alloy Fuel Tanker Semi-trailer', '45立方铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('46.1立方铝合金运油半挂车_46.1m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-461m3-alloy', 'semi-tanker-461m3-alloy.jpg', 'cat-tanker-semis', '46.1m³ Aluminum Alloy Fuel Tanker Semi-trailer', '46.1立方铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('47立方欧曼牌铝合金运油半挂车_47m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-47m3-auman-alloy', 'semi-tanker-47m3-auman-alloy.jpg', 'cat-tanker-semis', '47m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '47立方欧曼牌铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('48立方铝合金运油半挂车_48m3 Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-48m3-alloy', 'semi-tanker-48m3-alloy.png', 'cat-tanker-semis', '48m³ Aluminum Alloy Fuel Tanker Semi-trailer', '48立方铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    ('49.9立方欧曼牌铝合金运油半挂车_49.9m3 Auman Aluminum Alloy Fuel Tanker Semi-trailer.docx', 'semi-tanker-499m3-auman-alloy', 'semi-tanker-499m3-auman-alloy.jpg', 'cat-tanker-semis', '49.9m³ Auman Aluminum Alloy Fuel Tanker Semi-trailer', '49.9立方欧曼牌铝合金运油半挂车', 'badge-primary', 'Fuel Tanker Semi-trailer'),
    
    # Refrigerated Vehicles (5 models)
    ('欧曼牌冷藏车_Auman Refrigerated Truck.docx', 'reefer-truck-auman', 'reefer-truck-auman.jpg', 'cat-reefer', 'Auman Light-Duty Refrigerated Truck', '欧曼牌城配冷藏车', 'badge-info', 'Refrigerated Truck'),
    ('8米五十铃冷藏车_8m Isuzu Refrigerated Truck.docx', 'reefer-truck-8m-isuzu', 'reefer-truck-8m-isuzu.jpg', 'cat-reefer', '8m Isuzu Refrigerated Truck', '8米五十铃冷藏车', 'badge-info', 'Refrigerated Truck'),
    ('45英尺一体式冷藏半挂车（板簧）_45ft Integrated Refrigerated Semi-trailer (Leaf Spring).docx', 'reefer-semi-45ft-leaf-spring', 'reefer-semi-45ft-leaf-spring.jpg', 'cat-reefer', '45ft Integrated Refrigerated Semi-trailer (Leaf Spring)', '45英尺一体式冷藏半挂车 (板簧悬架)', 'badge-info', 'Refrigerated Semi-trailer'),
    ('45英尺一体式冷藏半挂车（空悬）_45ft Integrated Refrigerated Semi-trailer (Air Suspension).docx', 'reefer-semi-45ft-air-suspension', 'reefer-semi-45ft-air-suspension.png', 'cat-reefer', '45ft Integrated Refrigerated Semi-trailer (Air Suspension)', '45英尺一体式冷藏半挂车 (空气悬架)', 'badge-info', 'Refrigerated Semi-trailer'),
    ('45英尺分体式冷藏半挂车_45ft Split-type Refrigerated Semi-trailer.docx', 'reefer-semi-45ft-split', 'reefer-semi-45ft-split.jpg', 'cat-reefer', '45ft Split-type Refrigerated Semi-trailer', '45英尺分体式冷藏半挂车', 'badge-info', 'Refrigerated Semi-trailer'),
    
    # Engineering Vehicles (3 models)
    ('工程车1_Engineering Vehicle 1.docx', 'engineering-vehicle-1', 'engineering-vehicle-1.png', 'cat-engineering', 'Engineering Vehicle 1 (U-Box Body, 510L Steel)', '工程车1 (U型自卸上装 510L特钢)', 'badge-secondary', 'Engineering Vehicle'),
    ('工程车2_Engineering Vehicle 2.docx', 'engineering-vehicle-2', 'engineering-vehicle-2.jpg', 'cat-engineering', 'Engineering Vehicle 2 (Standard Heavy-Duty Body)', '工程车2 (标准重载工程车)', 'badge-secondary', 'Engineering Vehicle'),
    ('工程车3_Engineering Vehicle 3.docx', 'engineering-vehicle-3', 'engineering-vehicle-3.jpg', 'cat-engineering', 'Engineering Vehicle 3 (U-Box Body, T700 / IoT)', '工程车3 (U型自卸上装 T700高强钢 / 智能顶盖)', 'badge-secondary', 'Engineering Vehicle')
]

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

def sanitize_en(text):
    if not text:
        return ''
    text = re.sub(r'Manufactured by Hubei Forze Motor Co\.,Ltd\s*\(Model\s*[^)]+\)\.\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Manufactured by Hubei Forze Motor Co\.,Ltd\.\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'An engineering-vehicle body built by Forze\b', 'An engineering-vehicle body engineered for heavy-duty commercial applications', text, flags=re.IGNORECASE)
    text = re.sub(r'An engineering vehicle built by Forze\b', 'An engineering vehicle built for commercial infrastructure operations', text, flags=re.IGNORECASE)
    text = re.sub(r'A light-duty refrigerated truck built by Forze\b', 'A light-duty commercial refrigerated truck', text, flags=re.IGNORECASE)
    text = re.sub(r'\bForze\b', 'Rootze Partner Coalition', text)
    text = re.sub(r'\bHubei Forze\b', 'Xiangyang Automotive Manufacturing Base', text)
    text = re.sub(r'湖北福智汽车有限公司', '', text)
    text = re.sub(r'福智汽车', '', text)
    text = text.strip()
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    return text

def sanitize_zh(text):
    if not text:
        return ''
    text = re.sub(r'该车由湖北福智汽车有限公司生产，\s*', '该车', text)
    text = re.sub(r'由湖北福智汽车有限公司生产，\s*', '', text)
    text = re.sub(r'该车为福智汽车生产的\s*', '该车为高品质', text)
    text = re.sub(r'福智汽车生产的工程车，属于公司专用车产品线（工程车、罐式车、冷厢车）之一。', '重型工程专用车，属于特种车辆核心产品线之一。', text)
    text = re.sub(r'福智汽车生产的\s*', '', text)
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

def extract_val_pair(texts):
    if len(texts) == 1:
        s = texts[0]
        m = re.match(r'^([\u4e00-\u9fff\uff08\uff09\u3001\uff0c\s]+)([A-Za-z].*)$', s)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        return s, s
    zh_parts = []
    en_parts = []
    for t in texts:
        if re.search(r'[\u4e00-\u9fff]', t):
            zh_parts.append(t)
        else:
            en_parts.append(t)
    if zh_parts and en_parts:
        return ' '.join(zh_parts).strip(), ' '.join(en_parts).strip()
    return ' '.join(texts).strip(), ' '.join(texts).strip()

def parse_docx_full(paras):
    data = {
        'zh_title': ''.join(paras[0]) if len(paras) > 0 else '',
        'en_title': ' '.join(paras[1]) if len(paras) > 1 else '',
        'overview_zh': '',
        'overview_en': '',
        'specs': [],
        'optional_zh': '',
        'optional_en': '',
        'features': []
    }
    
    i = 2
    while i < len(paras):
        p_join = ''.join(paras[i])
        
        if 'Product Overview' in p_join or '产品简介' in p_join:
            if i + 1 < len(paras):
                data['overview_zh'] = ''.join(paras[i+1])
            if i + 2 < len(paras):
                p2_join = ''.join(paras[i+2])
                if not any(h in p2_join for h in ['Key Specifications', '主要参数', '上装技术参数', 'Body Technical Parameters', 'Features', '产品特点']):
                    data['overview_en'] = ' '.join(paras[i+2])
                    i += 3
                    continue
            i += 2
            continue
            
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
                    v_zh, v_en = extract_val_pair(val_texts)
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
                # Pair of zh and en features
                feat_zh = ''.join(paras[i])
                feat_en = ' '.join(paras[i+1]) if i + 1 < len(paras) and not paras[i+1][0].startswith('注：') else feat_zh
                data['features'].append({
                    'zh': feat_zh,
                    'en': feat_en
                })
                i += 2
            continue
            
        i += 1
        
    data['overview_en'] = sanitize_en(data['overview_en'])
    data['overview_zh'] = sanitize_zh(data['overview_zh'])
    data['optional_en'] = sanitize_en(data['optional_en'])
    data['optional_zh'] = sanitize_zh(data['optional_zh'])
    return data

def build_bilingual_dictionary(parsed_products):
    en_dict = {}
    zh_dict = {}

    # Category and shared UI keys
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
    zh_dict['catalog.spv.disclaimer_text'] = '注：以上参数为公布数据；多个数值表示不同可选配置，具体以采购合同及实际选配为准。'

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
        
        # Short description for catalog card
        short_en = data['overview_en']
        if len(short_en) > 130: short_en = short_en[:127] + '...'
        short_zh = data['overview_zh']
        if len(short_zh) > 80: short_zh = short_zh[:77] + '...'
        en_dict[f'spv.{slug}.short_desc'] = short_en
        zh_dict[f'spv.{slug}.short_desc'] = short_zh
        
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


def build_detail_page_i18n(prod_meta, doc_data):
    doc_file, slug, img, cat_id, display_title, display_title_zh, badge_class, category_name = prod_meta
    
    # Category metadata
    cat_obj = next(c for c in CATEGORIES if c['id'] == cat_id)
    cat_badge_key = f"catalog.spv.{cat_id}_badge"
    
    model_no = ''
    for s in doc_data['specs']:
        if 'model' in s['key_en'].lower():
            model_no = s['val_en']
            break
            
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

    # Spec rows
    spec_rows_html = ''
    if doc_data['specs']:
        for s_idx, s in enumerate(doc_data['specs']):
            sk_id = s['sk_id']
            k_en = html.escape(s['key_en'])
            v_en = html.escape(s['val_en'])
            
            # Check if value has translation key
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
          <!-- Left: Product Image -->
          <div class="col-lg-5 mb-4 mb-lg-0">
            <div class="border rounded p-3 bg-white shadow-sm text-center">
              <img src="../../images/products/vehicles/{img}" alt="{html.escape(display_title)}" class="img-fluid rounded" style="width: 100%; max-height: 420px; object-fit: contain; background: #fdfdfd;">
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
              <a href="../special-vehicles.html#contact" class="btn btn-primary py-2 px-4 font-weight-bold mr-2"><i class="ion-ios-paper-plane mr-1"></i> <span data-i18n="catalog.spv.btn_quote">Request a Factory Quote</span></a>
              <a href="../special-vehicles.html" class="btn btn-outline-secondary py-2 px-3 font-weight-bold"><i class="ion-ios-arrow-back mr-1"></i> <span data-i18n="catalog.spv.btn_back">Back to Vehicle Catalog</span></a>
            </div>
          </div>
        </div>

{specs_section_html}

{optional_section_html}

{features_section_html}

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

    short_desc = doc_data['overview_en']
    if len(short_desc) > 130:
        short_desc = short_desc[:127] + '...'

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
          <div id="{cat['collapse_id']}" class="collapse {is_show}" aria-labelledby="{cat['heading_id']}" data-parent="#spvAccordion">
            <div class="card-body p-3 p-md-4 bg-light">
              <div class="row">
{cards_html}              </div>
            </div>
          </div>
        </div>\n'''

    catalog_section = f'''    <!-- Product Showcase Catalog Accordion (Plan B) -->
    <section class="ftco-section bg-light py-5" id="catalog-section">
      <div class="container">
        <div class="row justify-content-center mb-5">
          <div class="col-md-9 text-center heading-section ftco-animate">
            <span class="subheading" style="color: var(--rootze-primary); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;" data-i18n="catalog.spv.section_badge">Factory Direct Product Matrix</span>
            <h2 class="mb-3" data-i18n="catalog.spv.section_title">Commercial Special Purpose Vehicles & Fleet Catalog</h2>
            <p class="text-muted" data-i18n="catalog.spv.section_desc">Export-certified special utility and transport vehicles engineered on Dongfeng, Auman, Howo, and Sitrak chassis. Click on any category to browse our 28 models, or view individual product pages for complete specifications.</p>
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
        # Fallback to legacy tag if needed
        start_tag = '<!-- Product Showcase Grid -->'
        
    before = content.split(start_tag)[0]
    after = content.split(end_tag)[1]
    
    catalog_section = build_main_catalog_section_i18n(parsed_products)
    new_content = before + catalog_section + '\n\n    ' + end_tag + after
    
    with open(MAIN_PAGE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("special-vehicles.html successfully updated with data-i18n bindings!")

def sync_all():
    print("Parsing all 28 products with bilingual data...")
    parsed_products = []
    
    for meta in PRODUCTS:
        doc_file = meta[0]
        paras = extract_docx_runs(os.path.join(DOC_DIR, doc_file))
        doc_data = parse_docx_full(paras)
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
        page_html = build_detail_page_i18n(meta, p['data'])
        out_file = os.path.join(OUT_DIR, f"{slug}.html")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(page_html)
            
    rebuild_main_page_i18n(parsed_products)
    print("Bilingual synchronization complete!")

if __name__ == '__main__':
    sync_all()
