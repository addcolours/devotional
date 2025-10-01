<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start(); // Start session if not already started
}

// Force UTF-8 output for every page
header('Content-Type: text/html; charset=UTF-8');

// Detect HTTP or HTTPS
$protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? "https" : "http";

// Get Hostname
$host = $_SERVER['HTTP_HOST'];

// Detect if running on localhost
$is_localhost = ($host == "localhost");

// Detect if running inside /devotional/ folder
$is_devotional= (strpos($_SERVER['REQUEST_URI'], '/devotional/') === 0);
$is_devotional = (strpos($_SERVER['REQUEST_URI'], '/devotional/') === 0);

// Define Dynamic Root Path for Localhost & Live
if (!defined('CUSTOM_ROOT_PATH')) {
    define('CUSTOM_ROOT_PATH', $is_localhost
        ? $_SERVER['DOCUMENT_ROOT'] . "/devotional/"
        : $_SERVER['DOCUMENT_ROOT'] . "/"
    );
}

// Define Base URL for Localhost & Live
if ($is_localhost) {
    $base_url = $protocol . "://" . $host . "/devotional";
} else {
    if ($is_devotional) {
        $base_url = "https://www.clickvedicastro.com/devotional/";
    } else {
        $base_url = "https://www.clickvedicastro.com";
    }
}

// Force correct base URL for devotional directory
if (strpos($_SERVER['REQUEST_URI'], '/devotional/') !== false) {
    $base_url = $protocol . "://" . $host . "/devotional";
}

// Additional fix: Force correct base URL for localhost devotional
if ($host == "localhost" && (strpos($_SERVER['REQUEST_URI'], '/devotional/') !== false || strpos($_SERVER['REQUEST_URI'], '/ver2/') !== false)) {
    $base_url = "http://localhost/devotional";
}

