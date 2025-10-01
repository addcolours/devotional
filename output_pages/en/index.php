<?php
// Meta Tags
$meta_title = "English Stotras & Slokas - ClickVedicAstro";
$meta_description = "Collection of Hindu devotional stotras and slokas in English with meaning and lyrics.";
$meta_keywords = "English Stotras, Slokas, Hindu Devotional Hymns"; 
$meta_url = "https://www.clickvedicastro.com/en/";

// Function to count entries in category files
function countCategoryEntries($categoryFile) {
    if (!file_exists($categoryFile)) {
        return 0;
    }
    
    $content = file_get_contents($categoryFile);
    if ($content === false) {
        return 0;
    }
    
    // Count the number of <li> tags with href attributes in the stotra-list
    preg_match_all('/<ul class="stotra-list">(.*?)<\/ul>/s', $content, $matches);
    if (empty($matches[1])) {
        return 0;
    }
    
    $listContent = $matches[1][0];
    preg_match_all('/<li><a href="[^"]*">[^<]*<\/a><\/li>/', $listContent, $liMatches);
    
    return count($liMatches[0]);
}

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
    <h1 class="category-title">Click Vedic Astro -English Stotras & Slokas</h1>
    <p>Browse our collection of Hindu devotional stotras and slokas organized by deity categories.</p>

    <h2>Browse by Deity</h2>
    <ul class="category-list">
    <li><a href="ayyappa-stotras">Ayyappa Swamy Stotras (<?php echo countCategoryEntries('ayyappa-stotras.php'); ?>)</a></li>
    <li><a href="dattatreya-stotras">Dattatreya Stotras (<?php echo countCategoryEntries('dattatreya-stotras.php'); ?>)</a></li>
    <li><a href="durga-stotras">Durga Stotras (<?php echo countCategoryEntries('durga-stotras.php'); ?>)</a></li>
    <li><a href="gayatri-stotras">Gayatri Stotras (<?php echo countCategoryEntries('gayatri-stotras.php'); ?>)</a></li>
    <li><a href="ganesha-stotras">Ganesha Stotras (<?php echo countCategoryEntries('ganesha-stotras.php'); ?>)</a></li>
    <li><a href="hanuman-stotras">Hanuman Stotras (<?php echo countCategoryEntries('hanuman-stotras.php'); ?>)</a></li>
    <li><a href="krishna-stotras">Krishna Stotras (<?php echo countCategoryEntries('krishna-stotras.php'); ?>)</a></li>
    <li><a href="lakshmi-stotras">Lakshmi Stotras (<?php echo countCategoryEntries('lakshmi-stotras.php'); ?>)</a></li>
    <li><a href="multiple-deities">Multiple Deities (<?php echo countCategoryEntries('multiple-deities.php'); ?>)</a></li>
    <li><a href="narasimha-stotras">Narasimha Swamy Stotras (<?php echo countCategoryEntries('narasimha-stotras.php'); ?>)</a></li>
    <li><a href="nava-graha-stotras">Nava Graha Stotras (<?php echo countCategoryEntries('nava-graha-stotras.php'); ?>)</a></li>
    <li><a href="others-stotras">Others Stotras (<?php echo countCategoryEntries('others-stotras.php'); ?>)</a></li>
    <li><a href="sahasranama-stotras">Sahasranama Stotras (<?php echo countCategoryEntries('sahasranama-stotras.php'); ?>)</a></li>
    <li><a href="saraswati-stotras">Saraswati Stotras (<?php echo countCategoryEntries('saraswati-stotras.php'); ?>)</a></li>
    <li><a href="shirdi-sai-baba">Shirdi Sai Baba (<?php echo countCategoryEntries('shirdi-sai-baba.php'); ?>)</a></li>
    <li><a href="shiva-stotras">Shiva Stotras (<?php echo countCategoryEntries('shiva-stotras.php'); ?>)</a></li>
    <li><a href="sri-venkateswara">Sri Venkateswara (<?php echo countCategoryEntries('sri-venkateswara.php'); ?>)</a></li>
    <li><a href="subrahmanya-stotras">Subrahmanya Stotras (<?php echo countCategoryEntries('subrahmanya-stotras.php'); ?>)</a></li>
    <li><a href="surya-bhagawan">Surya Bhagawan (<?php echo countCategoryEntries('surya-bhagawan.php'); ?>)</a></li>
    <li><a href="suktam-stotras">Suktam Stotras (<?php echo countCategoryEntries('suktam-stotras.php'); ?>)</a></li>
    <li><a href="suprabhatam-stotras">Suprabhatam Stotras (<?php echo countCategoryEntries('suprabhatam-stotras.php'); ?>)</a></li>
    <li><a href="vishnu-stotras">Vishnu Stotras (<?php echo countCategoryEntries('vishnu-stotras.php'); ?>)</a></li>
    </ul>
</div>
</section>
</main>

<?php include "../includes/footer.php"; ?>
