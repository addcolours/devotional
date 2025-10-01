import os, re, time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://vignanam.org"
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUT_DIR = "output_pages/en"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- Helpers ----------
def get_page(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def norm_space(txt):
    # Clean HTML entities first
    txt = txt.replace("&nbsp;", " ")
    txt = txt.replace("&amp;", "&")
    txt = txt.replace("&lt;", "<")
    txt = txt.replace("&gt;", ">")
    txt = txt.replace("&quot;", '"')
    txt = txt.replace("&#39;", "'")
    # Then normalize spaces
    return re.sub(r"\s+", " ", txt).strip()

def clean_html_entities(text):
    """Clean HTML entities from text"""
    if not text:
        return text
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&apos;", "'")
    # Clean up multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

def to_filename(title: str, suffix="-english.php"):
    # Clean HTML entities first
    title = clean_html_entities(title)
    slug = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
    slug = re.sub(r"\s+", "-", slug.strip().lower())
    slug = re.sub(r"-+", "-", slug)
    return f"{slug}{suffix}"

def deity_bucket_from_href(href: str):
    # naive bucketing from path; adjust as needed
    s = href.lower()
    if "siva" in s or "shiva" in s: return "Shiva"
    if "vishnu" in s: return "Vishnu"
    if "lakshmi" in s or "laxmi" in s: return "Lakshmi"
    if "hanuman" in s or "anjaneya" in s: return "Hanuman"
    if "ganesha" in s or "ganesh" in s or "vinayaka" in s: return "Ganesha"
    if "durga" in s: return "Durga"
    if "saraswati" in s or "sarasvati" in s: return "Saraswati"
    if "subrahmanya" in s or "murugan" in s or "kartikeya" in s: return "Subrahmanya"
    if "sahasranama" in s or "sahasranamam" in s: return "Sahasranama"
    if "suprabhat" in s: return "Suprabhatam"
    if "suktam" in s: return "Suktam"
    return "Others"

def build_meta_description(title: str, first_para: str):
    base = f"Full {title} lyrics in English with meaning. "
    if first_para:
        text = norm_space(re.sub("<[^>]+>", " ", first_para))  # strip tags
        cand = (base + text).strip()
    else:
        cand = base + "A devotional hymn."
    return (cand[:157] + "...") if len(cand) > 160 else cand

# ---------- 1) Collect English links from the hub ----------
# NOTE: We fetch without the # fragment; server returns full HTML.
hub_url = urljoin(BASE, "index.html")  # english hub is on the home
hub_html = get_page(hub_url)
hub = BeautifulSoup(hub_html, "html.parser")

# gather links that clearly point to English stotra pages
stotra_links = []
for a in hub.select("a[href]"):
    href = a.get("href")
    if not href: 
        continue
    # absolute-ize
    abs_url = urljoin(BASE, href)
    # include pages that are under /english/ and end with .html
    if "/english/" in abs_url and abs_url.endswith(".html"):
        text = a.get_text(strip=True)
        stotra_links.append((text, abs_url))

# de-duplicate by URL, keep the first seen text
seen = set()
filtered = []
for text, url in stotra_links:
    if url in seen:
        continue
    seen.add(url)
    filtered.append((text or url.split("/")[-1].replace(".html",""), url))

if not filtered:
    raise SystemExit("No English stotra links found on the hub. Inspect the selectors.")

# Try to pick Kanakadhara; else pick first
pick_url = None
pick_title = None
for text, url in filtered:
    if "kanakadhara" in url.lower():
        pick_url = url
        pick_title = text if text else "Kanakadhara Stotram"
        break
if not pick_url:
    pick_title, pick_url = filtered[0][0], filtered[0][1]

# ---------- 2) Download and create individual stotra pages ----------
def deity_to_slug(deity_name):
    """Convert deity name to URL-friendly slug"""
    slug = re.sub(r"[^a-z0-9-]+", "-", deity_name.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug

def create_stotra_page(title, url, deity_category=None):
    """Create individual stotra page from URL"""
    try:
        page_html = get_page(url)
        psoup = BeautifulSoup(page_html, "html.parser")

        # title
        h1 = psoup.find("h1")
        page_title = clean_html_entities(h1.get_text(strip=True)) if h1 else clean_html_entities(title)

        # content container (robust fallback)
        content = (psoup.select_one("div.entry-content") or 
                   psoup.select_one("article .entry-content") or
                   psoup.find("pre") or 
                   psoup.select_one("article") or
                   psoup.select_one("div.content") or
                   psoup.body)

        content_html = content.decode_contents() if content else ""
        # Clean HTML entities from content
        content_html = clean_html_entities(content_html)
        
        # a simple first paragraph for meta
        first_para = ""
        for p in BeautifulSoup(content_html, "html.parser").find_all(["p","div","li"], limit=1):
            first_para = str(p)
            break

        meta_description = build_meta_description(page_title, first_para)
        filename = to_filename(page_title, suffix="-english.php")

        # Build breadcrumb with deity category if available
        breadcrumb_links = f'''<li><a href="<?php echo $base_url; ?>/index.php">Home</a></li>
                <li><a href="<?php echo $base_url; ?>/en/" title="Stotras in English">Stotras in English</a></li>'''
        
        if deity_category:
            deity_slug = deity_to_slug(deity_category)
            breadcrumb_links += f'''
                <li><a href="<?php echo $base_url; ?>/en/{deity_slug}-stotras">{deity_category} Stotras</a></li>'''
        
        breadcrumb_links += f'''
                <li>{page_title}</li>'''

        php_page = f"""<?php
// Meta Tags
$meta_title = "{page_title} in English - ClickVedicAstro";
$meta_description = "{meta_description}";
$meta_keywords = "{page_title}, English Stotras, Devotional Hymns, Hindu Slokas, ClickVedicAstro"; 
$meta_url = "https://www.clickvedicastro.com/en/{filename}";

// Include Header (session_start is already here)
include "../includes/header.php";
?>

<main id="content" role="main" class="main-content pt-0 pb-0">
<!-- breadcrumb -->
<div class="page-breadcrumb bg-white py-0">
    <div class="container">
        <div class="my-3">
            <ul class="list">
                {breadcrumb_links}
            </ul>
        </div>
    </div>
</div>

    <!-- Ad Promotion Template: For my Website -->
    <div class="adpromotion mt-5">
    <?php include "../includes/ad-promotion2.php"; ?>
    </div>

<section class="devotional-content pt-5">
<div class="container">
    <?php include "../includes/language-table-birth.php"; ?><!-- Language Birth Template-->
    <h1 class="stotra-title">{page_title}</h1>

    <article class="stotra-content">
      {content_html}
    </article>
    
    <!-- Ad Promotion Template: For my Website -->
    <div class="promo mt-5 mb-5">
        <?php include "../includes/promo1-devotional.php"; ?>
    </div>
</div>
</section>
</main>

<?php include "../includes/footer.php"; ?>
"""

        with open(os.path.join(OUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(php_page)

        return filename, page_title
        
    except Exception as e:
        print(f"❌ Error creating page for {title}: {e}")
        return None, None

# Create individual pages for ALL stotras found
print("🔄 Creating individual stotra pages...")
created_pages = []

# Process ALL stotras, not just a sample
total_stotras = len(filtered)
print(f"📋 Found {total_stotras} stotras to process...")

for i, (text, url) in enumerate(filtered, 1):
    print(f"🔄 Processing {i}/{total_stotras}: {text}")
    deity_category = deity_bucket_from_href(url)
    filename, page_title = create_stotra_page(text, url, deity_category)
    
    if filename:
        created_pages.append((filename, page_title, url))
        print(f"✅ Created: {filename}")
    else:
        print(f"❌ Failed to create page for: {text}")
    
    # Be respectful to the server - small delay between requests
    time.sleep(0.3)

print(f"📊 Total pages created: {len(created_pages)}")

# ---------- 3) Build English category index and deity-specific pages ----------
# Build smart buckets by deity (from URL tokens)
buckets = {}
for text, url in filtered:
    bucket = deity_bucket_from_href(url)
    buckets.setdefault(bucket, []).append((text or url.split("/")[-1].replace(".html",""), url))

# Build mapping from URL to actual created filename
url_to_filename = {}
for filename, page_title, url in created_pages:
    url_to_filename[url] = filename.replace('.php', '')  # Remove .php for clean URLs

def href_to_local(url):
    # Use actual created filename if available, otherwise fallback
    if url in url_to_filename:
        return url_to_filename[url]
    # fallback for any missed URLs
    last = url.split("/")[-1].replace(".html","")
    slug = re.sub(r"[^a-z0-9-]+", "-", last.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return f"{slug}-english"

# Create individual deity category pages
deity_pages_created = []
for bucket in sorted(buckets.keys()):
    if not buckets[bucket]:  # skip empty buckets
        continue
        
    deity_slug = deity_to_slug(bucket)
    filename = f"{deity_slug}-stotras.php"
    
    # Build stotra list for this deity
    stotra_items = []
    for (text, url) in sorted(buckets[bucket], key=lambda x: x[0].lower()):
        clean_text = clean_html_entities(text)
        stotra_items.append(f'  <li><a href="{href_to_local(url)}">{clean_text}</a></li>')
    
    deity_php = f"""<?php
// Meta Tags
$meta_title = "{bucket} Stotras in English - ClickVedicAstro";
$meta_description = "Collection of {bucket} devotional stotras and slokas in English with meaning and lyrics.";
$meta_keywords = "{bucket} Stotras, English Stotras, {bucket} Slokas, Hindu Devotional Hymns"; 
$meta_url = "https://www.clickvedicastro.com/en/{filename}";

// Include Header
include "../includes/header.php";
?>

<main id="content" role="main" class="main-content pt-0 pb-0">
<!-- breadcrumb -->
<div class="page-breadcrumb bg-white py-0">
    <div class="container">
        <div class="my-3">
            <ul class="list">
                <li><a href="<?php echo $base_url; ?>/index.php">Home</a></li>
                <li><a href="<?php echo $base_url; ?>/en/" title="Stotras in English">Stotras in English</a></li>
                <li>{bucket} Stotras</li>
            </ul>
        </div>
    </div>
</div>

    <!-- Ad Promotion Template: For my Website -->
    <div class="mt-5 mb-5">
    <?php include "../includes/ad-promotion1.php"; ?>
    </div>

<section class="devotional-content pt-5">
<div class="container">
    <h1 class="category-title">{bucket} Stotras in English</h1>
    <p>Collection of {bucket} devotional stotras and slokas in English with meaning and lyrics.</p>

    <ul class="stotra-list">
{chr(10).join(stotra_items)}
    </ul>
</div>
</section>
</main>

<?php include "../includes/footer.php"; ?>
"""
    
    with open(os.path.join(OUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(deity_php)
    
    deity_pages_created.append((bucket, filename))
    print(f"✅ Wrote deity category: {filename}")

# Build main index page with links to deity categories
category_links = []
for bucket, filename in deity_pages_created:
    deity_slug = deity_to_slug(bucket)
    category_links.append(f'  <li><a href="{deity_slug}-stotras">{bucket} Stotras</a></li>')

main_index_php = f"""<?php
// Meta Tags
$meta_title = "English Stotras & Slokas - ClickVedicAstro";
$meta_description = "Collection of Hindu devotional stotras and slokas in English with meaning and lyrics.";
$meta_keywords = "English Stotras, Slokas, Hindu Devotional Hymns"; 
$meta_url = "https://www.clickvedicastro.com/en/";

// Include Header
include "../includes/header.php";
?>

<main id="content" role="main" class="main-content pt-0 pb-0">
<!-- breadcrumb -->
<div class="page-breadcrumb bg-white py-0">
    <div class="container">
        <div class="my-3">
            <ul class="list">
                <li><a href="<?php echo $base_url; ?>/index.php">Home</a></li>
                <li>Stotras in English</li>
            </ul>
        </div>
    </div>
</div>

    <!-- Ad Promotion Template: For my Website -->
    <div class="mt-5 mb-5">
    <?php include "../includes/ad-promotion1.php"; ?>
    </div>

<section class="devotional-content pt-5">
<div class="container">
    <h1 class="category-title">English Stotras & Slokas</h1>
    <p>Browse our collection of Hindu devotional stotras and slokas organized by deity categories.</p>

    <h2>Browse by Deity</h2>
    <ul class="category-list">
{chr(10).join(category_links)}
    </ul>
</div>
</section>
</main>

<?php include "../includes/footer.php"; ?>
"""

with open(os.path.join(OUT_DIR, "index.php"), "w", encoding="utf-8") as f:
    f.write(main_index_php)

print("✅ Wrote main category index: index.php")
