#!/usr/bin/env python3
"""
BULK PAGE GENERATOR - Ultra Fast & Accurate
Processes hundreds of pages in minutes with perfect template structure
"""

import os
import re
from pathlib import Path

# Template for all pages
TEMPLATE = '''<?php
   $meta_title = "{title} - ClickVedicAstro";
   $meta_description = "Full {title} lyrics in English with meaning. Collection of Spiritual and Devotional Literature in Various Indian Languages.";
   $meta_keywords = "{keywords}"; 
   $meta_url = "https://www.clickvedicastro.com/en/{filename}.php";
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
               <li><a href="<?php echo $base_url; ?>/en/{category}">{category_title}</a></li>
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
               <li class="language-item active"><a href="../en/{filename}">English</a></li>
               <li class="language-item"><a href="../tl/{filename}-telugu">Telugu</a></li>
               <li class="language-item"><a href="../ta/{filename}-tamil">Tamil</a></li>
               <li class="language-item"><a href="../kn/{filename}-kannada">Kannada</a></li>
               <li class="language-item"><a href="../ml/{filename}-malayalam">Malayalam</a></li>
               <li class="language-item"><a href="../hi/{filename}-hindi">Hindi</a></li>
               <li class="language-item"><a href="../gu/{filename}-gujarati">Gujarati</a></li>              
               <li class="language-item"><a href="../mr/{filename}-marathi">Marathi</a></li>
               <li class="language-item"><a href="../bn/{filename}-bengali">Bengali</a></li>
               <li class="language-item"><a href="../pu/{filename}-punjabi">Punjabi</a></li>
               <li class="language-item"><a href="../ory/{filename}-odia">Odia</a></li>
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
                        <p>Content will be get from source and inserted here...</p>
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
<?php include "../includes/footer.php"; ?>'''

# Category mappings
CATEGORIES = {
    'ayyappa': ('ayyappa-stotras', 'Ayyappa Swamy Stotras'),
    'dattatreya': ('dattatreya-stotras', 'Dattatreya Stotras'),
    'durga': ('durga-stotras', 'Durga Stotras'),
    'gayatri': ('gayatri-stotras', 'Gayatri Stotras'),
    'ganesha': ('ganesha-stotras', 'Ganesha Stotras'),
    'hanuman': ('hanuman-stotras', 'Hanuman Stotras'),
    'krishna': ('krishna-stotras', 'Krishna Stotras'),
    'lakshmi': ('lakshmi-stotras', 'Lakshmi Stotras'),
    'narasimha': ('narasimha-swamy-stotras', 'Narasimha Swamy Stotras'),
    'nava-graha': ('nava-graha-stotras', 'Nava Graha Stotras'),
    'saraswati': ('saraswati-stotras', 'Saraswati Stotras'),
    'shiva': ('shiva-stotras', 'Shiva Stotras'),
    'sri-venkateswara': ('sri-venkateswara', 'Sri Venkateswara'),
    'subrahmanya': ('subrahmanya-stotras', 'Subrahmanya Stotras'),
    'surya': ('surya-bhagawan', 'Surya Bhagawan'),
    'suktam': ('suktam-stotras', 'Suktam Stotras'),
    'suprabhatam': ('suprabhatam-stotras', 'Suprabhatam Stotras'),
    'vishnu': ('vishnu-stotras', 'Vishnu Stotras'),
    'sahasanama': ('sahasanama-stotras', 'Sahasanama Stotras'),
    'shirdi-sai': ('shirdi-sai-baba', 'Shirdi Sai Baba'),
    'others': ('others-stotras', 'Others Stotras')
}

def detect_category(filename):
    """Auto-detect category from filename"""
    filename_lower = filename.lower()
    
    for key, (category, title) in CATEGORIES.items():
        if key in filename_lower:
            return category, title
    
    # Default fallback
    return 'others-stotras', 'Others Stotras'

def generate_title(filename):
    """Generate proper title from filename"""
    # Remove -english suffix
    title = filename.replace('-english', '')
    # Replace hyphens with spaces
    title = title.replace('-', ' ')
    # Capitalize each word
    title = ' '.join(word.capitalize() for word in title.split())
    return title

def generate_keywords(filename):
    """Generate keywords from filename"""
    # Remove -english suffix
    keywords = filename.replace('-english', '')
    # Replace hyphens with commas
    keywords = keywords.replace('-', ', ')
    return keywords

def process_bulk_pages(file_list):
    """Process hundreds of pages in one go"""
    output_dir = Path("output_pages/en")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processed = 0
    errors = []
    
    print(f"🚀 BULK PROCESSING: {len(file_list)} pages")
    print("=" * 50)
    
    for i, filename in enumerate(file_list, 1):
        try:
            # Generate content
            title = generate_title(filename)
            keywords = generate_keywords(filename)
            category, category_title = detect_category(filename)
            
            # Create file content
            content = TEMPLATE.format(
                title=title,
                keywords=keywords,
                filename=filename,
                category=category,
                category_title=category_title
            )
            
            # Write file
            file_path = output_dir / f"{filename}.php"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            processed += 1
            if i % 10 == 0:  # Progress every 10 files
                print(f"✅ Processed {i}/{len(file_list)} pages...")
                
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")
    
    print("=" * 50)
    print(f"🎉 COMPLETED: {processed}/{len(file_list)} pages processed")
    
    if errors:
        print(f"❌ ERRORS: {len(errors)} files failed")
        for error in errors[:5]:  # Show first 5 errors
            print(f"   {error}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more errors")
    
    return processed, errors

def main():
    """Main function - ready for massive file lists"""
    
    # Example usage - you can add hundreds of filenames here
    example_files = [
        "sri-rama-ashtakam-english",
        "sri-krishna-ashtakam-english", 
        "sri-shiva-ashtakam-english",
        "sri-durga-ashtakam-english",
        "sri-lakshmi-ashtakam-english",
        "sri-ganesha-ashtakam-english",
        "sri-hanuman-ashtakam-english",
        "sri-venkateswara-ashtakam-english",
        "sri-narasimha-ashtakam-english",
        "sri-subrahmanya-ashtakam-english"
    ]
    
    print("🔥 ULTRA-FAST BULK PAGE GENERATOR")
    print("=" * 50)
    print("Ready to process hundreds of files in minutes!")
    print("Just add your file list to the script and run!")
    print("=" * 50)
    
    # Uncomment to run with example files
    # process_bulk_pages(example_files)
    
    print("\n💡 TO USE:")
    print("1. Add your file list to the 'example_files' list")
    print("2. Uncomment the process_bulk_pages() call")
    print("3. Run: python bulk-page-generator.py")
    print("4. Watch hundreds of pages get created in seconds!")

if __name__ == "__main__":
    main()
