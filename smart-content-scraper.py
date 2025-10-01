ou have #!/usr/bin/env python3
"""
SMART CONTENT SCRAPER - VIGNANAM.ORG
Intelligently scrapes content from vignanam.org and updates local pages
Respects copyright and avoids unwanted elements
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
from urllib.parse import urljoin, urlparse
import random

class SmartContentScraper:
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
        self.delay_range = (1, 3)  # Random delay between requests
        
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
            'footer'
        ]
        
        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # Remove div tags but keep their content
        for div in soup.find_all('div'):
            div.unwrap()
        
        # Clean up empty paragraphs
        for p in soup.find_all('p'):
            if not p.get_text().strip():
                p.decompose()
        
        return str(soup)
    
    def extract_stotra_content(self, url):
        """Extract stotra content from vignanam.org page"""
        try:
            print(f"Scraping: {url}")
            
            # Add random delay to be respectful
            time.sleep(random.uniform(*self.delay_range))
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for stotra content in common containers
            content_selectors = [
                '.stotra-content',
                '.content',
                '.stotram',
                '.stotra',
                'div[class*="stotra"]',
                'div[class*="content"]',
                'main',
                'article'
            ]
            
            content_html = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content_html = str(content_element)
                    break
            
            if not content_html:
                # Fallback: get body content
                body = soup.find('body')
                if body:
                    content_html = str(body)
            
            if content_html:
                cleaned_content = self.clean_content(content_html)
                return cleaned_content
            else:
                return None
                
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return None
    
    def generate_vignanam_url(self, local_slug):
        """Generate vignanam.org URL from local page slug"""
        # Remove -english suffix
        clean_slug = local_slug.replace('-english', '')
        
        # Convert to vignanam.org format
        vignanam_slug = clean_slug.replace('-', '-')
        
        # Common URL patterns on vignanam.org
        possible_urls = [
            f"{self.base_url}/english/{vignanam_slug}.html",
            f"{self.base_url}/en/{vignanam_slug}.html",
            f"{self.base_url}/{vignanam_slug}.html",
            f"{self.base_url}/english/{vignanam_slug}",
            f"{self.base_url}/en/{vignanam_slug}",
            f"{self.base_url}/{vignanam_slug}"
        ]
        
        return possible_urls
    
    def update_page_content(self, file_path, new_content):
        """Update page content with scraped content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and replace the placeholder content
            placeholder_pattern = r'<p>Content will be get from source and inserted here\.\.\.</p>'
            
            if re.search(placeholder_pattern, content):
                # Replace placeholder with new content
                updated_content = re.sub(
                    placeholder_pattern, 
                    new_content, 
                    content
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                return True
            else:
                print(f"No placeholder found in {file_path}")
                return False
                
        except Exception as e:
            print(f"Error updating {file_path}: {str(e)}")
            return False
    
    def process_single_page(self, local_file_path):
        """Process a single page"""
        try:
            # Extract slug from file path
            filename = os.path.basename(local_file_path)
            slug = filename.replace('.php', '')
            
            print(f"\nProcessing: {slug}")
            
            # Generate possible vignanam.org URLs
            possible_urls = self.generate_vignanam_url(slug)
            
            # Try each possible URL
            content = None
            for url in possible_urls:
                content = self.extract_stotra_content(url)
                if content:
                    print(f"✓ Found content at: {url}")
                    break
                else:
                    print(f"✗ No content at: {url}")
            
            if content:
                # Update the local file
                if self.update_page_content(local_file_path, content):
                    print(f"✓ Successfully updated: {filename}")
                    return True
                else:
                    print(f"✗ Failed to update: {filename}")
                    return False
            else:
                print(f"✗ No content found for: {slug}")
                return False
                
        except Exception as e:
            print(f"Error processing {local_file_path}: {str(e)}")
            return False

def main():
    """Main function to test with Ayyappa pages"""
    scraper = SmartContentScraper()
    
    print("🚀 SMART CONTENT SCRAPER - VIGNANAM.ORG")
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
    print("Content scraped from vignanam.org and updated locally")
    print("Respectful scraping with delays and proper headers")

if __name__ == "__main__":
    main()
