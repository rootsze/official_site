#!/usr/bin/env python3
"""
Extract, render, crop, and optimize brochure assets for web use.
Generates:
- 1920x600 Hero Cover Banners with contrast darkening for white typography
- 800x600 standardized Product Card and Equipment Visuals
- Turnkey manufacturing process equipment thumbnails and video poster
"""
import os
import shutil
import subprocess
from PIL import Image, ImageEnhance

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_DIR = os.path.join(BASE_DIR, 'resource', 'ProductBrochure')
IMG_DIR = os.path.join(BASE_DIR, 'images', 'products')
VID_DIR = os.path.join(BASE_DIR, 'videos', 'brakelines')

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

def ensure_dirs():
    os.makedirs(os.path.join(IMG_DIR, 'electrical'), exist_ok=True)
    os.makedirs(os.path.join(IMG_DIR, 'railway'), exist_ok=True)
    os.makedirs(os.path.join(IMG_DIR, 'brakelines'), exist_ok=True)
    os.makedirs(os.path.join(IMG_DIR, 'vehicles'), exist_ok=True)
    os.makedirs(VID_DIR, exist_ok=True)

def render_pdf_page(pdf_path, page_index, out_path, scale=2.0):
    """Render a specific PDF page using Swift / PDFKit if on macOS, or fallback to qlmanage."""
    swift_script = f'''
import PDFKit
import Cocoa

let url = URL(fileURLWithPath: "{pdf_path}")
guard let doc = PDFDocument(url: url), let page = doc.page(at: {page_index}) else {{
    exit(1)
}}
let rect = page.bounds(for: .mediaBox)
let scale: CGFloat = {scale}
let size = NSSize(width: rect.width * scale, height: rect.height * scale)
let img = NSImage(size: size)
img.lockFocus()
if let ctx = NSGraphicsContext.current?.cgContext {{
    ctx.setFillColor(NSColor.white.cgColor)
    ctx.fill(CGRect(origin: .zero, size: size))
    ctx.scaleBy(x: scale, y: scale)
    page.draw(with: .mediaBox, to: ctx)
}}
img.unlockFocus()
if let tiff = img.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff), let png = rep.representation(using: .png, properties: [:]) {{
    try? png.write(to: URL(fileURLWithPath: "{out_path}"))
}}
'''
    try:
        subprocess.run(['swift', '-e', swift_script], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # Fallback to qlmanage
        tmp_dir = '/tmp'
        subprocess.run(f"qlmanage -t -s 1200 -o '{tmp_dir}' '{pdf_path}' 2>/dev/null", shell=True)
        tmp_png = os.path.join(tmp_dir, f"{os.path.basename(pdf_path)}.png")
        if os.path.exists(tmp_png):
            shutil.copy2(tmp_png, out_path)

def extract_video_frame(video_path, timestamp_sec, out_path):
    """Extract a frame from video using ffmpeg or fallback to qlmanage."""
    try:
        run_cmd(f"ffmpeg -ss {timestamp_sec} -i '{video_path}' -vframes 1 -q:v 2 '{out_path}' -y 2>/dev/null")
    except Exception:
        run_cmd(f"qlmanage -t -s 1200 -o /tmp '{video_path}' 2>/dev/null")
        tmp_png = f"/tmp/{os.path.basename(video_path)}.png"
        if os.path.exists(tmp_png):
            shutil.copy2(tmp_png, out_path)

def crop_and_resize(src_path, dst_path, target_w=800, target_h=600, dark_factor=1.0, quality=90):
    """Crop image to target aspect ratio (centered) and resize with high-quality resampling."""
    im = Image.open(src_path).convert('RGB')
    w, h = im.size
    target_ratio = target_w / target_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Crop width
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        # Crop height
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))

    im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    if dark_factor != 1.0:
        enhancer = ImageEnhance.Brightness(im)
        im = enhancer.enhance(dark_factor)
    im.save(dst_path, 'JPEG', quality=quality, optimize=True)

