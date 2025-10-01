#!/usr/bin/env python3
"""
Direct Durga Kavacham Content Updater
"""

import requests
from bs4 import BeautifulSoup
import re

def get_durga_kavacham_content():
    """Get Durga Kavacham content from vignanam.org"""
    try:
        # Try the most likely URL
        url = "https://vignanam.org/veda/durga-kavacham-english.html"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for span tags with NotoSans font
            target_spans = soup.find_all('span', style=re.compile(r'font-family:\s*NotoSans'))
            print(f"Found {len(target_spans)} NotoSans spans")
            
            if target_spans:
                content_parts = []
                for span in target_spans:
                    content_parts.append(str(span))
                full_content = ''.join(content_parts)
                print(f"Content length: {len(full_content)} characters")
                return full_content
            else:
                print("No NotoSans spans found")
                return None
        else:
            print(f"HTTP Error: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def update_durga_kavacham_file(content):
    """Update the Durga Kavacham file with new content"""
    if not content:
        print("No content to update")
        return False
    
    try:
        file_path = "output_pages/en/durga-kavacham-english.php"
        
        # Read current file
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Replace the placeholder content
        placeholder = '<p>Content will be get from source and inserted here...</p>'
        
        if placeholder in file_content:
            # Replace with actual content
            new_content = content
            updated_content = file_content.replace(placeholder, new_content)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"Successfully updated {file_path}")
            return True
        else:
            print("Placeholder not found in file")
            return False
            
    except Exception as e:
        print(f"Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Durga Kavacham Content Updater ===")
    print("Starting script...")
    
    # Get content from vignanam.org
    print("Getting content from vignanam.org...")
    content = get_durga_kavacham_content()
    
    if content:
        print("Content received, updating file...")
        # Update the local file
        success = update_durga_kavacham_file(content)
        if success:
            print("✅ Durga Kavacham page updated successfully!")
        else:
            print("❌ Failed to update file")
    else:
        print("❌ Failed to get content from vignanam.org")
    
    print("Script completed.")
