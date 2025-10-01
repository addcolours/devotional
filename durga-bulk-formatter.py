#!/usr/bin/env python3
"""
DURGA BULK FORMATTER - Updates all Durga pages with proper formatting
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random

# Base URL for vignanam.org English stotras
BASE_VIGNANAM_URL = "https://vignanam.org/english/"
OUTPUT_DIR = "output_pages/en/"

def get_slug_from_filepath(file_path):
    """Extracts the slug from a given file path."""
    filename = os.path.basename(file_path)
    # Remove '-english.php' and replace with '-english.html' for vignanam URL
    slug = filename.replace('-english.php', '')
    return slug

def extract_content_from_vignanam(url, retry_count=0):
    """Extract content from vignanam.org with retry logic."""
    try:
        print(f"    -> Trying: {url} (attempt {retry_count + 1})")
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
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
            
            # Target the main content area
            content_selectors = [
                'div.content_text > span[style*="font-family:NotoSans"]',
                'div.content_text > p > span[style*="font-family:NotoSans"]',
                'div.content_text > p',
                'div.content_text'
            ]
            
            content_parts = []
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        # Extract text and preserve line breaks from <br> tags
                        for br in element.find_all('br'):
                            br.replace_with('\n')
                        content_parts.append(element.get_text(separator='\n', strip=True))
                    break
            
            full_content = '\n'.join(content_parts)
            
            # Clean up unwanted elements
            for unwanted_selector in ['ul.aqtree3clickable', 'p.relatedCategories']:
                for div in soup.select(unwanted_selector):
                    div.decompose()
            
            # Further refine content
            lines = full_content.split('\n')
            cleaned_lines = []
            for line in lines:
                stripped_line = line.strip()
                if stripped_line and not re.match(r'^(Vaidika Vignanam|Collection of Spiritual and Devotional Literature|Meaning, Multimedia|View this in:|This document is in romanized sanskrit|Open In Vignanam Mobile App)', stripped_line):
                    cleaned_lines.append(line)
            
            final_content = '\n'.join(cleaned_lines).strip()
            
            if len(final_content) > 100:
                print(f"✅ Found content. Length: {len(final_content)} characters")
                return final_content
            else:
                print(f"    -> No substantial content found")
                return None
        elif response.status_code == 403:
            print(f"    -> 403 Forbidden - Rate limited")
            if retry_count < 2:
                wait_time = 30 + (retry_count * 20)
                print(f"    -> Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                return extract_content_from_vignanam(url, retry_count + 1)
            else:
                return "RATE_LIMITED"
        else:
            print(f"    -> HTTP Error: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"    -> Network Error: {e}")
        return None
    except Exception as e:
        print(f"    -> Error during scraping: {e}")
        return None

def format_content_for_php(raw_content):
    """Formats the raw scraped content into proper HTML paragraphs for PHP files."""
    lines = raw_content.split('\n')
    formatted_paragraphs = []
    
    current_paragraph_lines = []
    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:  # Empty line, signifies a paragraph break
            if current_paragraph_lines:
                formatted_paragraphs.append(f'<p>{"<br/>".join(current_paragraph_lines)}</p>')
                current_paragraph_lines = []
        else:
            # Check for specific markers that should start a new paragraph
            is_new_paragraph_marker = False
            if re.match(r'^(dhyānaṃ|ṛṣiruvācha|rājauvācha|āhuti|om|iti)', stripped_line, re.IGNORECASE):
                is_new_paragraph_marker = True
            if re.match(r'^\s*॥\d+॥', stripped_line):  # Verse numbers like ॥1॥
                is_new_paragraph_marker = True
            
            if is_new_paragraph_marker and current_paragraph_lines:
                formatted_paragraphs.append(f'<p>{"<br/>".join(current_paragraph_lines)}</p>')
                current_paragraph_lines = []
            
            current_paragraph_lines.append(stripped_line)
    
    # Add any remaining content
    if current_paragraph_lines:
        formatted_paragraphs.append(f'<p>{"<br/>".join(current_paragraph_lines)}</p>')
    
    # Add bolding for specific headers
    final_formatted_content = '\n                        '.join(formatted_paragraphs)
    final_formatted_content = re.sub(r'(<p>)(dhyānaṃ)(</p>)', r'\1<strong>\2</strong>\3', final_formatted_content)
    final_formatted_content = re.sub(r'(<p>)(ṛṣiruvācha॥\d+॥)(</p>)', r'\1<strong>\2</strong>\3', final_formatted_content)
    final_formatted_content = re.sub(r'(<p>)(rājauvācha॥\d+॥)(</p>)', r'\1<strong>\2</strong>\3', final_formatted_content)
    final_formatted_content = re.sub(r'(<p>)(āhuti)(</p>)', r'\1<strong>\2</strong>\3', final_formatted_content)

    return final_formatted_content

def update_page_content(file_path, new_content):
    """Updates the content section of a PHP file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Find the content placeholder and replace it
        placeholder_pattern = re.compile(
            r'(<span style="font-family:NotoSans; line-height:150%;">\s*<p>Content will be get from source and inserted here\.\.\.</p>\s*</span>)',
            re.DOTALL
        )
        
        match = placeholder_pattern.search(file_content)
        
        if match:
            # Replace the placeholder with new content
            updated_file_content = file_content.replace(match.group(1), new_content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_file_content)
            print(f"    -> ✅ Updated content in {file_path}")
            return True
        else:
            print(f"    -> ❌ Placeholder not found in {file_path}")
            return False
    except Exception as e:
        print(f"    -> ❌ Error updating file {file_path}: {e}")
        return False

def process_single_page(file_path):
    """Process a single page - scrape content and update it."""
    slug = get_slug_from_filepath(file_path)
    vignanam_url = f"{BASE_VIGNANAM_URL}{slug}.html"
    
    scraped_content = extract_content_from_vignanam(vignanam_url)
    
    if scraped_content and scraped_content != "RATE_LIMITED":
        formatted_content = format_content_for_php(scraped_content)
        return update_page_content(file_path, formatted_content)
    elif scraped_content == "RATE_LIMITED":
        print(f"❌ Failed to scrape {vignanam_url} due to rate limiting")
        return False
    else:
        print(f"❌ Failed to scrape content for {vignanam_url}")
        return False

def main():
    """Main function to process all Durga pages."""
    print("=== DURGA BULK FORMATTER ===")
    print("Updating all Durga pages with proper formatting...")
    
    # List of all Durga pages that need content updates
    durga_pages = [
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
    
    print(f"Total Durga pages to process: {len(durga_pages)}")
    
    success_count = 0
    failed_count = 0
    
    for i, page in enumerate(durga_pages, 1):
        print(f"\n[{i}/{len(durga_pages)}] Processing: {page}")
        
        if process_single_page(page):
            success_count += 1
        else:
            failed_count += 1
        
        # Wait between requests to avoid rate limiting
        if i < len(durga_pages):
            wait_time = random.randint(3, 7)
            print(f"    -> Waiting {wait_time} seconds...")
            time.sleep(wait_time)
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"✅ Successfully updated: {success_count} pages")
    print(f"❌ Failed: {failed_count} pages")
    print(f"📊 Total processed: {success_count + failed_count} pages")

if __name__ == "__main__":
    main()
