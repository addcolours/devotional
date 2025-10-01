#!/usr/bin/env python3
"""
ROBUST DURGA SCRAPER - Handle rate limiting and continue processing
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random

def check_page_needs_update(file_path):
    """Check if a page has placeholder content that needs updating"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for placeholder text
        placeholder = '<p>Content will be get from source and inserted here...</p>'
        return placeholder in content
    except:
        return False

def extract_content_from_vignanam(url, retry_count=0):
    """Extract content from vignanam.org with retry logic"""
    try:
        print(f"    -> Trying: {url} (attempt {retry_count + 1})")
        
        # Randomize user agents to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=20)
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
            if retry_count < 2:  # Retry up to 2 times
                wait_time = 30 + (retry_count * 20)  # Increasing wait time
                print(f"    -> Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                return extract_content_from_vignanam(url, retry_count + 1)
            else:
                return "RATE_LIMITED"
        else:
            print(f"    -> HTTP Error: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"    -> Error: {str(e)}")
        if retry_count < 1:
            print(f"    -> Retrying in 10 seconds...")
            time.sleep(10)
            return extract_content_from_vignanam(url, retry_count + 1)
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
    
    # First check if page needs updating
    if not check_page_needs_update(file_path):
        print(f"    -> ⏭️  Page already has content, skipping...")
        return "SKIPPED"
    
    # Extract slug from file path
    slug = os.path.basename(file_path).replace('-english.php', '')
    print(f"    -> Slug: {slug}")
    
    # Generate vignanam.org URL
    vignanam_url = f"https://vignanam.org/veda/{slug}-english.html"
    
    # Get content from vignanam.org
    content = extract_content_from_vignanam(vignanam_url)
    
    if content == "RATE_LIMITED":
        print(f"    -> ⏸️  Rate limited after retries, skipping for now...")
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
    print("=== ROBUST DURGA SCRAPER ===")
    print("Processing pages that need content updates with retry logic...")
    
    # Pages that need content updates (27 pages from status checker)
    pages_needing_content = [
        "output_pages/en/sree-durga-sahasra-nama-stotram-english.php",
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
    skipped_count = 0
    failed_count = 0
    rate_limited_count = 0
    
    for i, page in enumerate(pages_needing_content, 1):
        print(f"\n[{i}/{len(pages_needing_content)}] Processing: {os.path.basename(page)}")
        
        if os.path.exists(page):
            result = process_durga_page(page)
            if result == "SUCCESS":
                success_count += 1
            elif result == "SKIPPED":
                skipped_count += 1
            elif result == "RATE_LIMITED":
                rate_limited_count += 1
            else:
                failed_count += 1
        else:
            print(f"    -> ❌ File not found: {page}")
            failed_count += 1
        
        # Add random delay between requests to avoid detection
        if i < len(pages_needing_content):
            delay = random.randint(5, 10)
            print(f"    -> Waiting {delay} seconds...")
            time.sleep(delay)
    
    print(f"\n=== FINAL REPORT ===")
    print(f"Total pages processed: {len(pages_needing_content)}")
    print(f"✅ Successfully updated: {success_count}")
    print(f"⏭️  Already had content (skipped): {skipped_count}")
    print(f"⏸️  Rate limited: {rate_limited_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"Success rate: {(success_count/(success_count+failed_count)*100):.1f}%" if (success_count+failed_count) > 0 else "N/A")

if __name__ == "__main__":
    main()
