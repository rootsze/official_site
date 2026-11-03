#!/usr/bin/env python3
"""
Update and optimize imagery for Special Purpose Vehicles (商用特种改装车辆与工程运输车队)
Downloads and processes authentic, high-resolution commercial truck photography
matching the technical specifications on products/special-vehicles.html.
"""

import os
import sys
import time
import urllib.request
from PIL import Image, ImageEnhance

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'images', 'products', 'vehicles')
CACHE_DIR = os.path.join(BASE_DIR, 'resource', 'vehicles_cache')

HEADERS = {
    'User-Agent': 'RootzeIndustrialBot/1.0 (https://rootzeglobal.com; export@rootzeglobal.com)'
}

ASSETS = [
    {
        'filename': 'hero-vehicles.jpg',
        'cache_name': 'fleet_parked.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Trucks_parked_in_USA.jpg/1920px-Trucks_parked_in_USA.jpg',
        'width': 1920,
        'height': 600,
        'dark_factor': 0.60,
        'quality': 88,
        'description': 'Commercial utility & engineering truck fleet lineup'
    },
    {
        'filename': 'refrigerated-truck.jpg',
        'cache_name': 'refrig_kiat.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Kiat_Ananda_Group_Mitsubishi_Fuso_Canter_%28GIICOMVEC_2026%29.jpg/1920px-Kiat_Ananda_Group_Mitsubishi_Fuso_Canter_%28GIICOMVEC_2026%29.jpg',
        'width': 800,
        'height': 600,
        'dark_factor': 1.0,
        'quality': 90,
        'description': 'Cold-chain refrigerated box truck with refrigeration unit'
    },
    {
        'filename': 'fuel-tanker.jpg',
        'cache_name': 'tanker_isuzu.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Isuzu_FVM_Fuel_Tanker_Truck_2017.jpg/1920px-Isuzu_FVM_Fuel_Tanker_Truck_2017.jpg',
        'width': 800,
        'height': 600,
        'dark_factor': 1.0,
        'quality': 90,
        'description': 'Heavy fuel and water tanker transport truck'
    },
    {
        'filename': 'sweeper-truck.jpg',
        'cache_name': 'sweeper_china.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Street_sweeper_truck_A48639D_at_Xizhimen_%2820200820133725%29.jpg/1920px-Street_sweeper_truck_A48639D_at_Xizhimen_%2820200820133725%29.jpg',
        'width': 800,
        'height': 600,
        'dark_factor': 1.0,
        'quality': 90,
        'description': 'Municipal road sweeper with circular sweeping disc brooms'
    },
    {
        'filename': 'heavy-dump-truck.jpg',
        'cache_name': 'dump_howo.jpg',
        'url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Howo_Sinotruk_Mining_Dump_Truck_%28Mining_Indonesia_2026%29.jpg/1920px-Howo_Sinotruk_Mining_Dump_Truck_%28Mining_Indonesia_2026%29.jpg',
        'width': 800,
        'height': 600,
        'dark_factor': 1.0,
        'quality': 90,
        'description': 'Heavy-duty 6x4/8x4 engineering dump tipper truck'
    }
]


def ensure_source_image(asset):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, asset['cache_name'])
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 10000:
        return cache_path

    print(f"Downloading source for {asset['filename']} from {asset['url']}...")
    req = urllib.request.Request(asset['url'], headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp, open(cache_path, 'wb') as f:
            f.write(resp.read())
        time.sleep(1)
        return cache_path
    except Exception as e:
        print(f"Error downloading {asset['url']}: {e}", file=sys.stderr)
        if os.path.exists(cache_path):
            return cache_path
        raise


def crop_center_resize(img, target_w, target_h):
    w, h = img.size
    target_ratio = target_w / target_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        box = (offset, 0, offset + new_w, h)
    else:
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        box = (0, offset, w, offset + new_h)

    cropped = img.crop(box)
    return cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)


def process_asset(asset):
    src_path = ensure_source_image(asset)
    dst_path = os.path.join(OUTPUT_DIR, asset['filename'])

    with Image.open(src_path) as im:
        if im.mode != 'RGB':
            im = im.convert('RGB')
        resized = crop_center_resize(im, asset['width'], asset['height'])
        if asset.get('dark_factor', 1.0) < 1.0:
            resized = ImageEnhance.Brightness(resized).enhance(asset['dark_factor'])

        resized.save(dst_path, 'JPEG', quality=asset.get('quality', 90), optimize=True)

    size = os.path.getsize(dst_path)
    print(f"Generated {asset['filename']}: {resized.size}, {size} bytes ({size / 1024:.1f} KB)")
    assert 1000 < size < 500000, f"File size out of bounds for {dst_path}: {size}"


def main():
    print("Processing Special Vehicles Commercial Truck Imagery...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for asset in ASSETS:
        process_asset(asset)
    print("All special vehicles imagery processed and validated successfully!")


if __name__ == '__main__':
    main()
