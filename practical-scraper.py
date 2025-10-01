#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import re
import time

# ✅ Config
OUTPUT_DIR = "output_pages/en/"

# ✅ Predefined URLs for testing (since category pages are blocked)
TEST_URLS = [
    # Ayyappa Swamy Stotras
    {
        "title": "Ayyappa Swamy Stotram",
        "url": "https://www.vignanam.org/english/ayyappa-swamy-stotram.html",
        "category_slug": "ayyappa-swamy-stotras",
        "category_name": "Ayyappa Swamy Stotras"
    },
    {
        "title": "Ayyappa Suprabhatam",
        "url": "https://www.vignanam.org/english/ayyappa-suprabhatam.html",
        "category_slug": "ayyappa-swamy-stotras", 
        "category_name": "Ayyappa Swamy Stotras"
    },
    # Dattatreya Stotras
    {
        "title": "Dattatreya Ashtottara Sata Namavali",
        "url": "https://www.vignanam.org/english/dattatreya-ashtottara-sata-namavali.html",
        "category_slug": "dattatreya-stotras",
        "category_name": "Dattatreya Stotras"
    },
    {
        "title": "Sri Dattatreya Stotram",
        "url": "https://www.vignanam.org/english/sri-dattatreya-stotram.html",
        "category_slug": "dattatreya-stotras",
        "category_name": "Dattatreya Stotras"
    },
    # Ganesha Stotrasd2wedn
    {
        "title": "Ganesha Ashtottara Sata Namavali",
        "url": "https://www.vignanam.org/english/ganesha-ashtottara-sata-namavali.html",
        "category_slug": "ganesha-stotras",
        "category_name": "Ganesha Stotras"
    },
    {
        "title": "Ganesha Stotram",
        "url": "https://www.vignanam.org/english/ganesha-stotram.html",
        "category_slug": "ganesha-stotras",
        "category_name": "Ganesha Stotras"
    }
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
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def scrape_stotram_page(url, title):
    """Scrape content from vignanam.org"""
    try:
        print(f"  Scraping: {url}")
        resp = requests.get(url, timeout=15)
        resp.encoding = "utf-8"
        
        if resp.status_code != 200:
            print(f"  Error: HTTP {resp.status_code} for {url}")
            return None
            
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Look for the main content div
        content_div = soup.find("div", {"class": "stotramtext"})
        if not content_div:
            print(f"  Could not find stotramtext div for {title}")
            return None
            
        # Remove unwanted tags - including aqtree3clickable
        for tag in content_div.find_all(["table", "style", "script", "noscript", "ul"]):
            # Specifically remove aqtree3clickable ul elements
            if tag.name == "ul" and tag.get("class") and "aqtree3clickable" in tag.get("class"):
                print("  Removing aqtree3clickable ul element")
                tag.decompose()
            else:
                tag.decompose()
            
        # Get the content and clean it up
        content = str(content_div)
        
        # Remove the outer div wrapper to get just the inner content
        content = content.replace('<div class="stotramtext">', '').replace('<div class="stotramtext" id="stext">', '').replace('</div>', '')
        
        # Remove any remaining div tags that might be nested
        content = re.sub(r'<div[^>]*>', '', content)
        content = re.sub(r'</div>', '', content)
        
        print(f"  Successfully scraped content for {title}")
        return content
        
    except Exception as e:
        print(f"  Error scraping {url}: {str(e)}")
        return None

def create_php_file(title, content, slug, category_slug, category_name):
    """Create PHP file with the template format"""
    keywords = title.replace(" ", ", ")
    
    php_content = TEMPLATE.format(
        title=title,
        keywords=keywords,
        slug=slug,
        category_slug=category_slug,
        category_name=category_name,
        content=content
    )
    
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.php")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(php_content)
    
    print(f"  Created: {output_path}")
    return output_path

def process_pages(pages):
    """Process all pages"""
    print(f"\n{'='*60}")
    print(f"Processing {len(pages)} Pages")
    print(f"{'='*60}")
    
    success_count = 0
    
    for i, page in enumerate(pages, 1):
        print(f"\n[{i}/{len(pages)}] Processing: {page['title']}")
        print(f"  Category: {page['category_name']}")
        
        # Scrape content
        content = scrape_stotram_page(page['url'], page['title'])
        
        if content:
            # Create slug
            slug = slugify(page['title']) + "-english"
            
            # Create PHP file
            output_path = create_php_file(
                page['title'], 
                content, 
                slug, 
                page['category_slug'], 
                page['category_name']
            )
            
            if output_path:
                success_count += 1
                print(f"  ✅ Success: {page['title']}")
            else:
                print(f"  ❌ Failed to create: {page['title']}")
        else:
            print(f"  ❌ Failed to scrape: {page['title']}")
        
        # Add delay to be respectful to the server
        time.sleep(1)
    
    print(f"\nCompleted: {success_count}/{len(pages)} pages successful")
    return success_count

# ✅ Main execution
def main():
    print("Starting Practical Scraper...")
    print("=" * 60)
    
    success_count = process_pages(TEST_URLS)
    
    print(f"\n{'='*60}")
    print(f"PRACTICAL SCRAPING COMPLETED!")
    print(f"Total pages processed successfully: {success_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
