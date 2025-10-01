import requests
from bs4 import BeautifulSoup
import os
import re

# ✅ Config
BASE_CATEGORY_URL = "https://www.vignanam.org/english/"
OUTPUT_DIR = "output_pages/en/"

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
               <li><a href="<?php echo $base_url; ?>/en/lakshmi-stotras">Lakshmi Stotras</a></li>
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
        print(f"Scraping: {url}")
        resp = requests.get(url, timeout=10)
        resp.encoding = "utf-8"
        
        if resp.status_code != 200:
            print(f"Error: HTTP {resp.status_code} for {url}")
            return None
            
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Look for the main content div
        content_div = soup.find("div", {"class": "stotramtext"})
        if not content_div:
            print(f"Could not find stotramtext div for {title}")
            return None
            
        # Remove unwanted tags
        for tag in content_div.find_all(["table", "style", "script", "noscript"]):
            tag.decompose()
            
        # Get the content and clean it up
        content = str(content_div)
        
        # Remove the outer div wrapper to get just the inner content
        content = content.replace('<div class="stotramtext">', '').replace('</div>', '')
        
        print(f"Successfully scraped content for {title}")
        return content
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None

def create_php_file(title, content, slug):
    """Create PHP file with the template format"""
    keywords = title.replace(" ", ", ")
    
    php_content = TEMPLATE.format(
        title=title,
        keywords=keywords,
        slug=slug,
        content=content
    )
    
    output_path = os.path.join(OUTPUT_DIR, f"{slug}.php")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(php_content)
    
    print(f"Created: {output_path}")
    return output_path

# ✅ Test pages to create
test_pages = [
    {
        "title": "Ashta Lakshmi Stotram",
        "url": "https://www.vignanam.org/english/ashta-lakshmi-stotram.html",
        "slug": "ashta-lakshmi-stotram-english"
    },
    {
        "title": "Annamayya Keerthanas Jaya Lakshmi Vara Lakshmi",
        "url": "https://www.vignanam.org/english/annamayya-keerthanas-jaya-lakshmi-vara-lakshmi.html",
        "slug": "annamayya-keerthanas-jaya-lakshmi-vara-lakshmi-english"
    }
]

# ✅ Main execution
print("Starting scraper-format.py...")
print(f"Will create {len(test_pages)} test pages")
print("=" * 50)

for page in test_pages:
    print(f"\n--- Processing: {page['title']} ---")
    
    # Scrape content
    content = scrape_stotram_page(page['url'], page['title'])
    
    if content:
        # Create PHP file
        output_path = create_php_file(page['title'], content, page['slug'])
        print(f"✅ Successfully created: {output_path}")
    else:
        print(f"❌ Failed to create: {page['title']}")

print("\n🎉 Scraper-format.py completed!")
print("Test the created pages:")
for page in test_pages:
    print(f"  - http://localhost/devotional/output_pages/en/{page['slug']}")
