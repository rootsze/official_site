#!/usr/bin/env python3
"""
Extract, copy, and optimize brochure assets for web use.
"""
import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(BASE_DIR, 'resource', 'ProductBrochure')
IMG_DIR = os.path.join(BASE_DIR, 'images', 'products')
VID_DIR = os.path.join(BASE_DIR, 'videos', 'brakelines')

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def ensure_dirs():
    os.makedirs(os.path.join(IMG_DIR, 'electrical'), exist_ok=True)
    os.makedirs(os.path.join(IMG_DIR, 'railway'), exist_ok=True)
    os.makedirs(os.path.join(IMG_DIR, 'brakelines'), exist_ok=True)
    os.makedirs(os.path.join(IMG_DIR, 'vehicles'), exist_ok=True)
    os.makedirs(VID_DIR, exist_ok=True)

def process_electrical():
    # 1. 雷神 SZBB 补偿柜
    szbb_src = os.path.join(RES_DIR, '雷神', 'SZBB', '补偿柜')
    if os.path.exists(szbb_src) and os.listdir(szbb_src):
        f = sorted(os.listdir(szbb_src))[0]
        src = os.path.join(szbb_src, f)
        dst = os.path.join(IMG_DIR, 'electrical', 'szbb-compensation.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}' 2>/dev/null || cp '{src}' '{dst}'")
    else:
        # fallback to product manual image
        src = os.path.join(RES_DIR, '雷神', '产品手册', '产品手册总_页面_010_图像_0001.jpg')
        dst = os.path.join(IMG_DIR, 'electrical', 'szbb-compensation.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}'")

    # 2. 雷神 KYN28 开关柜
    kyn_src = os.path.join(RES_DIR, '雷神', 'KYN28A-12', 'KYN28A-12', '主图')
    if os.path.exists(kyn_src) and os.listdir(kyn_src):
        f = [x for x in os.listdir(kyn_src) if x.lower().endswith(('.jpg', '.png'))][0]
        src = os.path.join(kyn_src, f)
        dst = os.path.join(IMG_DIR, 'electrical', 'kyn28-switchgear.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}' 2>/dev/null || cp '{src}' '{dst}'")
    else:
        src = os.path.join(RES_DIR, '雷神', '产品手册', '产品手册总_页面_020_图像_0001.jpg')
        dst = os.path.join(IMG_DIR, 'electrical', 'kyn28-switchgear.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}'")

    # 3. 雷神 SZGQH / SZYQ 软起
    szgqh_src = os.path.join(RES_DIR, '雷神', 'SZGQH', '主图')
    if os.path.exists(szgqh_src) and os.listdir(szgqh_src):
        f = [x for x in os.listdir(szgqh_src) if x.lower().endswith(('.jpg', '.png'))][0]
        src = os.path.join(szgqh_src, f)
        dst = os.path.join(IMG_DIR, 'electrical', 'szyq-liquid-starter.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}' 2>/dev/null || cp '{src}' '{dst}'")

    # 4. 雷诺尔 RNMV-EI 软起
    rnmv_pdf = os.path.join(RES_DIR, '雷诺尔', 'RNMV-EI智能型高压固态软起动柜[2024 .pdf')
    dst = os.path.join(IMG_DIR, 'electrical', 'rnmv-softstarter.jpg')
    # Generate thumbnail with qlmanage
    run(f"qlmanage -t -s 1000 -o /tmp '{rnmv_pdf}' 2>/dev/null")
    tmp_png = f"/tmp/{os.path.basename(rnmv_pdf)}.png"
    if os.path.exists(tmp_png):
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst}'")
    else:
        # fallback to high-voltage cabinet from Leishen
        src = os.path.join(RES_DIR, '雷神', '产品手册', '产品手册总_页面_005_图像_0001.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}'")

    # 5. 雷诺尔 RNHV 变频器
    rnhv_pdf = os.path.join(RES_DIR, '雷诺尔', 'RNHV系列高压变频器- 全系列.pdf')
    dst = os.path.join(IMG_DIR, 'electrical', 'rnhv-inverter.jpg')
    run(f"qlmanage -t -s 1000 -o /tmp '{rnhv_pdf}' 2>/dev/null")
    tmp_png = f"/tmp/{os.path.basename(rnhv_pdf)}.png"
    if os.path.exists(tmp_png):
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst}'")
    else:
        src = os.path.join(RES_DIR, '雷神', '产品手册', '产品手册总_页面_015_图像_0001.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst}'")

def process_railway():
    # 1. 海特数显轨距尺
    haite_pdf = os.path.join(RES_DIR, '海特', '海特 -印刷版本2026.pdf')
    dst_gauge = os.path.join(IMG_DIR, 'railway', 'haite-digital-gauge.jpg')
    run(f"qlmanage -t -s 1000 -o /tmp '{haite_pdf}' 2>/dev/null")
    tmp_png = f"/tmp/{os.path.basename(haite_pdf)}.png"
    if os.path.exists(tmp_png):
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst_gauge}'")
    else:
        # use template railway image
        src = os.path.join(BASE_DIR, 'images', 'image_4.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst_gauge}'")

    # 2. Linkage 捣固机 & 切轨机
    linkage_pdf = os.path.join(RES_DIR, 'linkage', 'Linkage-宣传册.pdf')
    dst_tamper = os.path.join(IMG_DIR, 'railway', 'linkage-tamper.jpg')
    dst_cutter = os.path.join(IMG_DIR, 'railway', 'linkage-cutter.jpg')
    run(f"qlmanage -t -s 1000 -o /tmp '{linkage_pdf}' 2>/dev/null")
    tmp_png = f"/tmp/{os.path.basename(linkage_pdf)}.png"
    if os.path.exists(tmp_png):
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst_tamper}'")
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst_cutter}'")
    else:
        src = os.path.join(BASE_DIR, 'images', 'image_4.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst_tamper}'")
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst_cutter}'")

def process_brakelines():
    # 1. 拷贝视频
    src_video = os.path.join(RES_DIR, '枣阳 刹车片', '外弧磨和钻孔机.mp4')
    dst_video = os.path.join(VID_DIR, 'outer-arc-grinder.mp4')
    if os.path.exists(src_video):
        shutil.copy2(src_video, dst_video)

    # 2. 生成 poster 封面图和产品加工机床图
    dst_poster = os.path.join(IMG_DIR, 'brakelines', 'video-poster.jpg')
    dst_machine = os.path.join(IMG_DIR, 'brakelines', 'grinder-driller.jpg')
    # Generate thumbnail from mp4
    run(f"qlmanage -t -s 1000 -o /tmp '{src_video}' 2>/dev/null")
    tmp_png = f"/tmp/{os.path.basename(src_video)}.png"
    if os.path.exists(tmp_png):
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst_poster}'")
        run(f"sips -s format jpeg -z 600 800 '{tmp_png}' --out '{dst_machine}'")
    else:
        src = os.path.join(BASE_DIR, 'images', 'image_5.jpg')
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst_poster}'")
        run(f"sips -s format jpeg -z 600 800 '{src}' --out '{dst_machine}'")

def process_vehicles():
    # 从已有高品质车型素材裁剪适配
    src_car1 = os.path.join(BASE_DIR, 'images', 'car-1.jpg')
    src_car2 = os.path.join(BASE_DIR, 'images', 'car-2.jpg')
    dst_truck = os.path.join(IMG_DIR, 'vehicles', 'refrigerated-truck.jpg')
    dst_tanker = os.path.join(IMG_DIR, 'vehicles', 'fuel-tanker.jpg')
    run(f"sips -s format jpeg -z 600 800 '{src_car1}' --out '{dst_truck}'")
    run(f"sips -s format jpeg -z 600 800 '{src_car2}' --out '{dst_tanker}'")

def main():
    print("Extracting and optimizing brochure assets...")
    ensure_dirs()
    process_electrical()
    process_railway()
    process_brakelines()
    process_vehicles()
    print("Done!")

if __name__ == '__main__':
    main()
