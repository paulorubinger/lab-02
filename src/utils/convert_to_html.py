#!/usr/bin/env python3
"""
Script to convert Markdown files (.md) to HTML
The HTML can be converted to PDF via browser (Ctrl+P → Save as PDF)
"""

import os
import markdown
from pathlib import Path

def md_to_html(md_file, html_file):
    """Converts Markdown file to HTML"""
    
    if not os.path.exists(md_file):
        print(f"Error: File {md_file} not found!")
        return False
    
    try:
        # Read Markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown.markdown(
            md_content, 
            extensions=['extra', 'codehilite', 'toc', 'tables']
        )
        
        # Complete HTML
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Path(md_file).stem}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #000;
            background-color: #fff;
            padding: 40px;
            max-width: 900px;
            margin: 0 auto;
        }}
        
        h1 {{
            border-bottom: 3px solid #000;
            padding-bottom: 10px;
            margin: 30px 0 20px 0;
            color: #000;
            font-size: 2.5em;
        }}
        
        h2 {{
            border-left: 4px solid #000;
            padding-left: 15px;
            margin: 25px 0 15px 0;
            color: #000;
            font-size: 1.8em;
        }}
        
        h3 {{
            margin: 20px 0 10px 0;
            color: #000;
            font-size: 1.3em;
        }}
        
        h4, h5, h6 {{
            margin: 15px 0 8px 0;
            color: #333;
        }}
        
        p {{
            margin: 10px 0;
            text-align: justify;
        }}
        
        ul, ol {{
            margin: 10px 0 10px 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        pre {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
        }}
        
        code {{
            background-color: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #ddd;
            padding-left: 20px;
            margin: 10px 0;
            color: #777;
            font-style: italic;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        th {{
            background-color: #003d80;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        
        td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        a {{
            color: #000;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            margin: 15px 0;
        }}
        
        .toc {{
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        @media print {{
            body {{
                padding: 20px;
                max-width: 100%;
            }}
            
            a {{
                color: #000;
                text-decoration: underline;
            }}
            
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
            
            table {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
        
        # Save HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✓ Successfully converted: {md_file} → {html_file}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {md_file}: {e}")
        return False

def main():
    """Main function"""
    
    conversions = [
        ('notes/GUIA_CORRELACOES.md', 'notes/GUIA_CORRELACOES.html'),
        ('reports/FINAL_REPORT.md', 'reports/FINAL_REPORT.html'),
    ]
    
    print("=" * 70)
    print("Converting Markdown to HTML (for later saving as PDF)...")
    print("=" * 70)
    
    success = 0
    for md_file, html_file in conversions:
        if md_to_html(md_file, html_file):
            success += 1
    
    print("=" * 70)
    print(f"Result: {success}/{len(conversions)} file(s) successfully converted!")
    print("\nNext steps:")
    print("1. Open the .html file in your browser (double-click)")
    print("2. Press Ctrl+P (or Cmd+P on Mac)")
    print("3. Click 'Save as PDF'")
    print("=" * 70)

if __name__ == '__main__':
    main()
