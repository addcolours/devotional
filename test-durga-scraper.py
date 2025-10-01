#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
import os

def scrape_and_update(file_path):
    filename = os.path.basename(file_path)
    slug = filename.replace('.php', '').replace('-english', '')
    
    print(f"Testing: {filename}")
    
    try:
        url = f"https://vignanam.org/english/{slug}.html"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            
            if spans:
                content = ''.join([str(span) for span in spans])
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                pattern = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
                
                if re.search(pattern, file_content, re.DOTALL):
                    updated = re.sub(pattern, r'\1' + content + r'\2', file_content, flags=re.DOTALL)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated)
                    print(f"SUCCESS: {filename}")
                    return True
        
        print(f"FAILED: {filename}")
        return False
        
    except Exception as e:
        print(f"ERROR: {filename} - {str(e)}")
        return False

def main():
    print("TEST DURGA SCRAPER")
    print("=" * 30)
    
    test_pages = [
        "output_pages/en/sri-durga-chalisa-english.php",
        "output_pages/en/durga-kavacham-english.php",
        "output_pages/en/durga-suktam-english.php"
    ]
    
    success = 0
    for page in test_pages:
        if os.path.exists(page):
            if scrape_and_update(page):
                success += 1
    
    print("=" * 30)
    print(f"Result: {success}/{len(test_pages)} pages updated")

if __name__ == "__main__":
    main()
