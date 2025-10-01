#!/usr/bin/env python3
"""
FAST DURGA SCRAPER - VIGNANAM.ORG
Quick and accurate content scraper
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os

def extract_content_from_vignanam(url):
    """Extract content from vignanam.org"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=8)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            target_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            
            if target_spans:
                content_parts = [str(span) for span in target_spans]
                return ''.join(content_parts)
        return None
    except:
        return None

def update_local_file(file_path, new_content):
    """Update local file with scraped content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
        
        if re.search(pattern, content, re.DOTALL):
            updated_content = re.sub(pattern, r'\1' + new_content + r'\2', content, flags=re.DOTALL)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
    except:
        return False

def process_single_page(file_path):
    """Process a single page"""
    filename = os.path.basename(file_path)
    slug = filename.replace('.php', '').replace('-english', '')
    
    print(f"Processing: {filename}")
    
    # Try main URL first
    url = f"https://vignanam.org/english/{slug}.html"
    content = extract_content_from_vignanam(url)
    
    if content and update_local_file(file_path, content):
        print(f"SUCCESS: {filename}")
        return True
    
    print(f"FAILED: {filename}")
    return False

def main():
    """Main function - Process first 10 Durga pages"""
    print("FAST DURGA SCRAPER - VIGNANAM.ORG")
    print("=" * 50)
    
    # First 10 Durga pages for quick processing
    durga_pages = [
        "output_pages/en/sree-durga-sahasra-nama-stotram-english.php",
        "output_pages/en/sri-durga-ashtottara-sata-nama-stotram-english.php",
        "output_pages/en/sri-durga-chalisa-english.php",
        "output_pages/en/durga-kavacham-english.php",
        "output_pages/en/durga-ashtottara-sata-namavali-english.php",
        "output_pages/en/durga-suktam-english.php",
        "output_pages/en/durga-pancha-ratnam-english.php",
        "output_pages/en/nava-durga-stotram-english.php",
        "output_pages/en/arjuna-kruta-durga-stotram-english.php",
        "output_pages/en/durga-apaduddharaka-stotram-english.php"
    ]
    
    success_count = 0
    total_pages = len(durga_pages)
    
    print(f"Processing {total_pages} Durga pages...")
    print()
    
    for i, page_path in enumerate(durga_pages, 1):
        print(f"[{i}/{total_pages}] ", end="")
        if os.path.exists(page_path):
            if process_single_page(page_path):
                success_count += 1
        else:
            print(f"NOT FOUND: {page_path}")
        time.sleep(0.5)  # Quick delay
    
    print("=" * 50)
    print(f"COMPLETE! Success: {success_count}/{total_pages} pages")
    print(f"Success rate: {(success_count/total_pages)*100:.1f}%")
    print("=" * 50)

if __name__ == "__main__":
    main()