// Define Root Path for PHP Includes
if (!defined('ROOT_PATH')) {
    define("ROOT_PATH", $_SERVER['DOCUMENT_ROOT'] . ($is_localhost ? "/devotional" : ""));
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
 <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <!--
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  -->
  <!-- Start: Dynamic SEO Tags -->
  <title><?php echo isset($meta_title) ? $meta_title : "Free Birth Chart & Horoscope Online: AI-Powered Vedic Astrology"; ?></title>
 <meta name="description" content="<?php echo isset($meta_description) ? $meta_description : 'ClickVedicAstro: AI-powered free birth chart reports,Online Vedic astrology services, daily horoscope, marriage matching & predictions in Indian languages'; ?>">
  <meta name="keywords" content="<?php echo isset($meta_keywords) ? $meta_keywords : 'Vedic Astrology Prediction, Today Horoscope, astrology service, AI Astrology, ChatGpt Astrology, Kundli, Kundali Matching, Janma Kundali, Rashifal, rasi phalalu, numerology, zodiac signs, astrotalk, astro sage, click astro, palm reading, chinese astrology, vastu shastra'; ?>">
  <meta name="robots" content="index,follow" />
  
  <!-- Open Graph Meta Tags (For Social Sharing) -->
  <meta property="og:title" content="<?php echo isset($meta_title) ? $meta_title : 'ClickVedicAstro'; ?>" />
  <meta property="og:description" content="<?php echo isset($meta_description) ? $meta_description : 'Discover astrology insights and horoscope predictions at ClickVedicAstro.'; ?>" />
  <meta property="og:image" content="<?php echo isset($meta_image) ? $meta_image : 'https://www.clickvedicastro.com/images/online-free-kundli-birth-chart-report.jpg'; ?>" />
  <meta property="og:url" content="<?php echo isset($meta_url) ? $meta_url : 'https://www.clickvedicastro.com/devotional/'; ?>" />

  <!-- Twitter Meta Tags -->
  <meta name="twitter:title" content="<?php echo isset($meta_title) ? $meta_title : 'ClickVedicAstro'; ?>">
  <meta name="twitter:description" content="<?php echo isset($meta_description) ? $meta_description : 'Discover astrology insights and horoscope predictions at ClickVedicAstro.'; ?>">
  <meta name="twitter:image" content="<?php echo isset($meta_image) ? $meta_image : 'https://www.clickvedicastro.com/images/online-free-kundli-birth-chart-report.jpg'; ?>">
  <meta name="twitter:card" content="summary_large_image">
  <!-- End: Dynamic SEO Tags -->

  <meta name="author" content="ClickVedicAstro">
  <meta name="google-site-verification" content="oABMQeg-8FKpnHrrIoP8dF4uRWdB-UH2N0qEGYhtaqg" />
  <meta name="google-adsense-account" content="ca-pub-5004450060607590">


  <!-- Favicon icon -->
  <link rel="icon" type="image/png" sizes="16x16" href="<?php echo $base_url; ?>/images/favicon.png">
  <link rel="shortcut icon" type="image/x-icon" href="<?php echo $base_url; ?>/images/favicon.ico">

  <link href="<?php echo $base_url; ?>/css/bootstrap.min.css" rel="stylesheet">
  <link href="<?php echo $base_url; ?>/css/main.css" rel="stylesheet">
  <link href="/devotional/styles.css" rel="stylesheet">
  <link href="<?php echo $base_url; ?>/css/owl.carousel.min.css" rel="stylesheet">
  
	<!-- Google tag (gtag.js) -->
	<script async src="https://www.googletagmanager.com/gtag/js?id=G-EMFN9V1H8P"></script>
	<script>
	  window.dataLayer = window.dataLayer || [];
	  function gtag(){dataLayer.push(arguments);}
	  gtag('js', new Date());

	  gtag('config', 'G-EMFN9V1H8P');
	</script>
	
	<!-- Google tag (gtag.js) -->
	<script async src="https://www.googletagmanager.com/gtag/js?id=G-EMFN9V1H8P"></script>
	<script>
	  window.dataLayer = window.dataLayer || [];
	  function gtag(){dataLayer.push(arguments);}
	  gtag('js', new Date());

	  gtag('config', 'G-EMFN9V1H8P');
	</script>
	<!-- Google Ads -->
	<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5004450060607590"
 crossorigin="anonymous"></script>
 
 <?php if (isset($canonical)) : ?>
	<link rel="canonical" href="<?= htmlspecialchars($canonical); ?>" />
 <?php endif; ?>
</head>
 <!-- header top section -->
  <header class="header pg-blog border-bottom">
    <div class="header-wrap">
     <div class="container">
        <div class="row">
            <div class="col-12 text-center header-columns">
                <a href="<?php echo $base_url; ?>" class="brand">
                    <img src="<?php echo $base_url; ?>/images/click-vedic-astro-logo.svg" class="img-fluid logo-astro" alt="Brand Logo" title="Brand Logo">
                </a>
                <img src="<?php echo $base_url; ?>/images/shooting-star.gif" class="d-flex ms-2 d-none d-lg-block" style="margin:0 0px 0 0px; width:45px">
				
				<!-- Single HTML Code with Dropdown & Buttons -->
    <input type="checkbox" id="languageDropdown" class="d-lg-none" style="display: none;">
    <label for="languageDropdown" class="btn btn-secondary btn-sm d-lg-none dropdown-label text-lowercase" style="min-width: 95px;" id="toggleRotation">Language</label>

    <!-- Language Menu (Overlay in Mobile) -->
    <div class="ui-language ui-head-block-d gap-1 menu-list">
        <a href="<?php echo $base_url; ?>/free-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="English"><span class="min-screen">English</span></a>
		<a href="<?php echo $base_url; ?>/hindi-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Hindi"><span class="min-screen">हिंदी</span></a>
        <a href="<?php echo $base_url; ?>/telugu-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Telugu"><span class="min-screen">తెలుగు</span></a>
		<a href="<?php echo $base_url; ?>/tamil-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Tamil"><span class="min-screen">தமிழ்</span></a>
        <a href="<?php echo $base_url; ?>/kannada-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Kannada"><span class="min-screen">ಕನ್ನಡ</span></a>
		<a href="<?php echo $base_url; ?>/malayalam-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Malayalam"><span class="min-screen">മലയാളം</span></a>
        <a href="<?php echo $base_url; ?>/gujarati-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Gujarati"><span class="min-screen">ગુજરાતી</span></a>
        <a href="<?php echo $base_url; ?>/marathi-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Marathi"><span class="min-screen">मराठी</span></a>
        <a href="<?php echo $base_url; ?>/bengali-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Bengali"><span class="min-screen">বাংলা</span></a>       
        <a href="<?php echo $base_url; ?>/odisha-astrology/" class="btn btn-deep-orange br-radius card-shadow" title="Odia"><span class="min-screen">ଓଡ଼ିଆ</span></a>
		<!-- Close Button Inside Menu -->
        <button class="close-btn" onclick="closeMenu()">✕</button>
    </div>

                <div class="d-flex ms-2 d-none d-lg-block" style="/* margin-top: 20px; */ margin-left: auto !important;">
                    <!--a href="https://api.whatsapp.com/send?phone=918143800000&amp;text=Hello%20AstroPdf.com" target="_blank" class="rounded-pill btn btn-secondary font-small primary-btn-effect" style="margin-right:5px;"><i class="bi bi-whatsapp"></i> +91-9866858646</a-->
                    <img src="<?php echo $base_url; ?>/images/star.gif" width="35" style="margin:0 0px 0 0px;">
                    <a href="<?php echo $base_url; ?>/free-astrology/" class="rounded-pill btn btn-primary btn-sm font-small primary-btn-effect" type="submit">Consult Now <i class="bi bi-arrow-right-short btn-arrow"></i></a>
                </div>
            </div>
        </div>
      </div>
    </div>
        
    <!-- Header Part -->
    <div class="navbar navbar-expand-lg py-0 px-0">   
      <nav class="container">
       <div class="switch order-lg-1 ms-0 ms-lg-3">
          <div class="btn-wrapper">
            <button class="navbar-toggler theme-bg-secondary border-0 menu-toggle" type="button" data-label="Menu" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="icon-bars"></span>
            </button>
            <!--button onclick="window.location.href='appointment.php';" class="rounded-pill btn btn-primary font-small primary-btn-effect" type="submit">Consult Now <i class="bi bi-arrow-right-short btn-arrow"></i></button-->
          </div>
        </div> 
        
        <div class="collapse navbar-collapse" id="navbarSupportedContent">      
          <ul class="navbar-nav mb-lg-0">           
            <li class="nav-item dropdown">
              <a class="nav-link nav-effect dropdown-toggle" href="<?php echo $base_url; ?>/free-astrology/index.php" id="navbarDropdownPages" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">       
                <img src="<?php echo $base_url; ?>/images/new-label.gif"> Free Astrology</a>
              <ul class="dropdown-menu dropdown-menu-efct sub-menu-effect" aria-labelledby="navbarDropdownPages">
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Date of Birth Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Marriage Matching Compatibility</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-horoscope/yearly-horoscope.php">2025 Horoscope</a></li>
             
                <hr>

                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Vedic Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Janma Kundali Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Kundali Matching Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Love Matching Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Couple's Matching Astrology</a></li>
                <hr>      

                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/newborn-horoscope.php">NewBorn Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/">Health Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Carrer & Business Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Wealth Astrology</a></li>
                <li><a class="dropdown-item" href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Education Astrology</a></li>
               
                </ul>
            </li>

            <li class="nav-item dropdown">
              <a class="nav-link nav-effect dropdown-toggle" href="#" id="navbarDropdownPages" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">Birth Chart</a>
              <ul class="dropdown-menu dropdown-menu-efct sub-menu-effect" aria-labelledby="navbarDropdownPages">
                <li><a href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php" class="dropdown-item">English</a></li>
                <li><a href="<?php echo $base_url; ?>/hindi-astrology/free-janm-kundli-birth-chart.php" class="dropdown-item">Hindi</a></li>
				<li><a href="<?php echo $base_url; ?>/telugu-astrology/free-jathakam-predictions-horoscope-by-birth-date.php" class="dropdown-item">Telugu</a></li>
                <li><a href="<?php echo $base_url; ?>/tamil-astrology/free-jathagam-birth-chart.php" class="dropdown-item">Tamil</a></li>
				<li><a href="<?php echo $base_url; ?>/kannada-astrology/free-kannada-jataka.php" class="dropdown-item">Kannada</a></li>
				<li><a href="<?php echo $base_url; ?>/malayalam-astrology/free-malayalam-jathakam.php" class="dropdown-item">Malayalam</a></li>
                <li><a href="<?php echo $base_url; ?>/gujarati-astrology/free-gujarati-birth-chart.php" class="dropdown-item">Gujarati</a></li>  
                <li><a href="<?php echo $base_url; ?>/marathi-astrology/free-marathi-birth-chart.php" class="dropdown-item">Marathi</a></li>
                <li><a href="<?php echo $base_url; ?>/bengali-astrology/free-bengali-birth-chart.php" class="dropdown-item">Bengali</a></li>
				<li><a href="<?php echo $base_url; ?>/odisha-astrology/free-odia-birth-chart.php" class="dropdown-item">Odia</a></li> 
              </ul>
            </li>

            <li class="nav-item dropdown">
              <a class="nav-link nav-effect dropdown-toggle" href="#" id="navbarDropdownPages" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">Marriage Matching</a>
              <ul class="dropdown-menu dropdown-menu-efct sub-menu-effect" aria-labelledby="navbarDropdownPages">
                <li><a href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php" class="dropdown-item">English</a></li>
                <li><a href="<?php echo $base_url; ?>/hindi-astrology/marriage-matching.php" class="dropdown-item">Hindi</a></li>
				<li><a href="<?php echo $base_url; ?>/telugu-astrology/free-jataka-pontana-marriage-horoscope.php" class="dropdown-item">Telugu</a></li>
                <li><a href="<?php echo $base_url; ?>/tamil-astrology/marriage-matching.php" class="dropdown-item">Tamil</a></li>    
                <li><a href="<?php echo $base_url; ?>/kannada-astrology/marriage-matching.php" class="dropdown-item">Kannada</a></li> 
                <li><a href="<?php echo $base_url; ?>/malayalam-astrology/marriage-matching.php" class="dropdown-item">Malayalam</a></li>
                <li><a href="<?php echo $base_url; ?>/gujarati-astrology/marriage-matching.php" class="dropdown-item">Gujarati</a></li>  
                <li><a href="<?php echo $base_url; ?>/marathi-astrology/marriage-matching.php" class="dropdown-item">Marathi</a></li>
				 <li><a href="<?php echo $base_url; ?>/bengali-astrology/marriage-matching.php" class="dropdown-item">Bengali</a></li>
                <li><a href="<?php echo $base_url; ?>/odisha-astrology/marriage-matching.php" class="dropdown-item">Odia</a></li>
              </ul>
            </li>
            
             <li class="nav-item dropdown">
              <a class="nav-link nav-effect dropdown-toggle" href="#" id="navbarDropdownPages" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">Sample Reports</a>
              <ul class="dropdown-menu dropdown-menu-efct sub-menu-effect" aria-labelledby="navbarDropdownPages">
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-english.pdf" target="_blank" class="dropdown-item">in (English)</a></li>
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-tamil.pdf" target="_blank" class="dropdown-item">in (Tamil)</a></li> 
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-hindi.pdf" target="_blank" class="dropdown-item">in (Hindi)</a></li>                                 
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-telugu.pdf" target="_blank" class="dropdown-item">in (Telugu)</a></li>
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-malayalam.pdf" target="_blank" class="dropdown-item">in (Malayalam)</a></li>
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-kannada.pdf" target="_blank" class="dropdown-item">in (Kannada)</a></li> 
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-marathi.pdf" target="_blank" class="dropdown-item">in (Marathi)</a></li>
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-bangla.pdf" target="_blank" class="dropdown-item">in (Bangla)</a></li>
                <li><a href="<?php echo $base_url; ?>/horoscope-reports/birth-chart/click-vedic-astro-gujarati.pdf" target="_blank" class="dropdown-item">in (Gujarati)</a></li>    
              </ul>
            </li>
                                        
           <!-- Mega Menu 2 -->
           <!--<li class="nav-item dropdown megamenu-li">
            <a class="nav-link nav-effect dropdown-toggle" href="#" id="navbarDropdownShop" aria-haspopup="true" data-bs-toggle="dropdown" aria-expanded="false">Remedies</a>-->
            
            <!-- mega menu section -->
            <!--div class="dropdown-menu megamenu p-4" aria-labelledby="navbarDropdownShop">
              <div class="row">
                <div class="col-sm-6 col-lg-3 mb-3 mb-lg-0">
                  <h5 class="mb-3 fw-bold">Graha Dosham</h5>
                  <ul class="sub-menu-effect">  
                   <li><a href="<?php echo $base_url; ?>nivarana-dosha.php" class="dropdown-item">All Nivarana Dosha</a></li>
                    <li><a href="<?php echo $base_url; ?>nava-graha-shanti.php" class="dropdown-item">Nava Graha Dosha Shanti</a></li>
                    <li><a href="<?php echo $base_url; ?>kuja-graha-shanti.php" class="dropdown-item">Kuja Graha Shanti</a></li>    
                    <li><a href="<?php echo $base_url; ?>sani-graha-shanti.php" class="dropdown-item">Shani Graha Shanti</a></li>
                    <li><a href="<?php echo $base_url; ?>homas.php" class="dropdown-item">Homams (Sacrifice Ritual)</a></li>
                  </ul>
                </div>
                <div class="col-sm-6 col-lg-3 mb-3 mb-lg-0">
                  <h5 class="mb-3 fw-bold">Powerful Remedies</h5>
                  <ul class="sub-menu-effect">
                    <li><a href="poojas-manthras.php" class="dropdown-item">Poojas/Manthras</a></li>
                    <li><a href="<?php echo $base_url; ?>donate-spices-graha-shanti.php" class="dropdown-item">Donate Spices</a></li>
                    <li><a href="<?php echo $base_url; ?>vastu-shastra.php" class="dropdown-item">Vastu Shastra</a></li>
                    <li><a href="<?php echo $base_url; ?>hindu-temples.php" class="dropdown-item">Temples</a></li>
                    <li><a href="<?php echo $base_url; ?>festivals.php" class="dropdown-item">Festivals</a></li>
                  </ul>
                </div>
                <div class="col-sm-6 col-lg-3 mb-3 mb-lg-0">
                  <h5 class="mb-3 fw-bold">Tradational Remedies</h5>
                  <ul class="sub-menu-effect">
                  <li><a href="<?php echo $base_url; ?>numerology.php" class="dropdown-item">Numerology</a></li>
                    <li><a href="<?php echo $base_url; ?>birth-stones.php" class="dropdown-item">Birth Stones / GemStones</a></li>
                    <li><a href="<?php echo $base_url; ?>rudraksha.php" class="dropdown-item">Rudraksha</a></li>
                    <li><a href="<?php echo $base_url; ?>meditation-yoga-healing.php" class="dropdown-item">Meditation/Yoga</a></li>                    
                    <li><a href="<?php echo $base_url; ?>https://www.youtube.com/c/raliskitchen" target="_blank" class="dropdown-item">Healing with Food</a></li>
                  </ul>
                </div>
                <div class="col-sm-6 col-lg-3 mb-3 mb-lg-0">
                  <h5 class="mb-3 fw-bold">International Healings</h5>
                  <ul class="sub-menu-effect">
                   <li><a href="crystal-therapy.php" class="dropdown-item">Healing with Crystal Therapy</a></li>
                    <li><a href="<?php echo $base_url; ?>accupressure.php" class="dropdown-item">Healing with Accupressure Points</a></li>
                    <li><a href="<?php echo $base_url; ?>medical-astrology.php" class="dropdown-item">Medical Astrology</a></li>
                    <li><a href="<?php echo $base_url; ?>feng-shui.php" class="dropdown-item">Feng Shui</a></li>
                    <li><a href="<?php echo $base_url; ?>reik-healing.php" class="dropdown-item">Reik Healing</a></li>      
                  </ul>
                </div>
              </div>
            </div-->
            <!-- end mega menu section -->
          <!--/li-->
                   
            <li class="nav-item dropdown">
              <a class="nav-link nav-effect dropdown-toggle" href="#" id="navbarDropdownPages" data-bs-toggle="dropdown" aria-expanded="false" data-bs-auto-close="outside">2025</a>
              <ul class="dropdown-menu dropdown-menu-efct sub-menu-effect" aria-labelledby="navbarDropdownPages">
                <li><a href="<?php echo $base_url; ?>/free-horoscope/yearly-horoscope.php" class="dropdown-item">2025 Horoscope</a></li>
                <!--<li><a href="<?php echo $base_url; ?>shubh-muhurat.php" class="dropdown-item">Shubh Muhurat 2025</a></li>
                <li><a href="<?php echo $base_url; ?>holidays.php" class="dropdown-item">Holidays 2025</a></li>
                <li><a href="<?php echo $base_url; ?>calendar.php" class="dropdown-item">Calendar 2025</a></li>    
                <li><a href="<?php echo $base_url; ?>chinese-horoscope.php" class="dropdown-item">Chinese Horoscope 2025</a></li>           
                <li><a href="<?php echo $base_url; ?>tarot-reading.php" class="dropdown-item">Tarot Reading 2025</a></li>-->
                </ul>
            </li>

          </ul>                 
        </div>
        <div>   
            <a href="<?php echo $base_url; ?>/refund-cancellation-policy.php" class="moneyreturn" type="submit"><img src="<?php echo $base_url; ?>/images/money-return-policy.svg"> Money Refund?</a>
        </div>
      </nav>
    </div>
      </header>