#!/usr/bin/env python3
"""
REVERT BULK CHANGES - Restore original placeholder content
"""

import os
import re

def revert_page_content(file_path):
    """Revert page content back to placeholder"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Find the content section and replace with placeholder
        # Look for the stotramtext div and replace its content
        pattern = r'(<div class="stotramtext" id="stext">\s*<span>\s*<span style="font-family:NotoSans; line-height:150%;">\s*).*?(</span>\s*</span>\s*</div>)'
        
        replacement = r'\1<p>Content will be get from source and inserted here...</p>\2'
        
        new_content = re.sub(pattern, replacement, file_content, flags=re.DOTALL)
        
        if new_content != file_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        else:
            print(f"    -> No content found to revert in {file_path}")
            return False
    except Exception as e:
        print(f"    -> Error reverting {file_path}: {e}")
        return False

def main():
    """Main function to revert all bulk changes"""
    print("=== REVERT BULK CHANGES ===")
    print("Reverting all pages back to placeholder content...")
    
    # Pages that were updated by the fast bulk updater (23 pages)
    pages_to_revert = [
        "devi-mahatmyam-durga-sapta-adhyaya-12-english.php",
        "devi-mahatmyam-durga-sapta-adhyaya-1-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-6-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-4-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-9-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-7-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-8-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-3-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-2-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-11-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-12-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-10-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-1-english.php",
        "dakaradi-sree-durga-sahasra-nama-stotram-english.php",
        "sree-durga-nakshatra-malika-stuti-english.php",
        "sri-durga-chandrakala-stuti-english.php",
        "sri-durga-atharvasheersham-english.php",
        "sri-durga-sapta-shloki-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-5-english.php",
        "devi-mahatmyam-durga-saptasati-chapter-13-english.php",
        "devi-mahatmyam-durga-dvaatrimsannaamaavali-english.php",
        "devi-mahatmyam-durga-sapta-kavacham-english.php",
        "dakaradi-durga-ashtottara-sata-namavali-english.php"
    ]
    
    print(f"Total pages to revert: {len(pages_to_revert)}")
    
    success_count = 0
    skipped_count = 0
    
    for i, page in enumerate(pages_to_revert, 1):
        file_path = f"output_pages/en/{page}"
        
        print(f"\n[{i}/{len(pages_to_revert)}] Reverting: {page}")
        
        if not os.path.exists(file_path):
            print(f"    -> ❌ File not found: {file_path}")
            skipped_count += 1
            continue
        
        # Revert the page
        if revert_page_content(file_path):
            print(f"    -> ✅ Reverted successfully")
            success_count += 1
        else:
            print(f"    -> ⏭️  Skipped (no content to revert)")
            skipped_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"✅ Successfully reverted: {success_count} pages")
    print(f"⏭️  Skipped: {skipped_count} pages")
    print(f"📊 Total processed: {success_count + skipped_count} pages")

if __name__ == "__main__":
    main()
