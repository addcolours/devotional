#!/usr/bin/env python3
"""
WORKING BULK SCRAPER - VIGNANAM.ORG
Reliable content scraper with verbose output
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import sys

def extract_content_from_vignanam(url):
    """Extract content from vignanam.org"""
    try:
        print(f"    -> Trying: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"    -> Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for span tags with NotoSans font
            target_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            print(f"    -> Found {len(target_spans)} NotoSans spans")
            
            if target_spans:
                content_parts = []
                for span in target_spans:
                    content_parts.append(str(span))
                full_content = ''.join(content_parts)
                print(f"    -> Content length: {len(full_content)} characters")
                return full_content
            else:
                print(f"    -> No NotoSans spans found")
                return None
        else:
            print(f"    -> HTTP Error: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"    -> Error: {str(e)}")
        return None

def update_local_file(file_path, new_content):
    """Update local file with scraped content"""
    try:
        print(f"    -> Updating file...")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace content in span tags
        pattern = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
        
        if re.search(pattern, content, re.DOTALL):
            updated_content = re.sub(pattern, r'\1' + new_content + r'\2', content, flags=re.DOTALL)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"    -> File updated successfully!")
            return True
        else:
            print(f"    -> Pattern not found in file")
            return False
        
    except Exception as e:
        print(f"    -> Update error: {str(e)}")
        return False

def process_single_page(file_path):
    """Process a single page"""
    filename = os.path.basename(file_path)
    slug = filename.replace('.php', '').replace('-english', '')
    
    print(f"Processing: {filename}")
    print(f"  Slug: {slug}")
    
    # Generate vignanam.org URLs
    urls = [
        f"https://vignanam.org/english/{slug}.html",
        f"https://vignanam.org/english/{slug}",
        f"https://vignanam.org/{slug}.html",
        f"https://vignanam.org/{slug}"
    ]
    
    for url in urls:
        content = extract_content_from_vignanam(url)
        if content:
            print(f"  -> Content found!")
            if update_local_file(file_path, content):
                print(f"  -> SUCCESS: {filename}")
                return True
            else:
                print(f"  -> FAILED to update: {filename}")
                return False
        time.sleep(1)  # Be respectful
    
    print(f"  -> No content found for: {filename}")
    return False

def main():
    """Main function"""
    print("WORKING BULK SCRAPER - VIGNANAM.ORG")
    print("=" * 50)
    
    # Durga Stotras pages
    durga_pages = [
        "output_pages/en/sree-durga-sahasra-nama-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-ashtottara-sata-namavali-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-adhyaya-2-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-navarna-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-siddha-kunjika-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-adhyaya-13-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-argala-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-rahasya-trayam-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-suktam-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-keelaka-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-pancha-ratnam-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-kshama-prarthana-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-adhyaya-12-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-adhyaya-1-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-6-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-4-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-9-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-7-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-8-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-3-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-2-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-11-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-12-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-10-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-1-english.php",
        "output_pages/en/dakaradi-sree-durga-sahasra-nama-stotram-english.php",
        "output_pages/en/sree-durga-nakshatra-malika-stuti-english.php",
        "output_pages/en/sri-durga-ashtottara-sata-nama-stotram-english.php",
        "output_pages/en/sri-durga-chalisa-english.php",
        "output_pages/en/sri-durga-chandrakala-stuti-english.php",
        "output_pages/en/sri-durga-atharvasheersham-english.php",
        "output_pages/en/sri-durga-sapta-shloki-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-5-english.php",
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-13-english.php",
        "output_pages/en/devi-mahatmyam-durga-dvaatrimsannaamaavali-english.php",
        "output_pages/en/arjuna-kruta-durga-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-kavacham-english.php",
        "output_pages/en/dakaradi-durga-ashtottara-sata-namavali-english.php",
        "output_pages/en/navadurga-stotram-english.php",
        "output_pages/en/nava-durga-stotram-english.php",
        "output_pages/en/durga-suktam-english.php",
        "output_pages/en/durga-pancha-ratnam-english.php",
        "output_pages/en/durga-kavacham-english.php",
        "output_pages/en/durga-ashtottara-sata-namavali-english.php",
        "output_pages/en/durga-apaduddharaka-stotram-english.php"
    ]
    
    success_count = 0
    total_pages = len(durga_pages)
    
    print(f"Starting with Durga Stotras ({total_pages} pages)...")
    print("TARGETING: span tags with NotoSans font")
    print("UPDATING: Content in local pages")
    print()
    
    for i, page_path in enumerate(durga_pages, 1):
        print(f"[{i}/{total_pages}] Processing...")
        if os.path.exists(page_path):
            if process_single_page(page_path):
                success_count += 1
        else:
            print(f"NOT FOUND: {page_path}")
        print("-" * 30)
    
    print("=" * 50)
    print(f"BULK SCRAPING COMPLETE!")
    print(f"Success: {success_count}/{total_pages} pages")
    print(f"Success rate: {(success_count/total_pages)*100:.1f}%")
    print("=" * 50)
    
    if success_count == total_pages:
        print("All Durga pages updated successfully!")
        print("Ready to process other categories...")
    else:
        print("Some pages failed. Check the output above.")

if __name__ == "__main__":
    main()
