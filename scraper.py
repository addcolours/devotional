import requests
from bs4 import BeautifulSoup
import os
import re

# ✅ Config
BASE_CATEGORY_URL = "https://www.vignanam.org/english/"
OUTPUT_DIR = "output_pages/en/"
LANGUAGE_MENU = """
<ul class="language-table-menu-devotional">
   <li class="language-item active"><a href="../english/{slug}.html">English</a></li>
   <li class="language-item"><a href="../devanagari/{slug}.html">Devanagari</a></li>
   <li class="language-item"><a href="../telugu/{slug}.html">Telugu</a></li>
   <li class="language-item"><a href="../tamil/{slug}.html">Tamil</a></li>
   <li class="language-item"><a href="../kannada/{slug}.html">Kannada</a></li>
   <li class="language-item"><a href="../malayalam/{slug}.html">Malayalam</a></li>
   <li class="language-item"><a href="../gujarati/{slug}.html">Gujarati</a></li>
   <li class="language-item"><a href="../odia/{slug}.html">Odia</a></li>
   <li class="language-item"><a href="../bengali/{slug}.html">Bengali</a></li>
   <li class="language-item"><a href="../marathi/{slug}.html">Marathi</a></li>
   <li class="language-item"><a href="../assamese/{slug}.html">Assamese</a></li>
   <li class="language-item"><a href="../punjabi/{slug}.html">Punjabi</a></li>
   <li class="language-item"><a href="../hindi/{slug}.html">Hindi</a></li>
   <li class="language-item"><a href="../samskritam/{slug}.html">Samskritam</a></li>
   <li class="language-item"><a href="../konkani/{slug}.html">Konkani</a></li>
   <li class="language-item"><a href="../nepali/{slug}.html">Nepali</a></li>
   <li class="language-item"><a href="../sinhala/{slug}.html">Sinhala</a></li>
   <li class="language-item"><a href="../grantha/{slug}.html">Grantha</a></li>
</ul>
"""

TEMPLATE = """<?php
$meta_title = "{title} - ClickVedicAstro";
$meta_description = "Full {title} lyrics in English with meaning. Collection of Spiritual and Devotional Literature in Various Indian Languages.";
$meta_keywords = "{keywords}"; 
$meta_url = "https://www.clickvedicastro.com/en/{slug}.php";
include "../includes/header.php";
?>

<main id="content" role="main" class="main-content pt-0 pb-0">
   <div class="page-breadcrumb bg-white py-0">
      <div class="container">
         <div class="my-3">
            <ul class="list">
               <li><a href="<?php echo $base_url; ?>/index.php">Home</a></li>
               <li><a href="<?php echo $base_url; ?>/en/" title="Stotras in English">Stotras in English</a></li>
               <li>{title}</li>
            </ul>
         </div>
      </div>
   </div>

   <section class="devotional-content pt-5">
      <div class="container">
         <h1 class="stotra-title">{title}</h1>
         <div id="stotramheader">
            <div class="languageView">View this in:</div>
            {language_menu}
         </div>

         <div class="stotram-content">
            <h2 class="h2">{title}</h2>
            <div class="stotram-content-inner">
               <!-- START: Stotras Content -->
               {content}
               <!-- END: Stotras Content -->
            </div>
         </div>
      </div>
   </section>
</main>

<?php include "../includes/footer.php"; ?>
"""

# ✅ Helper functions
def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def scrape_stotram_page(url, title):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    content_div = soup.find("div", {"class": "stotramtext"})
    if not content_div:
        print(f"Could not find content for {title}")
        return None
    # Remove unwanted tags
    for tag in content_div.find_all(["table", "style", "script"]):
        tag.decompose()
    return str(content_div)

# ✅ Step 1: Get all English stotras URLs
print(f"Fetching category page: {BASE_CATEGORY_URL}")
resp = requests.get(BASE_CATEGORY_URL)
print(f"Response status: {resp.status_code}")
resp.encoding = "utf-8"
soup = BeautifulSoup(resp.text, "html.parser")

stotra_links = []
all_links = soup.find_all("a", href=True)
print(f"Found {len(all_links)} total links")

for a in all_links:
    href = a["href"]
    text = a.get_text(strip=True)
    if "english" in href.lower() and text:
        stotra_links.append((href, text))
        print(f"Added: {text} -> {href}")

print(f"Found {len(stotra_links)} English stotras")
for i, (href, title) in enumerate(stotra_links[:5]):  # Show first 5
    print(f"  {i+1}. {title} -> {href}")

# ✅ Step 2: Scrape each stotram and generate PHP
for href, title in stotra_links:
    page_url = "https://www.vignanam.org/" + href
    content_html = scrape_stotram_page(page_url, title)
    if content_html:
        slug = slugify(title)
        language_menu_final = LANGUAGE_MENU.format(slug=slug)
        php_content = TEMPLATE.format(title=title, keywords=title.replace(" ", ", "), slug=slug, language_menu=language_menu_final, content=content_html)
        output_path = os.path.join(OUTPUT_DIR, f"{slug}.php")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(php_content)
        print(f"Saved: {output_path}")

print("All English stotras completed!")
