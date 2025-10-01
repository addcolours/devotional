#!/usr/bin/env python3
"""
DIRECT DURGA UPDATER - Manual content replacement
"""

import requests
from bs4 import BeautifulSoup
import re
import os

def get_content_from_vignanam(slug):
    """Get content from vignanam.org"""
    try:
        url = f"https://vignanam.org/english/{slug}.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            
            if spans:
                content = ''.join([str(span) for span in spans])
                return content
        return None
    except:
        return None

def update_file_content(file_path, new_content):
    """Update file with new content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace content in the stotramtext div
        pattern = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
        
        if re.search(pattern, content, re.DOTALL):
            updated_content = re.sub(pattern, r'\1' + new_content + r'\2', content, flags=re.DOTALL)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        return False
    except:
        return False

def main():
    print("DIRECT DURGA UPDATER")
    print("=" * 40)
    
    # Key Durga pages to update
    pages_to_update = [
        ("sri-durga-chalisa", "output_pages/en/sri-durga-chalisa-english.php"),
        ("durga-kavacham", "output_pages/en/durga-kavacham-english.php"),
        ("durga-suktam", "output_pages/en/durga-suktam-english.php"),
        ("sri-durga-ashtottara-sata-nama-stotram", "output_pages/en/sri-durga-ashtottara-sata-nama-stotram-english.php"),
        ("durga-ashtottara-sata-namavali", "output_pages/en/durga-ashtottara-sata-namavali-english.php")
    ]
    
    success_count = 0
    
    for slug, file_path in pages_to_update:
        print(f"Processing: {slug}")
        
        if os.path.exists(file_path):
            # Get content from vignanam.org
            content = get_content_from_vignanam(slug)
            
            if content:
                # Update local file
                if update_file_content(file_path, content):
                    print(f"SUCCESS: {slug}")
                    success_count += 1
                else:
                    print(f"FAILED to update: {slug}")
            else:
                print(f"NO CONTENT found for: {slug}")
        else:
            print(f"FILE NOT FOUND: {file_path}")
        
        print("-" * 30)
    
    print("=" * 40)
    print(f"COMPLETED: {success_count}/{len(pages_to_update)} pages updated")
    print("=" * 40)

if __name__ == "__main__":
    main()