def process_electrical():
    print("Processing Electrical Systems assets...")
    elec_dir = os.path.join(IMG_DIR, 'electrical')

    # 1. Hero Banner (1920x600, dark_factor=0.55 for white text readability)
    rnhv_cover = '/tmp/renle_rnhv_p0.png'
    rnhv_pdf = os.path.join(RES_DIR, '雷诺尔', 'RNHV系列高压变频器- 全系列.pdf')
    if not os.path.exists(rnhv_cover):
        render_pdf_page(rnhv_pdf, 0, rnhv_cover, scale=2.5)
    
    hero_dst = os.path.join(elec_dir, 'hero-electrical.jpg')
    if os.path.exists(rnhv_cover):
        crop_and_resize(rnhv_cover, hero_dst, 1920, 600, dark_factor=0.55, quality=90)
    else:
        fallback = os.path.join(RES_DIR, '雷神', '产品手册', '产品手册总_页面_001_图像_0001.jpg')
        crop_and_resize(fallback, hero_dst, 1920, 600, dark_factor=0.55, quality=90)

    # 2. RNMV-EI Soft Starter (800x600)
    rnmv_cover = '/tmp/renle_rnmv_p0.png'
    rnmv_pdf = os.path.join(RES_DIR, '雷诺尔', 'RNMV-EI智能型高压固态软起动柜[2024 .pdf')
    if not os.path.exists(rnmv_cover):
        render_pdf_page(rnmv_pdf, 0, rnmv_cover, scale=2.0)
    dst_rnmv = os.path.join(elec_dir, 'rnmv-softstarter.jpg')
    if os.path.exists(rnmv_cover):
        crop_and_resize(rnmv_cover, dst_rnmv, 800, 600)

    # 3. RNHV High-Voltage Inverter (800x600)
    dst_rnhv = os.path.join(elec_dir, 'rnhv-inverter.jpg')
    if os.path.exists(rnhv_cover):
        crop_and_resize(rnhv_cover, dst_rnhv, 800, 600)

    # 4. Leishen SZBB Reactive Power Compensation Cabinet (800x600)
    szbb_src = os.path.join(RES_DIR, '雷神', 'SZBB', 'SZBB', '主图')
    dst_szbb = os.path.join(elec_dir, 'szbb-compensation.jpg')
    if os.path.exists(szbb_src):
        candidates = [os.path.join(szbb_src, f) for f in os.listdir(szbb_src) if f.endswith('.jpg')]
        best_szbb = sorted(candidates)[0]
        crop_and_resize(best_szbb, dst_szbb, 800, 600)

    # 5. Leishen KYN28A-12 Switchgear (800x600)
    kyn_src = os.path.join(RES_DIR, '雷神', 'KYN28A-12', 'KYN28A-12', '主图')
    dst_kyn = os.path.join(elec_dir, 'kyn28-switchgear.jpg')
    if os.path.exists(kyn_src):
        candidates = [os.path.join(kyn_src, f) for f in os.listdir(kyn_src) if f.endswith('.jpg')]
        best_kyn = sorted(candidates)[0]
        crop_and_resize(best_kyn, dst_kyn, 800, 600)

    # 6. Leishen SZYQ / SZGQH Liquid Starter (800x600)
    szgqh_src = os.path.join(RES_DIR, '雷神', 'SZGQH', '主图')
    dst_szyq = os.path.join(elec_dir, 'szyq-liquid-starter.jpg')
    if os.path.exists(szgqh_src):
        candidates = [os.path.join(szgqh_src, f) for f in os.listdir(szgqh_src) if f.endswith('.jpg')]
        best_szgqh = sorted(candidates)[0]
        crop_and_resize(best_szgqh, dst_szyq, 800, 600)

