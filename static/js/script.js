// Add basic JS functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('nav a[href^="#"]');
    
    for (const link of links) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth'
                });

                // Update active state in sidebar
                document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
                this.parentElement.classList.add('active');
            }
        });
    }
});