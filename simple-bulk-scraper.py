#!/usr/bin/env python3
"""
SIMPLE BULK SCRAPER - VIGNANAM.ORG
Reliable content scraper for bulk processing
Targets specific span tags with NotoSans font
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os

def extract_content_from_vignanam(url):
    """Extract content from vignanam.org - target specific span tags"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # TARGET: Look for span tags with NotoSans font and line-height:250%
        target_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans.*line-height:\s*250%'))
        
        if target_spans:
            content_parts = []
            for span in target_spans:
                content_parts.append(str(span))
            return ''.join(content_parts)
        
        # FALLBACK: Look for any span with NotoSans font
        fallback_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
        if fallback_spans:
            content_parts = []
            for span in fallback_spans:
                content_parts.append(str(span))
            return ''.join(content_parts)
        
        return None
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def update_local_file(file_path, new_content):
    """Update local file with scraped content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace content in span tags
        patterns = [
            r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)',
            r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:250%;font-size: 22px;">\s*).*?(\s*</span>\s*</span>\s*</div>)',
            r'<p>Content will be get from source and inserted here\.\.\.</p>'
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.DOTALL):
                if 'stotramtext' in pattern:
                    updated_content = re.sub(pattern, r'\1' + new_content + r'\2', content, flags=re.DOTALL)
                else:
                    updated_content = re.sub(pattern, new_content, content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                return True
        
        return False
        
    except Exception as e:
        print(f"Update error: {str(e)}")
        return False

def process_single_page(file_path):
    """Process a single page"""
    filename = os.path.basename(file_path)
    slug = filename.replace('.php', '').replace('-english', '')
    
    print(f"Processing: {filename}")
    
    # Generate vignanam.org URLs
    urls = [
        f"https://vignanam.org/english/{slug}.html",
        f"https://vignanam.org/english/{slug}",
        f"https://vignanam.org/{slug}.html",
        f"https://vignanam.org/{slug}"
    ]
    
    for url in urls:
        print(f"  → Trying: {url}")
        content = extract_content_from_vignanam(url)
        if content:
            print(f"  ✓ Content found!")
            if update_local_file(file_path, content):
                print(f"  ✅ Updated successfully!")
                return True
            else:
                print(f"  ✗ Update failed!")
                return False
        time.sleep(1)  # Be respectful
    
    print(f"  ✗ No content found")
    return False

def main():
    """Main function"""
    print("SIMPLE BULK SCRAPER - VIGNANAM.ORG")
    print("=" * 50)
    
    # Gayatri Stotras pages
    gayatri_pages = [
        "output_pages/en/sri-gayatri-sahasra-nama-stotram-english.php",
        "output_pages/en/sri-gayatri-hrudayam-english.php",
        "output_pages/en/sarva-devata-gayatri-mantras-english.php",
        "output_pages/en/gayatryashtakam-gayatri-ashtakam-english.php",
        "output_pages/en/gayatri-kavacham-english.php",
        "output_pages/en/gayatri-ashtottara-sata-namavali-english.php",
        "output_pages/en/gayatri-ashtottara-sata-nama-stotram-english.php",
        "output_pages/en/gayatri-mantram-ghanapatham-english.php"
    ]
    
    success_count = 0
    total_pages = len(gayatri_pages)
    
    print(f"Starting with Gayatri Stotras ({total_pages} pages)...")
    print("TARGETING: span tags with NotoSans font")
    print("UPDATING: Content in local pages")
    print()
    
    for i, page_path in enumerate(gayatri_pages, 1):
        print(f"[{i}/{total_pages}] Processing...")
        if os.path.exists(page_path):
            if process_single_page(page_path):
                success_count += 1
                print(f"SUCCESS: {os.path.basename(page_path)}")
            else:
                print(f"FAILED: {os.path.basename(page_path)}")
        else:
            print(f"NOT FOUND: {page_path}")
        print("-" * 30)
    
    print("=" * 50)
    print(f"BULK SCRAPING COMPLETE!")
    print(f"Success: {success_count}/{total_pages} pages")
    print(f"Success rate: {(success_count/total_pages)*100:.1f}%")
    print("=" * 50)
    
    if success_count == total_pages:
        print("All Gayatri pages updated successfully!")
        print("Ready to process other categories...")
    else:
        print("Some pages failed. Check the output above.")

if __name__ == "__main__":
    main()
