#!/usr/bin/env python3
"""
Assemble modular HTML partials in src/partials/ and src/partials-news/
into index.html and news.html
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

def main():
    build_page('partials', 'index.html')
    build_page('partials-news', 'news.html')

if __name__ == '__main__':
    main()
