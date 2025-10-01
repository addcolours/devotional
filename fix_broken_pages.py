#!/usr/bin/env python3
"""
Script to automatically fix broken PHP pages by comparing with reference file
and adding missing elements without deleting the entire file.
"""

import os
import re
import glob

def get_reference_structure():
    """Get the complete structure from the reference file"""
    reference_file = "output_pages/en/agastya-kruta-sri-lakshmi-stotram-english.php"
    
    with open(reference_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract key sections from reference
    sections = {}
    
    # Language table birth template
    sections['language_table_birth'] = '    <?php include "../includes/language-table-birth.php"; ?><!-- Language Birth Template-->'
    
    # Search and header section
    search_header_match = re.search(r'<div id="search">.*?</div> <div id="stotramheader">.*?</div>', content, re.DOTALL)
    if search_header_match:
        sections['search_header'] = search_header_match.group(0)
    
    # Language menu structure
    lang_menu_match = re.search(r'<ul class="language-table-menu-devotional">.*?</ul>', content, re.DOTALL)
    if lang_menu_match:
        sections['language_menu'] = lang_menu_match.group(0)
    
    # Language prefix
    lang_prefix_match = re.search(r'<div class="languagePrefix">.*?</div>', content, re.DOTALL)
    if lang_prefix_match:
        sections['language_prefix'] = lang_prefix_match.group(0)
    
    # Table structure with content
    table_match = re.search(r'<table>.*?</table>', content, re.DOTALL)
    if table_match:
        sections['table_structure'] = table_match.group(0)
    
    # Footer
    footer_match = re.search(r'<footer class="deepLinkFooter">.*?</footer>', content, re.DOTALL)
    if footer_match:
        sections['footer'] = footer_match.group(0)
    
    return sections

def fix_broken_file(file_path, sections):
    """Fix a single broken file by adding missing elements"""
    print(f"Fixing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has broken structure (missing search, incomplete language menu, etc.)
    if 'languagePrefix' in content and 'footer' in content and 'languagePrefix.*\n.*footer' in content:
        print(f"  - File appears to have broken structure")
        
        # Fix 1: Add missing language table birth template
        if 'language-table-birth.php' not in content:
            content = content.replace(
                '<div class="container">',
                f'<div class="container">\n{sections["language_table_birth"]}'
            )
        
        # Fix 2: Add search and header section
        if 'id="search"' not in content:
            # Find the mcontainer div and add search section
            content = re.sub(
                r'(<div class="mcontainer">)',
                r'\1\n      ' + sections['search_header'].replace('\n', '\n      '),
                content
            )
        
        # Fix 3: Fix language menu structure
        if 'language-table-menu-devotional' not in content:
            # Replace broken language menu with proper structure
            broken_menu_pattern = r'<li class=" active">.*?</ul>'
            if re.search(broken_menu_pattern, content, re.DOTALL):
                # Extract the page name for language links
                page_name = os.path.basename(file_path).replace('-english.php', '')
                
                # Create proper language menu
                proper_menu = sections['language_menu']
                # Replace the page name in all language links
                proper_menu = re.sub(r'../[^/]+/[^"]+\.html', f'../{{language}}/{page_name}.html', proper_menu)
                
                content = re.sub(broken_menu_pattern, proper_menu, content, flags=re.DOTALL)
        
        # Fix 4: Add language prefix
        if 'IAST' not in content:
            content = re.sub(
                r'(</ul>)',
                r'\1\n      \n      ' + sections['language_prefix'],
                content
            )
        
        # Fix 5: Add table structure with content placeholder
        if '<table>' not in content:
            # Extract page title
            title_match = re.search(r'<h1 class="stotra-title">(.*?)</h1>', content)
            page_title = title_match.group(1) if title_match else "Page Title"
            
            # Create table structure with page-specific title
            table_structure = sections['table_structure']
            table_structure = re.sub(r'<p class="stotramtitle" id="stitle">.*?</p>', 
                                   f'<p class="stotramtitle" id="stitle"> {page_title} </p>', 
                                   table_structure)
            
            content = re.sub(
                r'(<div class="languagePrefix">.*?</div>)',
                r'\1 <br/> </div> ' + table_structure,
                content,
                flags=re.DOTALL
            )
        
        # Fix 6: Add footer
        if 'deepLinkFooter' not in content:
            content = re.sub(
                r'(</table>)',
                r'\1 </div> ' + sections['footer'],
                content
            )
        
        # Fix 7: Add proper promo section
        if 'promo1-devotional.php' not in content:
            promo_section = '''    <!-- Ad Promotion Template: For my Website -->
    <div class="promo mt-5 mb-5">
        <?php include "../includes/promo1-devotional.php"; ?>
    </div>'''
            content = re.sub(
                r'(</article>)',
                r'\1\n    \n' + promo_section,
                content
            )
        
        # Fix 8: Add proper footer include
        if 'includes/footer.php' not in content:
            content = re.sub(
                r'(</main>)',
                r'\1\n\n<?php include "../includes/footer.php"; ?>',
                content
            )
        
        # Write the fixed content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ Fixed successfully")
        return True
    
    return False

def main():
    """Main function to fix all broken files"""
    print("🔧 Starting automatic fix for broken PHP pages...")
    
    # Get reference structure
    sections = get_reference_structure()
    print(f"📋 Loaded reference structure from agastya-kruta-sri-lakshmi-stotram-english.php")
    
    # Find all PHP files that might be broken
    php_files = glob.glob('output_pages/en/*-english.php')
    
    fixed_count = 0
    total_files = len(php_files)
    
    for file_path in php_files:
        if fix_broken_file(file_path, sections):
            fixed_count += 1
    
    print(f"\n✅ Completed! Fixed {fixed_count} out of {total_files} files.")
    print("🎯 All broken pages should now have proper structure matching the reference file.")

if __name__ == "__main__":
    main()
