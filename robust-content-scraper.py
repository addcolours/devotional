#!/usr/bin/env python3
"""
ROBUST CONTENT SCRAPER - VIGNANAM.ORG
Handles various content states and replaces content intelligently
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random

class RobustContentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.base_url = "https://vignanam.org"
        
    def clean_content(self, content_html):
        """Clean scraped content and remove unwanted elements"""
        soup = BeautifulSoup(content_html, 'html.parser')
        
        # Remove unwanted elements
        unwanted_selectors = [
            'ul.aqtree3clickable',
            'p.relatedCategories',
            '.related-categories',
            '.navigation',
            '.menu',
            '.sidebar',
            '.ads',
            '.advertisement',
            'script',
            'style',
            'nav',
            'header',
            'footer',
            '.logo',
            '.header',
            '.breadcrumb',
            '.breadcrumbs',
            'img[src*="logo"]',
            'img[src*="header"]',
            'a[href*="index"]',
            'a[href*="home"]'
        ]
        
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Remove div tags but keep their content
        for div in soup.find_all('div'):
            div.unwrap()
        
        # Clean up empty paragraphs and elements
        for element in soup.find_all(['p', 'span', 'div']):
            if not element.get_text().strip():
                element.decompose()
        
        # Remove links that are not content
        for link in soup.find_all('a'):
            if link.get('href') and ('index' in link.get('href') or 'home' in link.get('href')):
                link.unwrap()
        
        return str(soup)
    
    def extract_stotra_content(self, url):
        """Extract stotra content from vignanam.org page"""
        try:
            print(f"  → Trying: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the main content area
            content_selectors = [
                'div[class*="content"]',
                'div[class*="stotra"]',
                'div[class*="text"]',
                'main',
                'article',
                'body'
            ]
            
            content_html = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    # Check if it has meaningful content
                    text_content = content_element.get_text().strip()
                    if len(text_content) > 100:  # Has substantial content
                        content_html = str(content_element)
                        print(f"  ✓ Found content with selector: {selector}")
                        break
            
            if content_html:
                cleaned_content = self.clean_content(content_html)
                # Check if cleaned content has meaningful text
                soup_check = BeautifulSoup(cleaned_content, 'html.parser')
                text_check = soup_check.get_text().strip()
                if len(text_check) > 50:  # Has meaningful content
                    return cleaned_content
            
            return None
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return None
    
    def generate_vignanam_urls(self, local_slug):
        """Generate vignanam.org URLs from local page slug"""
        # Remove -english suffix
        clean_slug = local_slug.replace('-english', '')
        
        # Vignanam.org URL patterns based on their structure
        possible_urls = [
            f"{self.base_url}/english/{clean_slug}.html",
            f"{self.base_url}/english/{clean_slug}",
            f"{self.base_url}/{clean_slug}.html",
            f"{self.base_url}/{clean_slug}",
            f"{self.base_url}/en/{clean_slug}.html",
            f"{self.base_url}/en/{clean_slug}"
        ]
        
        return possible_urls
    
    def update_page_content(self, file_path, new_content):
        """Update page content with scraped content - robust replacement"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Multiple patterns to match different content states
            replacement_patterns = [
                # Original placeholder
                r'<p>Content will be get from source and inserted here\.\.\.</p>',
                # Alternative placeholder
                r'<p>Content will be scraped from vignanam\.org and inserted here\.\.\.</p>',
                # Content between stotramtext div
                r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)',
                # Any content in the stotramtext div
                r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
            ]
            
            updated = False
            for pattern in replacement_patterns:
                if re.search(pattern, content, re.DOTALL):
                    if 'stotramtext' in pattern:
                        # For stotramtext div, replace the content inside
                        updated_content = re.sub(
                            pattern, 
                            r'\1' + new_content + r'\2', 
                            content, 
                            flags=re.DOTALL
                        )
                    else:
                        # For simple placeholder, replace directly
                        updated_content = re.sub(pattern, new_content, content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    updated = True
                    break
            
            return updated
                
        except Exception as e:
            print(f"  ✗ Update error: {str(e)}")
            return False
    
    def process_single_page(self, local_file_path):
        """Process a single page"""
        try:
            # Extract slug from file path
            filename = os.path.basename(local_file_path)
            slug = filename.replace('.php', '')
            
            print(f"\n📄 Processing: {filename}")
            
            # Generate possible vignanam.org URLs
            possible_urls = self.generate_vignanam_urls(slug)
            
            # Try each possible URL
            content = None
            for url in possible_urls:
                content = self.extract_stotra_content(url)
                if content:
                    print(f"  ✓ Content found!")
                    break
                time.sleep(1)  # Be respectful
            
            if content:
                # Update the local file
                if self.update_page_content(local_file_path, content):
                    print(f"  ✅ Successfully updated: {filename}")
                    return True
                else:
                    print(f"  ✗ Failed to update: {filename}")
                    return False
            else:
                print(f"  ✗ No content found for: {slug}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error processing {local_file_path}: {str(e)}")
            return False

def main():
    """Main function to test with Ayyappa pages"""
    scraper = RobustContentScraper()
    
    print("🚀 ROBUST CONTENT SCRAPER - VIGNANAM.ORG")
    print("=" * 60)
    print("Testing with Ayyappa Stotras pages...")
    print("=" * 60)
    
    # Test with Ayyappa pages
    ayyappa_pages = [
        "output_pages/en/ayyappa-ashtottara-sata-nama-stotram-english.php",
        "output_pages/en/ayyappa-pancha-ratnam-english.php",
        "output_pages/en/maha-shasta-anugraha-kavacham-english.php",
        "output_pages/en/sri-ayyappa-ashtottara-sata-namavali-english.php"
    ]
    
    success_count = 0
    total_pages = len(ayyappa_pages)
    
    for page_path in ayyappa_pages:
        if os.path.exists(page_path):
            if scraper.process_single_page(page_path):
                success_count += 1
        else:
            print(f"File not found: {page_path}")
    
    print("\n" + "=" * 60)
    print(f"🎉 SCRAPING COMPLETE!")
    print(f"✅ Successfully updated: {success_count}/{total_pages} pages")
    print("=" * 60)

if __name__ == "__main__":
    main()
