#!/usr/bin/env python3
"""
Script to fix article structure in all individual stotra pages.
This script removes extra <br/> and </div> tags and fixes the article structure
to match the correct format from arjuna-kruta-durga-stotram-english.php
"""

import os
import re
import glob

def fix_article_structure(file_path):
    """Fix the article structure in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the file has the problematic structure
        if '<div class="mcontainer">  <br/> </div>  <br/> </div> <div id="search">' in content:
            print(f"Fixing: {file_path}")
            
            # Fix the structure by removing extra <br/> and </div> tags
            fixed_content = content.replace(
                '<div class="mcontainer">  <br/> </div>  <br/> </div> <div id="search">',
                '<div class="mcontainer"> <div id="search">'
            )
            
            # Write the fixed content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to process all English stotra pages"""
    # Get all English stotra pages
    pattern = "output_pages/en/*-english.php"
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} English stotra pages to check")
    
    fixed_count = 0
    skipped_count = 0
    
    for file_path in files:
        if fix_article_structure(file_path):
            fixed_count += 1
        else:
            skipped_count += 1
    
    print(f"\nSummary:")
    print(f"Files fixed: {fixed_count}")
    print(f"Files skipped (already correct): {skipped_count}")
    print(f"Total files processed: {len(files)}")

if __name__ == "__main__":
    main()
