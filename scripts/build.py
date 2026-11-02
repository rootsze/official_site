#!/usr/bin/env python3
"""
Assemble modular HTML partials in:
- src/partials/ -> index.html
- src/partials-news/ -> news.html
- src/partials-products/ -> products/*.html
"""
import glob
import os

def build_page(partials_dir_name, output_filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    partials_dir = os.path.join(base_dir, 'src', partials_dir_name)
    output_file = os.path.join(base_dir, output_filename)

    partial_files = sorted(glob.glob(os.path.join(partials_dir, '*.html')))
    if not partial_files:
        raise RuntimeError("No partials found in " + partials_dir)

    content = []
    for p in partial_files:
        print(f"[{output_filename}] Adding partial: {os.path.basename(p)}")
        with open(p, 'r', encoding='utf-8') as f:
            content.append(f.read())

    full_html = '\n'.join(content)
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(full_html)
    print(f"Successfully assembled {output_file} ({len(full_html)} bytes, {len(partial_files)} partials)")

def build_product_pages():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    partials_dir = os.path.join(base_dir, 'src', 'partials-products')
    out_dir = os.path.join(base_dir, 'products')
    os.makedirs(out_dir, exist_ok=True)

    head_path = os.path.join(partials_dir, '01-head-nav.html')
    foot_path = os.path.join(partials_dir, '09-footer.html')
    
    with open(head_path, 'r', encoding='utf-8') as f:
        head_template = f.read()
    with open(foot_path, 'r', encoding='utf-8') as f:
        foot = f.read()

    pages = [
        (
            'electrical.html',
            'electrical-systems.html',
            'Industrial Electrical Systems — Rootze Global | 襄阳如志进出口有限公司',
            'Factory-backed high & low-voltage soft starters, high-voltage variable frequency drives (VFD), reactive power compensation cabinets, and KYN28 switchgear from Renle and Leishen Electric.'
        ),
        (
            'railway.html',
            'railway-equipment.html',
            'Railway Track Equipment — Rootze Global | 襄阳如志进出口有限公司',
            'Precision digital railway track gauges, superelevation rulers, switch rail gauges, internal combustion tampers, abrasive cutters, and hydraulic adjusters from Haite and Linkage.'
        ),
        (
            'brakelines.html',
            'brake-pad-lines.html',
            'Turnkey Brake Pad Lines — Rootze Global | 襄阳如志进出口有限公司',
            'Complete turnkey automotive brake pad manufacturing lines, mixing, 200T-500T hot pressing, curing ovens, outer arc grinding and drilling machinery with OE friction formulas.'
        ),
        (
            'vehicles.html',
            'special-vehicles.html',
            'Special Purpose Vehicles — Rootze Global | 襄阳如志进出口有限公司',
            'Commercial utility and specialized vehicles: cold-chain refrigerated trucks, fluid tankers, municipal sweepers, and heavy engineering dump tippers on Dongfeng chassis.'
        ),
    ]

    for body_file, out_name, title, desc in pages:
        body_path = os.path.join(partials_dir, body_file)
        body = ''
        if os.path.exists(body_path):
            with open(body_path, 'r', encoding='utf-8') as f:
                body = f.read()
        
        head = head_template.replace('{{PAGE_TITLE}}', title).replace('{{PAGE_DESC}}', desc)
        full_content = head + '\n' + body + '\n' + foot
        out_file = os.path.join(out_dir, out_name)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(full_content)
        print(f"[products/{out_name}] Assembled {out_name} ({len(full_content)} bytes)")

def main():
    build_page('partials', 'index.html')
    build_page('partials-news', 'news.html')
    build_product_pages()

if __name__ == '__main__':
    main()
