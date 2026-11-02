#!/usr/bin/env python3
"""
Assemble modular HTML partials in src/partials/ into the root index.html
"""
import glob
import os

def build_index():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    partials_dir = os.path.join(base_dir, 'src', 'partials')
    output_file = os.path.join(base_dir, 'index.html')

    partial_files = sorted(glob.glob(os.path.join(partials_dir, '*.html')))
    if not partial_files:
        raise RuntimeError("No partials found in " + partial_files)

    content = []
    for p in partial_files:
        print(f"Adding partial: {os.path.basename(p)}")
        with open(p, 'r', encoding='utf-8') as f:
            content.append(f.read())

    full_html = '\n'.join(content)
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(full_html)
    print(f"Successfully assembled {output_file} ({len(full_html)} bytes, {len(partial_files)} partials)")

if __name__ == '__main__':
    build_index()