def process_railway():
    print("Processing Railway Equipment assets...")
    rail_dir = os.path.join(IMG_DIR, 'railway')

    # Render Haite & Linkage brochure pages
    haite_pdf = os.path.join(RES_DIR, '海特', '海特 -印刷版本2026.pdf')
    linkage_pdf = os.path.join(RES_DIR, 'linkage', 'Linkage-宣传册.pdf')

    haite_p1 = '/tmp/haite_p1.png'
    haite_p3 = '/tmp/haite_p3.png'
    haite_p5 = '/tmp/haite_p5.png'
    linkage_p1 = '/tmp/linkage_p1.png'
    linkage_p2 = '/tmp/linkage_p2.png'
    linkage_p3 = '/tmp/linkage_p3.png'

    render_pdf_page(haite_pdf, 0, haite_p1, scale=2.0)
    render_pdf_page(haite_pdf, 2, haite_p3, scale=2.0)
    render_pdf_page(haite_pdf, 4, haite_p5, scale=2.0)

    render_pdf_page(linkage_pdf, 0, linkage_p1, scale=2.0)
    render_pdf_page(linkage_pdf, 1, linkage_p2, scale=2.0)
    render_pdf_page(linkage_pdf, 2, linkage_p3, scale=2.0)

    # 1. Hero Banner (1920x600, dark_factor=0.55 for white text readability)
    hero_dst = os.path.join(rail_dir, 'hero-railway.jpg')
    if os.path.exists(haite_p1):
        crop_and_resize(haite_p1, hero_dst, 1920, 600, dark_factor=0.55, quality=90)
    elif os.path.exists(linkage_p1):
        crop_and_resize(linkage_p1, hero_dst, 1920, 600, dark_factor=0.55, quality=90)

    # 2. Haite Digital Track Gauge (800x600)
    dst_gauge = os.path.join(rail_dir, 'haite-digital-gauge.jpg')
    src_gauge = haite_p3 if os.path.exists(haite_p3) else haite_p1
    crop_and_resize(src_gauge, dst_gauge, 800, 600)

    # 3. Linkage Tamper (800x600)
    dst_tamper = os.path.join(rail_dir, 'linkage-tamper.jpg')
    src_tamper = linkage_p2 if os.path.exists(linkage_p2) else linkage_p1
    crop_and_resize(src_tamper, dst_tamper, 800, 600)

    # 4. Linkage Rail Cutter (800x600)
    dst_cutter = os.path.join(rail_dir, 'linkage-cutter.jpg')
    src_cutter = linkage_p3 if os.path.exists(linkage_p3) else linkage_p1
    crop_and_resize(src_cutter, dst_cutter, 800, 600)

    # 5. Haite Turnout Gauge / Rail Tensor (800x600)
    dst_turnout = os.path.join(rail_dir, 'haite-turnout-gauge.jpg')
    src_turnout = haite_p5 if os.path.exists(haite_p5) else haite_p3
    crop_and_resize(src_turnout, dst_turnout, 800, 600)

