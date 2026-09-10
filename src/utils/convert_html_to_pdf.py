#!/usr/bin/env python3
"""
Script to convert HTML files to PDF using Playwright
Automates a headless browser (Chromium) to generate high-quality PDFs
"""

import os
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright is not installed.")
    print("Execute: pip install playwright")
    sys.exit(1)


def html_to_pdf(html_file, pdf_file):
    """Converts HTML file to PDF using Playwright"""
    
    if not os.path.exists(html_file):
        print(f"✗ Error: File {html_file} not found!")
        return False
    
    try:
        # Convert relative path to file:// URL
        html_path = os.path.abspath(html_file).replace("\\", "/")
        html_url = f"file:///{html_path}"
        
        # Use Playwright to open in headless browser and save as PDF
        with sync_playwright() as p:
            print(f"  → Starting Chromium browser...")
            browser = p.chromium.launch()
            page = browser.new_page()
            
            print(f"  → Loading {html_file}...")
            page.goto(html_url, wait_until="networkidle")
            
            # Wait a bit to ensure everything is rendered
            page.wait_for_load_state("networkidle")
            
            print(f"  → Generating PDF...")
            page.pdf(
                path=pdf_file,
                format="A4",
                margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
                print_background=True,
                prefer_css_page_size=True,
            )
            
            browser.close()
        
        print(f"✓ Successfully converted: {html_file} → {pdf_file}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {html_file}: {e}")
        return False


def install_playwright_browsers():
    """Installs necessary Playwright browsers"""
    print("=" * 70)
    print("Installing Chromium browser from Playwright (first run)...")
    print("This may take a few minutes...")
    print("=" * 70)
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch()
        print("✓ Browser installed successfully!")
        return True
    except Exception as e:
        print(f"✗ Error installing browser: {e}")
        return False


def main():
    """Main function"""
    
    conversions = [
        ("notes/GUIA_CORRELACOES.html", "notes/GUIA_CORRELACOES.pdf"),
        ("reports/FINAL_REPORT.html", "reports/FINAL_REPORT.pdf"),
    ]
    
    print("=" * 70)
    print("Converting HTML to PDF with Playwright...")
    print("=" * 70)
    
    # Check if HTML files exist
    missing = [html for html, _ in conversions if not os.path.exists(html)]
    if missing:
        print(f"\n✗ Error: HTML files not found:")
        for f in missing:
            print(f"  - {f}")
        print("\nExecute first: python convert_to_html.py")
        sys.exit(1)
    
    success = 0
    for html_file, pdf_file in conversions:
        print(f"\nConverting {html_file}...")
        if html_to_pdf(html_file, pdf_file):
            success += 1
    
    print("\n" + "=" * 70)
    print(f"Result: {success}/{len(conversions)} file(s) successfully converted!")
    if success == len(conversions):
        print("\nPDF files ready:")
        for _, pdf_file in conversions:
            print(f"  ✓ {pdf_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
