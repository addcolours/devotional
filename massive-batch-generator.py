#!/usr/bin/env python3
"""
MASSIVE BATCH GENERATOR - Process 100+ files in under 1 minute!
All links from 7 categories: Shirdi Sai, Shiva, Subrahmanya, Surya, Suktam, Vishnu, Saraswati
"""

import os
from pathlib import Path

# The perfect template
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

def get_category_info(filename):
    """Smart category detection"""
    filename_lower = filename.lower()
    
    if 'sai' in filename_lower:
        return 'shirdi-sai-baba', 'Shirdi Sai Baba'
    elif 'shiva' in filename_lower:
        return 'shiva-stotras', 'Shiva Stotras'
    elif 'subrahmanya' in filename_lower or 'kartikeya' in filename_lower:
        return 'subrahmanya-stotras', 'Subrahmanya Stotras'
    elif 'surya' in filename_lower or 'aditya' in filename_lower:
        return 'surya-bhagawan', 'Surya Bhagawan'
    elif 'suktam' in filename_lower:
        return 'suktam-stotras', 'Suktam Stotras'
    elif 'vishnu' in filename_lower:
        return 'vishnu-stotras', 'Vishnu Stotras'
    elif 'saraswati' in filename_lower or 'sarasvati' in filename_lower:
        return 'saraswati-stotras', 'Saraswati Stotras'
    else:
        return 'others-stotras', 'Others Stotras'

def create_page(filename):
    """Create a single page with perfect template"""
    # Clean filename
    clean_filename = filename.replace('http://localhost/devotional/output_pages/en/', '').replace('.php', '')
    
    # Generate title and keywords
    title = clean_filename.replace('-english', '').replace('-', ' ').title()
    keywords = clean_filename.replace('-english', '').replace('-', ', ')
    
    # Get category
    category, category_title = get_category_info(clean_filename)
    
    # Generate content
    content = TEMPLATE.format(
        title=title,
        keywords=keywords,
        filename=clean_filename,
        category=category,
        category_title=category_title
    )
    
    # Write file
    output_dir = Path("output_pages/en")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = output_dir / f"{clean_filename}.php"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return clean_filename

def process_massive_list(file_list):
    """Process 100+ files in seconds"""
    print(f"🚀 MASSIVE BATCH PROCESSING: {len(file_list)} files")
    print("=" * 70)
    
    processed = 0
    for i, filename in enumerate(file_list, 1):
        try:
            result = create_page(filename)
            processed += 1
            
            # Show progress every 20 files
            if i % 20 == 0:
                print(f"⚡ Processed {i}/{len(file_list)} files... ({processed} successful)")
                
        except Exception as e:
            print(f"❌ Error with {filename}: {e}")
    
    print("=" * 70)
    print(f"🎉 COMPLETED: {processed}/{len(file_list)} files processed successfully!")
    print("⚡ All files created with perfect template structure!")
    
    return processed