def process_brakelines():
    print("Processing Brake Pad Lines assets...")
    brake_dir = os.path.join(IMG_DIR, 'brakelines')

    # Copy video
    src_video = os.path.join(RES_DIR, '枣阳 刹车片', '外弧磨和钻孔机.mp4')
    dst_video = os.path.join(VID_DIR, 'outer-arc-grinder.mp4')
    if os.path.exists(src_video) and not os.path.exists(dst_video):
        shutil.copy2(src_video, dst_video)

    # Extract high-definition frames from Zaoyang workshop videos
    vid_dfe = os.path.join(RES_DIR, '枣阳 刹车片', 'dfe34cbb2178196838ace1e69e86400e.mp4')
    vid_a01 = os.path.join(RES_DIR, '枣阳 刹车片', 'a0145f5c4aa31ebd902057d8a05f3580.mp4')
    vid_89c = os.path.join(RES_DIR, '枣阳 刹车片', '89ce9d79a57b6c2a4eb5f7d3d60ff3dd.mp4')

    frame_hero = '/tmp/zaoyang_hero_frame.jpg'
    frame_press = '/tmp/zaoyang_press_frame.jpg'
    frame_furnace = '/tmp/zaoyang_furnace_frame.jpg'
    frame_mixer = '/tmp/zaoyang_mixer_frame.jpg'
    frame_grinder = '/tmp/zaoyang_grinder_frame.jpg'

    extract_video_frame(vid_dfe, 30, frame_hero)
    extract_video_frame(vid_a01, 60, frame_press)
    extract_video_frame(vid_dfe, 90, frame_furnace)
    extract_video_frame(vid_89c, 15, frame_mixer)
    extract_video_frame(src_video, 5, frame_grinder)

    # 1. Hero Banner (1920x600, dark_factor=0.55 for white text readability)
    hero_dst = os.path.join(brake_dir, 'hero-brakelines.jpg')
    crop_and_resize(frame_hero, hero_dst, 1920, 600, dark_factor=0.55, quality=90)

    # 2. Video Poster (976x576) & Grinder-Driller Machine Thumbnail (800x600)
    dst_poster = os.path.join(brake_dir, 'video-poster.jpg')
    dst_machine = os.path.join(brake_dir, 'grinder-driller.jpg')
    crop_and_resize(frame_grinder, dst_poster, 976, 576, quality=90)
    crop_and_resize(frame_grinder, dst_machine, 800, 600, quality=90)

    # 3. Multi-Cavity Hydraulic Press (800x600)
    dst_press = os.path.join(brake_dir, 'hydraulic-press.jpg')
    crop_and_resize(frame_press, dst_press, 800, 600, quality=90)

    # 4. Continuous Tunnel Curing Oven (800x600)
    dst_furnace = os.path.join(brake_dir, 'tunnel-furnace.jpg')
    crop_and_resize(frame_furnace, dst_furnace, 800, 600, quality=90)

    # 5. Precision Mixing System (800x600)
    dst_mixer = os.path.join(brake_dir, 'mixing-system.jpg')
    crop_and_resize(frame_mixer, dst_mixer, 800, 600, quality=90)

def process_vehicles():
    print("Processing Special Purpose Vehicles assets...")
    veh_dir = os.path.join(IMG_DIR, 'vehicles')

    src_car1 = os.path.join(BASE_DIR, 'images', 'car-1.jpg')
    src_car2 = os.path.join(BASE_DIR, 'images', 'car-2.jpg')
    src_car9 = os.path.join(BASE_DIR, 'images', 'car-9.jpg')
    src_car10 = os.path.join(BASE_DIR, 'images', 'car-10.jpg')

    # 1. Hero Banner (1920x600, dark_factor=0.55 for white text readability)
    hero_dst = os.path.join(veh_dir, 'hero-vehicles.jpg')
    crop_and_resize(src_car1, hero_dst, 1920, 600, dark_factor=0.55, quality=90)

    # 2. Cold Chain Refrigerated Truck (800x600)
    dst_refrig = os.path.join(veh_dir, 'refrigerated-truck.jpg')
    crop_and_resize(src_car1, dst_refrig, 800, 600, quality=90)

    # 3. Heavy Fuel & Water Tanker (800x600)
    dst_tanker = os.path.join(veh_dir, 'fuel-tanker.jpg')
    crop_and_resize(src_car2, dst_tanker, 800, 600, quality=90)

    # 4. Municipal Road Sweeper & High-Pressure Jetting Truck (800x600)
    dst_sweeper = os.path.join(veh_dir, 'sweeper-truck.jpg')
    crop_and_resize(src_car10, dst_sweeper, 800, 600, quality=90)

    # 5. Heavy-Duty Dump Tipper Truck (800x600)
    dst_dump = os.path.join(veh_dir, 'heavy-dump-truck.jpg')
    crop_and_resize(src_car9, dst_dump, 800, 600, quality=90)

def main():
    print("Extracting, rendering, and optimizing brochure assets...")
    ensure_dirs()
    process_electrical()
    process_railway()
    process_brakelines()
    process_vehicles()
    print("All assets successfully generated!")

if __name__ == '__main__':
    main()
