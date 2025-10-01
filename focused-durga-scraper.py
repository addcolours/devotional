#!/usr/bin/env python3
"""
FOCUSED DURGA SCRAPER - Only process pages that need content updates
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os

def extract_content_from_vignanam(url):
    """Extract content from vignanam.org with better error handling"""
    try:
        print(f"    -> Trying: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
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
        elif response.status_code == 403:
            print(f"    -> 403 Forbidden - Rate limited or blocked")
            return "RATE_LIMITED"
        else:
            print(f"    -> HTTP Error: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"    -> Error: {str(e)}")
        return None

def update_local_file(file_path, new_content):
    """Update local PHP file with new content"""
    try:
        print(f"    -> Updating: {file_path}")
        
        # Read current file
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Replace placeholder content
        placeholder = '<p>Content will be get from source and inserted here...</p>'
        
        if placeholder in file_content:
            # Replace with actual content
            updated_content = file_content.replace(placeholder, new_content)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"    -> ✅ Successfully updated {file_path}")
            return True
        else:
            print(f"    -> ❌ Placeholder not found in {file_path}")
            return False
            
    except Exception as e:
        print(f"    -> ❌ Error updating file: {str(e)}")
        return False

def process_durga_page(file_path):
    """Process a single Durga page"""
    print(f"\nProcessing: {file_path}")
    
    # Extract slug from file path
    slug = os.path.basename(file_path).replace('-english.php', '')
    print(f"    -> Slug: {slug}")
    
    # Generate vignanam.org URL
    vignanam_url = f"https://vignanam.org/veda/{slug}-english.html"
    
    # Get content from vignanam.org
    content = extract_content_from_vignanam(vignanam_url)
    
    if content == "RATE_LIMITED":
        print(f"    -> ⏸️  Rate limited, waiting 15 seconds...")
        time.sleep(15)
        return "RATE_LIMITED"
    elif content:
        # Update local file
        success = update_local_file(file_path, content)
        if success:
            print(f"    -> ✅ Successfully updated {file_path}")
            return "SUCCESS"
        else:
            print(f"    -> ❌ Failed to update {file_path}")
            return "FAILED"
    else:
        print(f"    -> ❌ Failed to get content for {file_path}")
        return "FAILED"

def main():
    """Main function to process Durga pages that need content updates"""
    print("=== FOCUSED DURGA SCRAPER ===")
    print("Script started successfully!")
    print("Processing pages that need content updates...")
    
    # Pages that need content updates (from status report)
    pages_needing_content = [
        "output_pages/en/sree-durga-sahasra-nama-stotram-english.php",
        "output_pages/en/devi-mahatmyam-durga-sapta-ashtottara-sata-namavali-english.php",
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
        "output_pages/en/dakaradi-durga-ashtottara-sata-namavali-english.php"
    ]
    
    print(f"Total pages to process: {len(pages_needing_content)}")
    
    success_count = 0
    failed_count = 0
    rate_limited_count = 0
    
    for i, page in enumerate(pages_needing_content, 1):
        print(f"\n[{i}/{len(pages_needing_content)}] Processing: {os.path.basename(page)}")
        
        if os.path.exists(page):
            result = process_durga_page(page)
            if result == "SUCCESS":
                success_count += 1
            elif result == "RATE_LIMITED":
                rate_limited_count += 1
            else:
                failed_count += 1
        else:
            print(f"    -> ❌ File not found: {page}")
            failed_count += 1
        
        # Add delay between requests
        if i < len(pages_needing_content):
            print("    -> Waiting 5 seconds...")
            time.sleep(5)
    
    print(f"\n=== FINAL REPORT ===")
    print(f"Total pages processed: {len(pages_needing_content)}")
    print(f"✅ Successfully updated: {success_count}")
    print(f"⏸️  Rate limited: {rate_limited_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"Success rate: {(success_count/(success_count+failed_count)*100):.1f}%" if (success_count+failed_count) > 0 else "N/A")

if __name__ == "__main__":
    main()
