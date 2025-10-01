#!/usr/bin/env python3
"""
DURGA STATUS CHECKER - Comprehensive report on all Durga pages
"""

import os
import re

def check_page_status(file_path):
    """Check the status of a Durga page"""
    try:
        if not os.path.exists(file_path):
            return "NOT_FOUND"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for placeholder content
        placeholder = '<p>Content will be get from source and inserted here...</p>'
        has_placeholder = placeholder in content
        
        # Check for old structure (missing proper language menu)
        has_old_structure = 'language-table-menu-devotional' not in content
        
        # Check for actual content (more than just placeholder)
        has_content = len(content) > 2000 and 'om ' in content.lower()
        
        if has_placeholder:
            return "NEEDS_CONTENT"
        elif has_old_structure:
            return "NEEDS_STRUCTURE_UPDATE"
        elif has_content:
            return "HAS_CONTENT"
        else:
            return "NEEDS_CONTENT"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    """Main function to check all Durga pages"""
    print("=== DURGA PAGES STATUS CHECKER ===")
    print("Checking all Durga Stotras pages...")
    
    # Complete list of all Durga pages
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
        "output_pages/en/devi-mahatmyam-durga-saptasati-chapter-2-english.php",
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
    
    print(f"Total pages to check: {len(durga_pages)}")
    print()
    
    # Categorize pages
    categories = {
        "HAS_CONTENT": [],
        "NEEDS_CONTENT": [],
        "NEEDS_STRUCTURE_UPDATE": [],
        "NOT_FOUND": [],
        "ERROR": []
    }
    
    for i, page in enumerate(durga_pages, 1):
        print(f"[{i:2d}/{len(durga_pages)}] Checking: {os.path.basename(page)}")
        status = check_page_status(page)
        categories[status].append(page)
        print(f"    -> Status: {status}")
    
    print("\n" + "="*80)
    print("DURGA PAGES STATUS REPORT")
    print("="*80)
    
    # Report by category
    for category, pages in categories.items():
        if pages:
            print(f"\n{category} ({len(pages)} pages):")
            print("-" * 50)
            for page in pages:
                print(f"  • {os.path.basename(page)}")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✅ HAS_CONTENT: {len(categories['HAS_CONTENT'])} pages")
    print(f"🔄 NEEDS_CONTENT: {len(categories['NEEDS_CONTENT'])} pages")
    print(f"🔧 NEEDS_STRUCTURE_UPDATE: {len(categories['NEEDS_STRUCTURE_UPDATE'])} pages")
    print(f"❌ NOT_FOUND: {len(categories['NOT_FOUND'])} pages")
    print(f"⚠️  ERROR: {len(categories['ERROR'])} pages")
    
    total_processed = len(categories['HAS_CONTENT'])
    total_pages = len(durga_pages)
    completion_rate = (total_processed / total_pages) * 100
    
    print(f"\n📊 COMPLETION RATE: {completion_rate:.1f}% ({total_processed}/{total_pages})")
    
    if categories['NEEDS_CONTENT']:
        print(f"\n🎯 NEXT STEPS: {len(categories['NEEDS_CONTENT'])} pages need content updates")
    if categories['NEEDS_STRUCTURE_UPDATE']:
        print(f"🔧 STRUCTURE FIXES: {len(categories['NEEDS_STRUCTURE_UPDATE'])} pages need structure updates")

if __name__ == "__main__":
    main()
