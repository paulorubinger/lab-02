#!/usr/bin/env python3
"""
Script para converter arquivos HTML para PDF usando Playwright
Automatiza um navegador headless (Chromium) para gerar PDFs de alta qualidade
"""

import os
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Erro: Playwright não está instalado.")
    print("Execute: pip install playwright")
    sys.exit(1)


def html_to_pdf(html_file, pdf_file):
    """Converte arquivo HTML para PDF usando Playwright"""
    
    if not os.path.exists(html_file):
        print(f"✗ Erro: Arquivo {html_file} não encontrado!")
        return False
    
    try:
        # Converter caminho relativo para URL file://
        html_path = os.path.abspath(html_file).replace("\\", "/")
        html_url = f"file:///{html_path}"
        
        # Usar Playwright para abrir em navegador headless e salvar como PDF
        with sync_playwright() as p:
            print(f"  → Iniciando navegador Chromium...")
            browser = p.chromium.launch()
            page = browser.new_page()
            
            print(f"  → Carregando {html_file}...")
            page.goto(html_url, wait_until="networkidle")
            
            # Aguardar um pouco para garantir que tudo está renderizado
            page.wait_for_load_state("networkidle")
            
            print(f"  → Gerando PDF...")
            page.pdf(
                path=pdf_file,
                format="A4",
                margin={"top": "20mm", "right": "15mm", "bottom": "20mm", "left": "15mm"},
                print_background=True,
                prefer_css_page_size=True,
            )
            
            browser.close()
        
        print(f"✓ Convertido com sucesso: {html_file} → {pdf_file}")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao converter {html_file}: {e}")
        return False


def install_playwright_browsers():
    """Instala os navegadores necessários do Playwright"""
    print("=" * 70)
    print("Instalando navegador Chromium do Playwright (primeira execução)...")
    print("Isso pode levar alguns minutos...")
    print("=" * 70)
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch()
        print("✓ Navegador instalado com sucesso!")
        return True
    except Exception as e:
        print(f"✗ Erro ao instalar navegador: {e}")
        return False


def main():
    """Função principal"""
    
    conversions = [
        ("notes/GUIA_CORRELACOES.html", "notes/GUIA_CORRELACOES.pdf"),
        ("reports/FINAL_REPORT.html", "reports/FINAL_REPORT.pdf"),
    ]
    
    print("=" * 70)
    print("Convertendo HTML para PDF com Playwright...")
    print("=" * 70)
    
    # Verificar se arquivos HTML existem
    missing = [html for html, _ in conversions if not os.path.exists(html)]
    if missing:
        print(f"\n✗ Erro: Arquivos HTML não encontrados:")
        for f in missing:
            print(f"  - {f}")
        print("\nExecute primeiro: python convert_to_html.py")
        sys.exit(1)
    
    success = 0
    for html_file, pdf_file in conversions:
        print(f"\nConvertendo {html_file}...")
        if html_to_pdf(html_file, pdf_file):
            success += 1
    
    print("\n" + "=" * 70)
    print(f"Resultado: {success}/{len(conversions)} arquivo(s) convertido(s) com sucesso!")
    if success == len(conversions):
        print("\nArquivos PDF prontos:")
        for _, pdf_file in conversions:
            print(f"  ✓ {pdf_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
