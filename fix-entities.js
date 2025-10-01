// Fix HTML entities in stotra links
document.addEventListener('DOMContentLoaded', function() {
    // Find all stotra list links
    const stotraLinks = document.querySelectorAll('.stotra-list a');
    
    stotraLinks.forEach(function(link) {
        // Replace &nbsp; with regular spaces
        let text = link.innerHTML;
        text = text.replace(/&nbsp;/g, ' ');
        text = text.replace(/&amp;/g, '&');
        text = text.replace(/&lt;/g, '<');
        text = text.replace(/&gt;/g, '>');
        text = text.replace(/&quot;/g, '"');
        text = text.replace(/&#39;/g, "'");
        
        // Clean up multiple spaces
        text = text.replace(/\s+/g, ' ').trim();
        
        link.innerHTML = text;
    });
    
    // Also fix any other content areas
    const contentAreas = document.querySelectorAll('.stotra-content, .stotra-title');
    contentAreas.forEach(function(element) {
        let text = element.innerHTML;
        text = text.replace(/&nbsp;/g, ' ');
        text = text.replace(/&amp;/g, '&');
        text = text.replace(/&lt;/g, '<');
        text = text.replace(/&gt;/g, '>');
        text = text.replace(/&quot;/g, '"');
        text = text.replace(/&#39;/g, "'");
        
        // Clean up multiple spaces
        text = text.replace(/\s+/g, ' ').trim();
        
        element.innerHTML = text;
    });
});
