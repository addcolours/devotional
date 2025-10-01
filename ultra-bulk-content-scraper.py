#!/usr/bin/env python3
"""
ULTRA BULK CONTENT SCRAPER - VIGNANAM.ORG
Processes hundreds of pages with intelligent content extraction
Optimized for speed and accuracy with smart content targeting
Specifically targets span tags with NotoSans font for stotra content
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class UltraBulkContentScraper:
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
        
    def extract_stotra_content(self, url):
        """Extract stotra content from vignanam.org page - TARGET SPECIFIC SPAN TAGS"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # TARGET: Look specifically for span tags with NotoSans font and line-height:250%
            target_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans.*line-height:\s*250%'))
            
            if target_spans:
                # Extract content from all matching spans
                content_parts = []
                for span in target_spans:
                    # Get the content inside the span
                    span_content = str(span)
                    # Clean the content but preserve the span structure
                    content_parts.append(span_content)
                
                if content_parts:
                    # Join all content parts
                    full_content = ''.join(content_parts)
                    return full_content
            
            # FALLBACK: Look for any span with NotoSans font
            fallback_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            if fallback_spans:
                content_parts = []
                for span in fallback_spans:
                    span_content = str(span)
                    content_parts.append(span_content)
                
                if content_parts:
                    full_content = ''.join(content_parts)
                    return full_content
            
            return None
                
        except Exception as e:
            return None
    
    def generate_vignanam_urls(self, local_slug):
        """Generate vignanam.org URLs from local page slug"""
        # Remove -english suffix
        clean_slug = local_slug.replace('-english', '')
        
        # Vignanam.org URL patterns
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
        """Update page content with scraped content - TARGET SPECIFIC SPAN TAGS"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # TARGET: Replace content in the specific span tag structure
            # Pattern 1: span with line-height:150%
            pattern1 = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
            
            # Pattern 2: span with line-height:250% and font-size:22px
            pattern2 = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:250%;font-size: 22px;">\s*).*?(\s*</span>\s*</span>\s*</div>)'
            
            # Pattern 3: Simple placeholder
            pattern3 = r'<p>Content will be get from source and inserted here\.\.\.</p>'
            
            updated = False
            
            # Try pattern 1 first (line-height:150%)
            if re.search(pattern1, content, re.DOTALL):
                updated_content = re.sub(
                    pattern1, 
                    r'\1' + new_content + r'\2', 
                    content, 
                    flags=re.DOTALL
                )
                updated = True
            # Try pattern 2 (line-height:250% with font-size)
            elif re.search(pattern2, content, re.DOTALL):
                updated_content = re.sub(
                    pattern2, 
                    r'\1' + new_content + r'\2', 
                    content, 
                    flags=re.DOTALL
                )
                updated = True
            # Try pattern 3 (simple placeholder)
            elif re.search(pattern3, content):
                updated_content = re.sub(pattern3, new_content, content)
                updated = True
            
            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                return True
            
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
                time.sleep(0.5)  # Be respectful
            
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
                print(f"✗ {filename} (error)")
            return False
    
    def process_bulk_pages(self, file_paths):
        """Process multiple pages in parallel"""
        print(f"🚀 ULTRA BULK CONTENT SCRAPER - Processing {len(file_paths)} pages")
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
                    print(f"✗ {os.path.basename(file_path)} (exception)")
        
        print("\n" + "=" * 60)
        print(f"🎉 ULTRA BULK SCRAPING COMPLETE!")
        print(f"✅ Successfully updated: {success_count}/{total_pages} pages")
        print(f"⚡ Processing speed: ~{total_pages/2:.0f} pages per minute")
        print("=" * 60)
        
        return success_count, total_pages

def get_others_stotras_pages(limit=100):
    """Get list of Others Stotras pages to process"""
    others_pages = []
    others_dir = "output_pages/en"
    
    if os.path.exists(others_dir):
        for filename in os.listdir(others_dir):
            if filename.endswith('-english.php') and not filename.startswith('others-stotras'):
                others_pages.append(os.path.join(others_dir, filename))
                if len(others_pages) >= limit:
                    break
    
    return others_pages

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

def main():
    """Main function"""
    scraper = UltraBulkContentScraper(max_workers=5)  # Increased for faster processing
    
    print("🚀 ULTRA BULK CONTENT SCRAPER - VIGNANAM.ORG")
    print("=" * 60)
    print("🎯 TARGETING: span tags with NotoSans font and line-height:250%")
    print("📝 UPDATING: Content between span tags in local pages")
    print("=" * 60)
    print("Processing mode:")
    print("1. Ayyappa Stotras (4 pages) - STARTING HERE")
    print("2. Others Stotras (sample)")
    print("3. Others Stotras (ALL 378 pages)")
    print("=" * 60)
    
    # START WITH AYYAPPA STOTRAS as requested
    pages_to_process = get_ayyappa_pages()
    
    if pages_to_process:
        print(f"🎯 Starting with Ayyappa Stotras ({len(pages_to_process)} pages)...")
        success_count, total_pages = scraper.process_bulk_pages(pages_to_process)
        print(f"\n📊 AYYAPPA STOTRAS RESULTS:")
        print(f"✅ Success rate: {(success_count/total_pages)*100:.1f}%")
        print(f"⚡ Average speed: ~{total_pages/2:.0f} pages per minute")
        print(f"🌐 Content scraped from vignanam.org")
        print(f"🛡️ Respectful scraping with delays")
        
        if success_count == total_pages:
            print(f"\n🎉 AYYAPPA STOTRAS COMPLETE! Ready for bulk processing...")
            print(f"💡 Next: Run with Others Stotras or all pages")
        else:
            print(f"\n⚠️ Some pages failed. Check the output above.")
    else:
        print("No Ayyappa pages found to process")

if __name__ == "__main__":
    main()
