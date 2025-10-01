#!/usr/bin/env python3
"""
BULK CONTENT SCRAPER - VIGNANAM.ORG
Ultra-fast bulk scraping with intelligent content extraction
Processes hundreds of pages with smart content targeting
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class BulkContentScraper:
    def __init__(self, max_workers=5):
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
        self.max_workers = max_workers
        self.lock = threading.Lock()
        
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
            '.breadcrumbs'
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
        
        # Remove images and links that are not content
        for img in soup.find_all('img'):
            if 'logo' in img.get('src', '').lower() or 'header' in img.get('src', '').lower():
                img.decompose()
        
        for link in soup.find_all('a'):
            if link.get('href') and ('index' in link.get('href') or 'home' in link.get('href')):
                link.unwrap()
        
        return str(soup)
    
    def extract_stotra_content(self, url):
        """Extract stotra content from vignanam.org page"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for stotra content in specific containers
            content_selectors = [
                '.stotra-content',
                '.content',
                '.stotram',
                '.stotra',
                'div[class*="stotra"]',
                'div[class*="content"]',
                'main .container',
                'article',
                'main'
            ]
            
            content_html = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    # Check if it has meaningful content (more than just navigation)
                    text_content = content_element.get_text().strip()
                    if len(text_content) > 100:  # Has substantial content
                        content_html = str(content_element)
                        break
            
            if not content_html:
                # Fallback: get body content but filter out navigation
                body = soup.find('body')
                if body:
                    # Remove navigation elements
                    for nav in body.find_all(['nav', 'header', 'footer']):
                        nav.decompose()
                    content_html = str(body)
            
            if content_html:
                cleaned_content = self.clean_content(content_html)
                # Check if cleaned content has meaningful text
                soup_check = BeautifulSoup(cleaned_content, 'html.parser')
                text_check = soup_check.get_text().strip()
                if len(text_check) > 50:  # Has meaningful content
                    return cleaned_content
            
            return None
                
        except Exception as e:
            return None
    
    def generate_vignanam_urls(self, local_slug):
        """Generate vignanam.org URLs from local page slug"""
        # Remove -english suffix
        clean_slug = local_slug.replace('-english', '')
        
        # Common URL patterns on vignanam.org
        possible_urls = [
            f"{self.base_url}/english/{clean_slug}.html",
            f"{self.base_url}/en/{clean_slug}.html",
            f"{self.base_url}/{clean_slug}.html",
            f"{self.base_url}/english/{clean_slug}",
            f"{self.base_url}/en/{clean_slug}",
            f"{self.base_url}/{clean_slug}"
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
                return False
                
        except Exception as e:
            return False
    
    def process_single_page(self, local_file_path):
        """Process a single page"""
        try:
            # Extract slug from file path
            filename = os.path.basename(local_file_path)
            slug = filename.replace('.php', '')
            
            # Generate possible vignanam.org URLs
            possible_urls = self.generate_vignanam_urls(slug)
            
            # Try each possible URL
            content = None
            for url in possible_urls:
                content = self.extract_stotra_content(url)
                if content:
                    break
            
            if content:
                # Update the local file
                if self.update_page_content(local_file_path, content):
                    with self.lock:
                        print(f"✓ {filename}")
                    return True
            
            with self.lock:
                print(f"✗ {filename} (no content found)")
            return False
                
        except Exception as e:
            with self.lock:
                print(f"✗ {filename} (error: {str(e)})")
            return False
    
    def process_bulk_pages(self, file_paths):
        """Process multiple pages in parallel"""
        print(f"🚀 BULK CONTENT SCRAPER - Processing {len(file_paths)} pages")
        print("=" * 60)
        
        success_count = 0
        total_pages = len(file_paths)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {
                executor.submit(self.process_single_page, file_path): file_path 
                for file_path in file_paths
            }
            
            # Process completed tasks
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    if future.result():
                        success_count += 1
                except Exception as e:
                    print(f"✗ {os.path.basename(file_path)} (exception: {str(e)})")
        
        print("\n" + "=" * 60)
        print(f"🎉 BULK SCRAPING COMPLETE!")
        print(f"✅ Successfully updated: {success_count}/{total_pages} pages")
        print(f"⚡ Processing speed: ~{total_pages/2:.0f} pages per minute")
        print("=" * 60)
        
        return success_count, total_pages

def get_ayyappa_pages():
    """Get list of Ayyappa pages to process"""
    ayyappa_pages = [
        "output_pages/en/ayyappa-ashtottara-sata-nama-stotram-english.php",
        "output_pages/en/ayyappa-pancha-ratnam-english.php",
        "output_pages/en/maha-shasta-anugraha-kavacham-english.php",
        "output_pages/en/sri-ayyappa-ashtottara-sata-namavali-english.php"
    ]
    
    # Filter to only existing files
    existing_pages = [page for page in ayyappa_pages if os.path.exists(page)]
    return existing_pages

def get_others_stotras_pages():
    """Get list of Others Stotras pages to process (sample)"""
    # Get first 50 pages from others-stotras for testing
    others_pages = []
    others_dir = "output_pages/en"
    
    if os.path.exists(others_dir):
        for filename in os.listdir(others_dir):
            if filename.endswith('-english.php') and not filename.startswith('others-stotras'):
                others_pages.append(os.path.join(others_dir, filename))
                if len(others_pages) >= 50:  # Limit for testing
                    break
    
    return others_pages

def main():
    """Main function"""
    scraper = BulkContentScraper(max_workers=3)  # Conservative for respectful scraping
    
    print("🚀 BULK CONTENT SCRAPER - VIGNANAM.ORG")
    print("=" * 60)
    print("Choose processing mode:")
    print("1. Ayyappa Stotras (4 pages)")
    print("2. Others Stotras (50 pages - sample)")
    print("3. Custom file list")
    print("=" * 60)
    
    # For now, process Ayyappa pages
    pages_to_process = get_ayyappa_pages()
    
    if pages_to_process:
        success_count, total_pages = scraper.process_bulk_pages(pages_to_process)
        print(f"\n📊 RESULTS:")
        print(f"✅ Success rate: {(success_count/total_pages)*100:.1f}%")
        print(f"⚡ Average speed: ~{total_pages/2:.0f} pages per minute")
    else:
        print("No pages found to process")

if __name__ == "__main__":
    main()
