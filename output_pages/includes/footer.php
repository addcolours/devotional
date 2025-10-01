<!--?php
// Get the base URL dynamically
$base_url = (isset($_SERVER['HTTPS']) ? "https" : "http") . "://" . $_SERVER['HTTP_HOST'] . "/chatgpt-prompts-build-astro-portal";
?-->


<?php
// Automatically detect live or local environment
$protocol = isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http";
$host = $_SERVER['HTTP_HOST'];
$folder = ""; // Keep empty if installed in root (public_html)

// If on localhost, define the folder manually
if ($host == "localhost") {
    $folder = "/build-clickvedicastro-portal"; // Change this if the folder name is different
}

// Construct Base URL
$base_url = $protocol . "://" . $host . $folder;
?> 
  
  <!-- call to action -->
  <section class="call-to-action py-5 py-lg-0">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-12 col-lg-3 offset-lg-1 d-flex justify-content-center">
          <img src="<?php echo $base_url; ?>/images/call-to-action.png" class="img-fluid" alt="call to action">
        </div>
        <div class="col-12 col-lg-7">
          <div class="action-bg text-center text-lg-start">
            <div class="h1 fw-bold mb-4 theme-text-accent-one">Let's talk about your question</div>
            <p class="h5 fw-bold theme-text-accent-two mb-0">With live astrologers - Ask Question get solutions</p>
            <div class="group mt-5">
                <a href="<?php echo $base_url; ?>/free-astrology/" class="rounded-pill btn btn-primary btn-lg primary-btn-effect" type="submit">Book Consultation</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  
 <!-- Footer Part -->
  <footer class="footer py-3">
    <div class="container">
      <div class="row">
        <div class="col-12 col-lg-6 offset-lg-3 text-center">
          <h3 class="mt-4 h5 fw-bold mb-3">Subscribe to our <span class="text-meroon">ClickVeidcAstro</span> Newsletter</h3>
          <form class="form-subcriber">
            <input type="email" placeholder="Your emaill address">
            <button class="btn-subscribe" type="submit"><i class="bi bi-envelope"></i></button>
          </form>
        </div>
      </div>
      
      <div class="row">
        <div class="col-12 col-md-3 col-lg-3">
          <h3 class="h5 fw-bold mb-4 mt-5 mt-lg-5">
              <a href="<?php echo $base_url; ?>index.php">
                <img src="<?php echo $base_url; ?>/images/click-vedic-astro-logo.svg" style="width:160px;" class="img-fluid" alt="Brand light">
              </a>
          </h3>
          <p class="mb-3 font-small pe-lg-5"><b>We are expert to give solution for all your problems.</b></p>
                <ul class="link-list">
                    <li><a href="<?php echo $base_url; ?>/about.php">About Us</a></li>
                    <!--li><a href="<?php echo $base_url; ?>/testimonials.php">Testimonials</a></li-->
                    <li><a href="<?php echo $base_url; ?>/faq.php">FAQ</a></li>
                    <!--li><a href="<?php echo $base_url; ?>/blog.php">Blog</a></li-->
                    <li><a href="<?php echo $base_url; ?>/sitemap.php">Sitemap</a></li>
                    <li><a href="<?php echo $base_url; ?>/contact-us.php">Contact Us</a></li>
                </ul>
                 
        </div>
        
        <div class="col-12 col-md-3 col-lg-3">
              <div class="row">
                <div class="col-12">
                  <h3 class="h5 fw-bold mb-2 mt-5">Our Services</h3>
                  <ul class="link-list">
				   <li><a href="<?php echo $base_url; ?>/free-astrology/newborn-horoscope.php">NewBorn Astrology</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Birth Chart Horoscope</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Kundali Matching Horoscope</a></li> 
                    <li><a href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Love Matching Horoscope</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Couple Horoscope</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/marriage-matching-compatibility.php">Marriage Matching Horoscope</a></li>
                    <li><a href="<?php echo $base_url; ?>pricing-plan.php">Carrer/Business Horoscope</a></li>              
                    <li><a href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Health Horoscope</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/date-of-birth-astrology-prediction.php">Education Horoscope</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Wealth Horoscope</a></li>  
                    <li><a href="<?php echo $base_url; ?>/free-horoscope/yearly-horoscope.php">2025 Horoscope</a></li>
                  </ul>                
                </div>
              </div>
        </div>

            <div class="col-12 col-md-3 col-lg-3">
                  <h3 class="h5 fw-bold mb-2 mt-5">Special Services</h3>
                   <ul class="link-list">
                    <li><a href="<?php echo $base_url; ?>/numerology/">Numerology</a></li>
                    <li><a href="<?php echo $base_url; ?>/numerology/">Birth Stones / GemStones</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-horoscope/yearly-horoscope.php">Panchang</a></li>
                    <li><a href="<?php echo $base_url; ?>/poojas-mantras/">Spirituality</a></li>
                    <li><a href="<?php echo $base_url; ?>/poojas-mantras/">Powerful Manthras</a></li>
                    <li><a href="<?php echo $base_url; ?>/poojas-mantras/">Festival Poojas</a></li>
                                        
                  </ul>
                  <h3 class="mt-4 h5 fw-bold">Terms, Policy & Refund</h3>             
                <ul class="link-list">
                    <li><a href="<?php echo $base_url; ?>/terms-and-conditions.php">Terms & Condition</a></li>
                    <li><a href="<?php echo $base_url; ?>/privacy-policy.php">Privacy Policy</a></li>
                    <li><a href="<?php echo $base_url; ?>/refund-cancellation-policy.php">Refund & Cancellation Policy</a></li>
					<li><a href="<?php echo $base_url; ?>/shipping-and-delivery-policy.php">Shipping and Delivery Policy</a></li>
                </ul>
                  
            </div>          
          
            <div class="col-12 col-md-3 col-lg-3">
              <h3 class="h5 fw-bold mb-4 mt-5 mt-md-0 mt-lg-5">Social Network</h3>
              <div class="d-flex social">
                <a href="javascript:void(0)" class="pe-2"><i class="bi bi-facebook"></i></a>
                <a href="javascript:void(0)" class="px-2"><i class="bi bi-twitter"></i></a>
                <a href="javascript:void(0)" class="px-2"><i class="bi bi-linkedin"></i></a>
                <a href="javascript:void(0)" class="px-2"><i class="bi bi-instagram"></i></a>
              </div>
                <h3 class="h5 fw-bold mb-2 mt-3">Languages</h3>
                   <ul class="link-list">
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Astrology in English</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Astrology in Hindi</a></li>
                    <li><a href="<?php echo $base_url; ?>/tamil-astrology/">Astrology in Tamil</a></li>    
                    <li><a href="<?php echo $base_url; ?>/telugu-astrology/">Astrology in Telugu</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Astrology in Malayalam</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Astrology in Kannada</a></li> 
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Astrology in Marathi</a></li>
                    <li><a href="<?php echo $base_url; ?>/free-astrology/">Astrology in Gujarati</a></li>                    
                  </ul>
            </div>
    
      </div>
      
      <div class="row mt-3 pt-3 border-top">
        <div class="col-12 col-md-12 text-center">
          <p class="pt-2 mb-0 font-extra-small">© Copyright 2025 by ClickVedicAstro.com, All rights reserved. 
            <a href="<?php echo $base_url; ?>/terms-and-conditions.php">Terms & Conditions</a> | 
            <a href="<?php echo $base_url; ?>/privacy-policy.php">Privacy Policy</a> | 
			<a href="<?php echo $base_url; ?>/shipping-and-delivery-policy.php">Shipping and Delivery Policy</a> 			
          </p>
        </div>
      </div>
    </div>
  </footer>
 

  <!-- back to top -->
  <a href="#wrapper" data-type="section-switch" class="scrollup"><i class="bi bi-caret-up"></i></a>

    <!-- All Scripts comes here -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
    <script src="<?php echo $base_url; ?>/js/bootstrap.bundle.min.js"></script>
    <script src="<?php echo $base_url; ?>/js/owl.carousel.min.js"></script>
    <script src="<?php echo $base_url; ?>/js/main.js"></script>

    <!-- Google tag (gtag.js) -->
    <!--script async src="https://www.googletagmanager.com/gtag/js?id=G-EMFN9V1H8P"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-EMFN9V1H8P');
    </script-->

    <!-- Google Ads -->
    <!--script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5004450060607590"
     crossorigin="anonymous"></script-->

<!-- ✅ Razorpay Script - Applied to All Pages -->


  </body>
</html>
