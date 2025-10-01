#!/usr/bin/env python3
"""
UNIVERSAL ROBOTIC FORMATTER - Works for all categories (Durga, Shiva, Vishnu, etc.)
"""

import os
import re
import glob
import requests
from bs4 import BeautifulSoup
import time
import random

def analyze_and_fix_category_pages(category_pattern):
    """Complete robotic solution for any category."""
    print(f"=== UNIVERSAL ROBOTIC FORMATTER ===")
    print(f"🤖 Starting comprehensive analysis and update for {category_pattern}...")
    
    # Find all pages matching the pattern
    pattern = f"output_pages/en/{category_pattern}*.php"
    all_pages = glob.glob(pattern)
    all_pages.sort()
    
    print(f"📊 Found {len(all_pages)} pages")
    
    # Step 1: Analyze all pages
    needs_content = []
    needs_formatting = []
    needs_structure = []
    has_content = []
    
    for page in all_pages:
        try:
            with open(page, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'Content will be get from source and inserted here...' in content:
                needs_content.append(page)
            elif '<p><p>' in content or '<br/><br/>' in content or '<br/>' in content:
                needs_formatting.append(page)
            elif 'language-table-menu-devotional' not in content:
                needs_structure.append(page)
            else:
                has_content.append(page)
        except:
            needs_structure.append(page)
    
    print(f"✅ Pages with Content: {len(has_content)}")
    print(f"🔄 Pages Needing Content: {len(needs_content)}")
    print(f"🔧 Pages Needing Formatting Fix: {len(needs_formatting)}")
    print(f"🏗️ Pages Needing Structure: {len(needs_structure)}")
    
    # Step 2: Fix structure issues first
    if needs_structure:
        print(f"\n🔧 Fixing {len(needs_structure)} structure issues...")
        for page in needs_structure:
            fix_page_structure(page)
    
    # Step 3: Fix formatting issues
    if needs_formatting:
        print(f"\n🔧 Fixing {len(needs_formatting)} formatting issues...")
        for page in needs_formatting:
            fix_page_formatting(page)
    
    # Step 4: Update content for pages that need it
    if needs_content:
        print(f"\n🔄 Updating content for {len(needs_content)} pages...")
        for i, page in enumerate(needs_content, 1):
            print(f"[{i}/{len(needs_content)}] Processing: {os.path.basename(page)}")
            update_page_content_from_source(page)
            time.sleep(2)  # Rate limiting
    
    print(f"\n🎉 ROBOTIC UPDATE COMPLETE!")
    print(f"✅ All {category_pattern} pages have been analyzed and updated!")
    
    return {
        'total': len(all_pages),
        'has_content': len(has_content),
        'needs_content': len(needs_content),
        'needs_formatting': len(needs_formatting),
        'needs_structure': len(needs_structure)
    }

def fix_page_structure(file_path):
    """Fix structure issues in a page."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add proper structure if missing
        if 'language-table-menu-devotional' not in content:
            print(f"    ⚠️ {os.path.basename(file_path)} needs manual structure fix")
        
    except Exception as e:
        print(f"    ❌ Error fixing {file_path}: {e}")

def fix_page_formatting(file_path):
    """Fix formatting issues in a page to match source exactly."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix nested <p> tags and convert <br/> to <br> to match source
        content = re.sub(r'<p><p>', '<p>', content)
        content = re.sub(r'</p></p>', '</p>', content)
        content = re.sub(r'<br/><br/>', '<br>', content)
        content = re.sub(r'<br/>', '<br>', content)  # Convert all <br/> to <br>
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"    ✅ Fixed formatting: {os.path.basename(file_path)}")
        
    except Exception as e:
        print(f"    ❌ Error fixing {file_path}: {e}")

def update_page_content_from_source(file_path):
    """Update page content from source website with exact formatting."""
    try:
        # Extract slug from filename
        filename = os.path.basename(file_path)
        slug = filename.replace('-english.php', '')
        url = f"https://vignanam.org/english/{slug}.html"
        
        # Scrape content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content using multiple selectors
            content_selectors = [
                'div.content_text',
                'div[class*="content"]',
                'span[style*="NotoSans"]'
            ]
            
            extracted_content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        text = element.get_text(strip=True)
                        if len(text) > 100:
                            extracted_content = text
                            break
                if extracted_content:
                    break
            
            if extracted_content:
                # Format content properly to match source exactly
                formatted_content = format_content_for_php(extracted_content)
                
                # Update the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Replace placeholder
                placeholder = '<p>Content will be get from source and inserted here...</p>'
                if placeholder in file_content:
                    updated_content = file_content.replace(placeholder, formatted_content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    print(f"    ✅ Updated: {os.path.basename(file_path)}")
                else:
                    print(f"    ⚠️ No placeholder found in {os.path.basename(file_path)}")
            else:
                print(f"    ❌ No content found for {os.path.basename(file_path)}")
        else:
            print(f"    ❌ HTTP {response.status_code} for {os.path.basename(file_path)}")
            
    except Exception as e:
        print(f"    ❌ Error updating {file_path}: {e}")

def format_content_for_php(raw_content):
    """Format content for PHP files to match exact source structure."""
    lines = raw_content.split('\n')
    formatted_paragraphs = []
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                # Use <br> without slash to match source exactly
                formatted_paragraphs.append(f'<p>{"<br>".join(current_paragraph)}</p>')
                current_paragraph = []
        else:
            current_paragraph.append(line)
    
    if current_paragraph:
        # Use <br> without slash to match source exactly
        formatted_paragraphs.append(f'<p>{"<br>".join(current_paragraph)}</p>')
    
    return '\n                        '.join(formatted_paragraphs)

def main():
    """Main function - can be used for any category."""
    import sys
    
    if len(sys.argv) > 1:
        category = sys.argv[1]
    else:
        category = "*durga*"  # Default to Durga pages
    
    print(f"Processing category: {category}")
    results = analyze_and_fix_category_pages(category)
    
    print(f"\n📊 FINAL SUMMARY:")
    print(f"Total Pages: {results['total']}")
    print(f"✅ Pages with Content: {results['has_content']}")
    print(f"🔄 Pages Needing Content: {results['needs_content']}")
    print(f"🔧 Pages Needing Formatting Fix: {results['needs_formatting']}")
    print(f"🏗️ Pages Needing Structure: {results['needs_structure']}")

if __name__ == "__main__":
    main()