# MASSIVE BATCH - All links from 7 categories (Total: 112 files)
if __name__ == "__main__":
    massive_file_list = [
        # Shirdi Sai Baba (5 files)
        "http://localhost/devotional/output_pages/en/sai-baba-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/shiridi-sai-baba-afternoon-aarati-madhyahna-aarati-english",
        "http://localhost/devotional/output_pages/en/shiridi-sai-baba-evening-aarati-dhoop-aarati-english",
        "http://localhost/devotional/output_pages/en/shiridi-sai-baba-morning-aarati-kakada-aarati-english",
        "http://localhost/devotional/output_pages/en/shiridi-sai-baba-night-aarati-shej-aarati-english",
        
        # Shiva Stotras (29 files)
        "http://localhost/devotional/output_pages/en/carnatic-music-svarajathi-2-samba-shiva-english",
        "http://localhost/devotional/output_pages/en/daridrya-dahana-shiva-stotram-english",
        "http://localhost/devotional/output_pages/en/shivananda-lahari-english",
        "http://localhost/devotional/output_pages/en/shivashtakam-english",
        "http://localhost/devotional/output_pages/en/shiva-aparadha-kshamapana-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/shiva-ashtottara-sata-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-bhujanga-prayata-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-bhujanga-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-kavacham-english",
        "http://localhost/devotional/output_pages/en/shiva-keshadi-padanta-varnana-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-mahimna-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-manasa-puja-english",
        "http://localhost/devotional/output_pages/en/shiva-mangalaashtakam-english",
        "http://localhost/devotional/output_pages/en/shiva-namavalyashtakam-namavali-ashtakam-english",
        "http://localhost/devotional/output_pages/en/shiva-padadi-keshanta-varnana-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-panchakshari-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-panchamruta-snanam-english",
        "http://localhost/devotional/output_pages/en/shiva-sahasra-namavali-english",
        "http://localhost/devotional/output_pages/en/shiva-sahasra-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-sankalpa-upanishad-shiva-sankalpamastu-english",
        "http://localhost/devotional/output_pages/en/shiva-shadakshari-stotram-english",
        "http://localhost/devotional/output_pages/en/shiva-tandava-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-samba-sadashiva-aksharamala-stotram-matruka-varnamalika-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-shiva-aarati-english",
        "http://localhost/devotional/output_pages/en/sri-shiva-chalisa-english",
        "http://localhost/devotional/output_pages/en/sri-shiva-dandakam-telugu-english",
        "http://localhost/devotional/output_pages/en/yama-kruta-shiva-keshava-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/yama-kruta-shiva-keshava-stotram-english",
        
        # Subrahmanya Stotras (17 files)
        "http://localhost/devotional/output_pages/en/kartikeya-pragna-vivardhana-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-kartikeya-karavalamba-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-subrahmanya-hrudaya-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-subrahmanya-kavacha-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-subrahmanya-sahasra-namavali-english",
        "http://localhost/devotional/output_pages/en/sri-subrahmanya-sahasra-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-subrahmanya-trishati-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-aparadha-kshamapana-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-ashtakam-karavalamba-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-ashtottara-sata-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-bhujanga-prayata-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-bhujanga-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-pancha-ratna-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-shatpadi-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-stotram-english",
        "http://localhost/devotional/output_pages/en/subrahmanya-vajra-panjara-stotram-english",
        
        # Surya Bhagawan (16 files)
        "http://localhost/devotional/output_pages/en/aditya-hrudayam-english",
        "http://localhost/devotional/output_pages/en/aditya-kavacham-english",
        "http://localhost/devotional/output_pages/en/dvadasha-aditya-dhyana-slokas-english",
        "http://localhost/devotional/output_pages/en/dwadasha-aditya-dhyana-slokas-english",
        "http://localhost/devotional/output_pages/en/sri-surya-namaskara-mantram-english",
        "http://localhost/devotional/output_pages/en/sri-surya-panjara-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-surya-shatakam-english",
        "http://localhost/devotional/output_pages/en/sri-surya-upanishad-english",
        "http://localhost/devotional/output_pages/en/surya-ashtottara-sata-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/surya-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/surya-kavacham-english",
        "http://localhost/devotional/output_pages/en/surya-mandala-stotram-english",
        "http://localhost/devotional/output_pages/en/surya-sahasra-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/surya-sahasra-namavali-english",
        "http://localhost/devotional/output_pages/en/surya-suktam-english",
        "http://localhost/devotional/output_pages/en/suryashtakam-english",
        
        # Suktam Stotras (20 files)
        "http://localhost/devotional/output_pages/en/aghamarshana-suktam-english",
        "http://localhost/devotional/output_pages/en/agni-suktam-rugveda-english",
        "http://localhost/devotional/output_pages/en/aikamatya-suktam-english",
        "http://localhost/devotional/output_pages/en/ayushya-suktam-english",
        "http://localhost/devotional/output_pages/en/bhagya-suktam-english",
        "http://localhost/devotional/output_pages/en/bhu-suktam-english",
        "http://localhost/devotional/output_pages/en/devi-mahatmyam-devi-suktam-english",
        "http://localhost/devotional/output_pages/en/durva-suktam-mahanarayana-upanishad-english",
        "http://localhost/devotional/output_pages/en/go-suktam-english",
        "http://localhost/devotional/output_pages/en/hiranya-garbha-suktam-english",
        "http://localhost/devotional/output_pages/en/krimi-samharaka-suktam-yajurveda-english",
        "http://localhost/devotional/output_pages/en/manyu-suktam-english",
        "http://localhost/devotional/output_pages/en/medha-suktam-english",
        "http://localhost/devotional/output_pages/en/mrittika-suktam-mahanarayana-upanishad-english",
        "http://localhost/devotional/output_pages/en/narayana-suktam-english",
        "http://localhost/devotional/output_pages/en/nila-suktam-english",
        "http://localhost/devotional/output_pages/en/purusha-suktam-english",
        "http://localhost/devotional/output_pages/en/saraswati-suktam-english",
        "http://localhost/devotional/output_pages/en/sri-ganesha-ganapati-suktam-english",
        "http://localhost/devotional/output_pages/en/vishnu-suktam-english",
        
        # Vishnu Stotras (13 files)
        "http://localhost/devotional/output_pages/en/kyts-52-vishnumukhaa-vai-devaah-krishna-yajurveda-taittiriya-samhita-patha-english",
        "http://localhost/devotional/output_pages/en/kyts-jata-52-vishnumukhaa-vai-devaah-krishna-yajurveda-taittiriya-samhita-english",
        "http://localhost/devotional/output_pages/en/maha-vishnu-stotram-garudagamana-tava-english",
        "http://localhost/devotional/output_pages/en/sree-vishnu-sahasra-namavali-english",
        "http://localhost/devotional/output_pages/en/sree-vishnu-sahasra-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-vishnu-ashtottara-sata-naama-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-vishnu-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/sri-vishnu-panjara-stotram-english",
        "http://localhost/devotional/output_pages/en/sri-vishnu-sata-namavali-vishnu-purana-english",
        "http://localhost/devotional/output_pages/en/sri-vishnu-sata-nama-stotram-vishnu-purana-english",
        "http://localhost/devotional/output_pages/en/vishnu-padadi-keshanta-varnana-stotram-english",
        "http://localhost/devotional/output_pages/en/vishnu-shatpadi-english",
        "http://localhost/devotional/output_pages/en/vishnu-suktam-english",
        
        # Saraswati Stotras (12 files)
        "http://localhost/devotional/output_pages/en/maha-sarasvati-stavam-english",
        "http://localhost/devotional/output_pages/en/sarasvati-kavacham-english",
        "http://localhost/devotional/output_pages/en/sarasvati-sahasra-namavali-english",
        "http://localhost/devotional/output_pages/en/sarasvati-sahasra-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/saraswati-ashtottara-sata-namavali-english",
        "http://localhost/devotional/output_pages/en/saraswati-ashtottara-sata-nama-stotram-english",
        "http://localhost/devotional/output_pages/en/saraswati-prarthana-ghanapatham-english",
        "http://localhost/devotional/output_pages/en/saraswati-stavam-english",
        "http://localhost/devotional/output_pages/en/saraswati-stotram-english",
        "http://localhost/devotional/output_pages/en/saraswati-stotram-yagnavalkya-krutam-english",
        "http://localhost/devotional/output_pages/en/saraswati-suktam-english",
        "http://localhost/devotional/output_pages/en/sree-saraswati-ashtottara-sata-nama-stotram-english"
    ]
    
    print("🔥 MASSIVE BATCH GENERATOR")
    print("=" * 70)
    print("Processing 112 files from 7 categories!")
    print("Categories: Shirdi Sai, Shiva, Subrahmanya, Surya, Suktam, Vishnu, Saraswati")
    print("=" * 70)
    
    process_massive_list(massive_file_list)
