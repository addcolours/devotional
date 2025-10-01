#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob

# ✅ Config
OUTPUT_DIR = "output_pages/en/"

# ✅ Test with a few specific files
TEST_FILES = [
    "hanuman-chalisa-english.php",
    "ganesha-stotram-english.php", 
    "krishna-ashtakam-english.php"
]

# ✅ Template based on agastya-kruta-sri-lakshmi-stotram-english.php
TEMPLATE = """<?php
   $meta_title = "{title} - ClickVedicAstro";
   $meta_description = "Full {title} lyrics in English with meaning. Collection of Spiritual and Devotional Literature in Various Indian Languages.";
   $meta_keywords = "{keywords}"; 
   $meta_url = "https://www.clickvedicastro.com/en/{slug}.php";
   include "../includes/header.php";
   ?>

<main id="content" role="main" class="main-content pt-0 pb-0">
   <!-- START: Breadcrumb -->
   <div class="page-breadcrumb bg-white py-0">
      <div class="container">
         <div class="my-3">
            <ul class="list">
               <li><a href="<?php echo $base_url; ?>/index.php">Home</a></li>
               <li><a href="<?php echo $base_url; ?>/en/" title="Stotras in English">Stotras in English</a></li>
               <li><a href="<?php echo $base_url; ?>/en/{category_slug}">{category_name}</a></li>
               <li>{title}</li>
            </ul>
         </div>
      </div>
   </div>
   <!-- END: Breadcrumb -->

   <!-- Ad Promotion Template: For my Website -->
   <div class="adpromotion mt-5">
      <?php include "../includes/ad-promotion2.php"; ?>
   </div>
   <section class="devotional-content pt-5">
      <div class="container">
         <h1 class="stotra-title">{title}</h1>
         <!-- START: Mulilanguage Menu -->
            <div id="stotramheader">
               <div class="languageView">View this in:</div>
               <ul class="language-table-menu-devotional">
               <li class="language-item active"><a href="../en/{slug}">English</a></li>
               <li class="language-item"><a href="../tl/{slug}-telugu">Telugu</a></li>
               <li class="language-item"><a href="../ta/{slug}-tamil">Tamil</a></li>
               <li class="language-item"><a href="../kn/{slug}-kannada">Kannada</a></li>
               <li class="language-item"><a href="../ml/{slug}-malayalam">Malayalam</a></li>
               <li class="language-item"><a href="../hi/{slug}-hindi">Hindi</a></li>
               <li class="language-item"><a href="../gu/{slug}-gujarati">Gujarati</a></li>              
               <li class="language-item"><a href="../mr/{slug}-marathi">Marathi</a></li>
               <li class="language-item"><a href="../bn/{slug}-bengali">Bengali</a></li>
               <li class="language-item"><a href="../pu/{slug}-punjabi">Punjabi</a></li>
               <li class="language-item"><a href="../ory/{slug}-odia">Odia</a></li>
               </ul>
            </div>
          <!-- END: Mulilanguage Menu -->
      
         <!-- START: Stotras Container -->
         <div class="stotram-content">
            <h2 class="h2">{title}</h2>
            <div class="stotram-content-inner">
               <!-- START: Stotras Content -->
               <div class="stotramtext" id="stext">
                  <span>
                     <span style="font-family:NotoSans; line-height:150%;">
                        {content}
                     </span>
                  </span>
               </div>
               <!-- END: Stotras Content -->
            </div>
         </div>
         <!-- END: Stotras Container -->
         
         <!-- Ad Promotion Template: For my Website -->
         <div class="promo mt-5 mb-5">
            <?php include "../includes/promo1-devotional.php"; ?>
         </div>
      </div>
   </section>
</main>
<?php include "../includes/footer.php"; ?>"""

# ✅ Helper functions
def get_category_from_filename(filename):
    """Determine category from filename"""
    filename_lower = filename.lower()
    
    if 'hanuman' in filename_lower or 'anjaneya' in filename_lower:
        return "hanuman-stotras"
    elif 'ganesha' in filename_lower or 'ganapati' in filename_lower:
        return "ganesha-stotras"
    elif 'krishna' in filename_lower or 'gopala' in filename_lower:
        return "krishna-stotras"
    else:
        return "others-stotras"

def get_category_name(category_slug):
    """Get display name for category"""
    category_names = {
        "hanuman-stotras": "Hanuman Stotras",
        "ganesha-stotras": "Ganesha Stotras", 
        "krishna-stotras": "Krishna Stotras",
        "others-stotras": "Others Stotras"
    }
    return category_names.get(category_slug, "Others Stotras")

def extract_title_from_filename(filename):
    """Extract title from filename"""
    # Remove .php extension
    title = filename.replace('.php', '')
    # Remove -english suffix
    title = title.replace('-english', '')
    # Replace hyphens with spaces and title case
    title = title.replace('-', ' ')
    title = ' '.join(word.capitalize() for word in title.split())
    return title

def extract_content_from_file(file_path):
    """Extract existing content from PHP file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for existing stotram content
        stotram_match = re.search(r'<div[^>]*class="stotramtext"[^>]*>(.*?)</div>', content, re.DOTALL)
        if stotram_match:
            inner_content = stotram_match.group(1)
            # Clean up the content
            inner_content = re.sub(r'<div[^>]*>', '', inner_content)
            inner_content = re.sub(r'</div>', '', inner_content)
            return inner_content.strip()
        
        # If no stotramtext div found, try to extract from other common patterns
        p_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        if p_match:
            return p_match.group(1).strip()
        
        return "<p>Content extracted from existing file...</p>"
        
    except Exception as e:
        print(f"  Error reading {file_path}: {str(e)}")
        return "<p>Content could not be extracted...</p>"

def update_file_structure(file_path):
    """Update a single file to new structure"""
    try:
        filename = os.path.basename(file_path)
        print(f"  Processing: {filename}")
        
        # Extract title and category
        title = extract_title_from_filename(filename)
        category_slug = get_category_from_filename(filename)
        category_name = get_category_name(category_slug)
        
        # Extract existing content
        content = extract_content_from_file(file_path)
        
        # Create slug
        slug = filename.replace('.php', '')
        
        # Generate new content
        keywords = title.replace(" ", ", ")
        
        new_content = TEMPLATE.format(
            title=title,
            keywords=keywords,
            slug=slug,
            category_slug=category_slug,
            category_name=category_name,
            content=content
        )
        
        # Write updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ Updated: {filename}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error updating {file_path}: {str(e)}")
        return False

def main():
    print("Starting Test Structure Updater...")
    print("=" * 60)
    
    success_count = 0
    
    for i, filename in enumerate(TEST_FILES, 1):
        file_path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(file_path):
            print(f"\n[{i}/{len(TEST_FILES)}] Processing: {filename}")
            
            if update_file_structure(file_path):
                success_count += 1
        else:
            print(f"\n[{i}/{len(TEST_FILES)}] File not found: {filename}")
    
    print(f"\n{'='*60}")
    print(f"TEST STRUCTURE UPDATE COMPLETED!")
    print(f"Successfully updated: {success_count}/{len(TEST_FILES)} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
