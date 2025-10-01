#!/usr/bin/env python3
"""
ROBOTIC DURGA ANALYZER - Comprehensive analysis and status report for all Durga pages
"""

import os
import re
import glob

def analyze_page_status(file_path):
    """Analyze a single page and return its status."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for placeholder content
        if 'Content will be get from source and inserted here...' in content:
            return "NEEDS_CONTENT"
        
        # Check for old malformed content (extra <br/> tags, nested <p> tags)
        if '<p><p>' in content or '<br/><br/>' in content or '<br/>' in content:
            return "NEEDS_FORMATTING_FIX"
        
        # Check for structure issues
        if 'language-table-menu-devotional' not in content:
            return "NEEDS_STRUCTURE_UPDATE"
        
        # Check if it has proper content
        if len(content) > 1000 and '॥' in content:
            return "HAS_CONTENT"
        
        return "NEEDS_CONTENT"
        
    except Exception as e:
        return f"ERROR: {e}"

def main():
    """Main analysis function."""
    print("=== ROBOTIC DURGA ANALYZER ===")
    print("Analyzing all Durga pages...")
    
    # Find all Durga pages
    durga_pattern = "output_pages/en/*durga*.php"
    durga_pages = glob.glob(durga_pattern)
    
    # Also include devi-mahatmyam pages
    devi_pattern = "output_pages/en/devi-mahatmyam*.php"
    devi_pages = glob.glob(devi_pattern)
    
    all_pages = durga_pages + devi_pages
    all_pages = list(set(all_pages))  # Remove duplicates
    all_pages.sort()
    
    print(f"Found {len(all_pages)} Durga-related pages")
    
    # Analyze each page
    status_counts = {
        "HAS_CONTENT": 0,
        "NEEDS_CONTENT": 0,
        "NEEDS_FORMATTING_FIX": 0,
        "NEEDS_STRUCTURE_UPDATE": 0,
        "ERROR": 0
    }
    
    pages_by_status = {
        "HAS_CONTENT": [],
        "NEEDS_CONTENT": [],
        "NEEDS_FORMATTING_FIX": [],
        "NEEDS_STRUCTURE_UPDATE": [],
        "ERROR": []
    }
    
    for page in all_pages:
        status = analyze_page_status(page)
        status_counts[status] = status_counts.get(status, 0) + 1
        pages_by_status[status].append(page)
    
    # Print detailed report
    print(f"\n=== DETAILED ANALYSIS REPORT ===")
    print(f"Total Pages: {len(all_pages)}")
    print(f"✅ Pages with Content: {status_counts.get('HAS_CONTENT', 0)} pages")
    print(f"🔄 Pages Needing Content: {status_counts.get('NEEDS_CONTENT', 0)} pages")
    print(f"🔧 Pages Needing Formatting Fix: {status_counts.get('NEEDS_FORMATTING_FIX', 0)} pages")
    print(f"🏗️ Pages Needing Structure Update: {status_counts.get('NEEDS_STRUCTURE_UPDATE', 0)} pages")
    print(f"❌ Pages with Errors: {status_counts.get('ERROR', 0)} pages")
    
    # Show pages that need content
    if pages_by_status.get('NEEDS_CONTENT'):
        print(f"\n=== PAGES NEEDING CONTENT ({len(pages_by_status['NEEDS_CONTENT'])}) ===")
        for page in pages_by_status['NEEDS_CONTENT']:
            print(f"  - {os.path.basename(page)}")
    
    # Show pages that need formatting fix
    if pages_by_status.get('NEEDS_FORMATTING_FIX'):
        print(f"\n=== PAGES NEEDING FORMATTING FIX ({len(pages_by_status['NEEDS_FORMATTING_FIX'])}) ===")
        for page in pages_by_status['NEEDS_FORMATTING_FIX']:
            print(f"  - {os.path.basename(page)}")
    
    # Show pages that need structure update
    if pages_by_status.get('NEEDS_STRUCTURE_UPDATE'):
        print(f"\n=== PAGES NEEDING STRUCTURE UPDATE ({len(pages_by_status['NEEDS_STRUCTURE_UPDATE'])}) ===")
        for page in pages_by_status['NEEDS_STRUCTURE_UPDATE']:
            print(f"  - {os.path.basename(page)}")
    
    # Calculate completion rate
    completed = status_counts.get('HAS_CONTENT', 0)
    total = len(all_pages)
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    print(f"\n=== COMPLETION SUMMARY ===")
    print(f"Completion Rate: {completion_rate:.1f}% ({completed}/{total} pages completed)")
    print(f"Pages with Content: {status_counts.get('HAS_CONTENT', 0)} pages ✅")
    print(f"Pages Needing Content: {status_counts.get('NEEDS_CONTENT', 0)} pages 🔄")
    print(f"Pages Needing Formatting Fix: {status_counts.get('NEEDS_FORMATTING_FIX', 0)} pages 🔧")
    print(f"Pages Needing Structure: {status_counts.get('NEEDS_STRUCTURE_UPDATE', 0)} pages 🏗️")
    
    # Save analysis results for next step
    with open('durga_analysis_results.txt', 'w', encoding='utf-8') as f:
        f.write("DURGA PAGES ANALYSIS RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Pages: {len(all_pages)}\n")
        f.write(f"Completion Rate: {completion_rate:.1f}%\n\n")
        
        for status, pages in pages_by_status.items():
            if pages:
                f.write(f"{status} ({len(pages)} pages):\n")
                for page in pages:
                    f.write(f"  - {page}\n")
                f.write("\n")
    
    print(f"\n📊 Analysis results saved to 'durga_analysis_results.txt'")
    
    return pages_by_status

if __name__ == "__main__":
    main()
