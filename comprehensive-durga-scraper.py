#!/usr/bin/env python3
"""
COMPREHENSIVE DURGA SCRAPER - One file to handle all Durga pages
- Extract content from vignanam.org
- Format with proper paragraph structure
- Update pages with correct content
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random

def extract_content_from_vignanam(url, retry_count=0):
    """Extract content from vignanam.org with retry logic"""
    try:
        print(f"    -> Fetching: {url} (attempt {retry_count + 1})")
        
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
            
            # Look for span tags with NotoSans font (main content)
            target_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            print(f"    -> Found {len(target_spans)} NotoSans spans")
            
            if target_spans:
                content_parts = []
                for span in target_spans:
                    # Get HTML content to preserve formatting
                    html_content = str(span)
                    # Clean up the HTML but preserve structure
                    html_content = html_content.replace('<span style="font-family:NotoSans; line-height:250%;font-size: 22px;">', '')
                    html_content = html_content.replace('<span style="font-family:NotoSans">', '')
                    html_content = html_content.replace('</span>', '')
                    content_parts.append(html_content)
                
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
        print(f"    -> Error: {e}")
        return None

def format_sanskrit_content(content):
    """Format Sanskrit content with proper paragraph structure like source website"""
    
    # Split content into lines
    lines = content.split('\n')
    formatted_paragraphs = []
    
    current_paragraph = ""
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
            
        # Check for section headers
        if line in ['dhyānaṃ', 'dhyānam']:
            if current_paragraph:
                formatted_paragraphs.append(f'<p>{current_paragraph}</p>')
                current_paragraph = ""
            formatted_paragraphs.append(f'<p><strong>{line}</strong></p>')
            
        # Check for speaker headers (rājauvācha, ṛṣiruvācha, etc.)
        elif re.match(r'^(rājauvācha|ṛṣiruvācha|devī uvācha|nārada uvācha)', line, re.IGNORECASE):
            if current_paragraph:
                formatted_paragraphs.append(f'<p>{current_paragraph}</p>')
                current_paragraph = ""
            formatted_paragraphs.append(f'<p><strong>{line}</strong></p>')
                
        # Check for verses ending with ॥
        elif line.endswith('॥'):
            if current_paragraph:
                current_paragraph += '<br/>' + line
                formatted_paragraphs.append(f'<p>{current_paragraph}</p>')
                current_paragraph = ""
            else:
                formatted_paragraphs.append(f'<p>{line}</p>')
                
        # Check for title lines (usually contain "nāma" or "adhyāya")
        elif re.search(r'(nāma|adhyāya|ōdhyāya)', line, re.IGNORECASE) and line.endswith('॥'):
            if current_paragraph:
                formatted_paragraphs.append(f'<p>{current_paragraph}</p>')
                current_paragraph = ""
            formatted_paragraphs.append(f'<p><strong>{line}</strong></p>')
            
        # Regular content lines
        else:
            if current_paragraph:
                current_paragraph += '<br/>' + line
            else:
                current_paragraph = line
                
        i += 1
    
    # Add any remaining content
    if current_paragraph:
        formatted_paragraphs.append(f'<p>{current_paragraph}</p>')
    
    return '\n'.join(formatted_paragraphs)

def update_page_content(file_path, content):
    """Update page content with extracted and formatted content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Replace placeholder content
        placeholder = '<p>Content will be get from source and inserted here...</p>'
        if placeholder in file_content:
            # Format the content with proper paragraph structure
            formatted_content = format_sanskrit_content(content)
            
            file_content = file_content.replace(placeholder, formatted_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            return True
        else:
            print(f"    -> ❌ No placeholder found in {file_path}")
            return False
    except Exception as e:
        print(f"    -> ❌ Error updating {file_path}: {e}")
        return False

def get_vignanam_url(page_name):
    """Convert page name to vignanam.org URL"""
    # Remove -english.php suffix
    clean_name = page_name.replace('-english.php', '')
    
    # Convert to vignanam.org format
    vignanam_url = f"https://vignanam.org/english/{clean_name}.html"
    
    return vignanam_url

def process_single_page(page_name):
    """Process a single page - extract content and update"""
    file_path = f"output_pages/en/{page_name}"
    
    print(f"\nProcessing: {page_name}")
    
    if not os.path.exists(file_path):
        print(f"    -> ❌ File not found: {file_path}")
        return False
    
    # Get vignanam.org URL
    vignanam_url = get_vignanam_url(page_name)
    print(f"    -> URL: {vignanam_url}")
    
    # Extract content from vignanam.org
    content = extract_content_from_vignanam(vignanam_url)
    
    if content and content != "RATE_LIMITED":
        # Update the page
        if update_page_content(file_path, content):
            print(f"    -> ✅ Updated successfully")
            return True
        else:
            print(f"    -> ❌ Failed to update file")
            return False
    elif content == "RATE_LIMITED":
        print(f"    -> ⚠️  Rate limited, skipping")
        return False
    else:
        print(f"    -> ❌ Failed to extract content")
        return False

def main():
    """Main function"""
    print("=== COMPREHENSIVE DURGA SCRAPER ===")
    print("One file to handle all Durga pages with proper formatting")
    
    # Test with Chapter 2 first
    test_page = "devi-mahatmyam-durga-saptasati-chapter-2-english.php"
    
    print(f"\n🧪 TESTING with: {test_page}")
    print("If successful, will process all remaining pages...")
    
    success = process_single_page(test_page)
    
    if success:
        print(f"\n✅ SUCCESS! Chapter 2 updated successfully")
        print("Ready to process all remaining pages...")
        
        # List of all Durga pages that need content
        all_durga_pages = [
            "sree-durga-sahasra-nama-stotram-english.php",
            "devi-mahatmyam-durga-sapta-adhyaya-12-english.php",
            "devi-mahatmyam-durga-sapta-adhyaya-1-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-6-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-4-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-9-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-7-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-8-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-3-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-11-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-12-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-10-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-1-english.php",
            "dakaradi-sree-durga-sahasra-nama-stotram-english.php",
            "sree-durga-nakshatra-malika-stuti-english.php",
            "sri-durga-ashtottara-sata-nama-stotram-english.php",
            "sri-durga-chalisa-english.php",
            "sri-durga-chandrakala-stuti-english.php",
            "sri-durga-atharvasheersham-english.php",
            "sri-durga-sapta-shloki-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-5-english.php",
            "devi-mahatmyam-durga-saptasati-chapter-13-english.php",
            "devi-mahatmyam-durga-dvaatrimsannaamaavali-english.php",
            "arjuna-kruta-durga-stotram-english.php",
            "devi-mahatmyam-durga-sapta-kavacham-english.php",
            "dakaradi-durga-ashtottara-sata-namavali-english.php"
        ]
        
        # Remove the test page from the list
        remaining_pages = [p for p in all_durga_pages if p != test_page]
        
        print(f"\n🚀 Processing remaining {len(remaining_pages)} pages...")
        
        success_count = 1  # Chapter 2 already done
        failed_count = 0
        
        for i, page in enumerate(remaining_pages, 1):
            print(f"\n[{i}/{len(remaining_pages)}] Processing: {page}")
            
            if process_single_page(page):
                success_count += 1
            else:
                failed_count += 1
            
            # Wait between requests to avoid rate limiting
            if i < len(remaining_pages):
                wait_time = random.randint(3, 7)
                print(f"    -> Waiting {wait_time} seconds...")
                time.sleep(wait_time)
        
        print(f"\n=== FINAL SUMMARY ===")
        print(f"✅ Successfully updated: {success_count} pages")
        print(f"❌ Failed: {failed_count} pages")
        print(f"📊 Total processed: {success_count + failed_count} pages")
        
    else:
        print(f"\n❌ TEST FAILED! Chapter 2 could not be updated")
        print("Please check the error messages above")

if __name__ == "__main__":
    main()
