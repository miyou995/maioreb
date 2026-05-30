// Professional Wagtail Website JavaScript

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');

    if (mobileMenuToggle && mainNav) {
        mobileMenuToggle.addEventListener('click', function () {
            mainNav.classList.toggle('active');

            // Update aria-expanded attribute
            const isExpanded = mainNav.classList.contains('active');
            mobileMenuToggle.setAttribute('aria-expanded', isExpanded);
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function (event) {
            if (!event.target.closest('.site-header')) {
                mainNav.classList.remove('active');
                mobileMenuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add scroll effect to header
    const header = document.querySelector('.site-header');
    if (header) {
        let lastScroll = 0;

        window.addEventListener('scroll', function () {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 100) {
                header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
            } else {
                header.style.boxShadow = '0 1px 2px 0 rgba(0, 0, 0, 0.05)';
            }

            lastScroll = currentScroll;
        });
    }

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#ef4444';
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Veuillez remplir tous les champs obligatoires.');
            }
        });
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and sections
    document.querySelectorAll('.card, .section-header').forEach(el => {
        observer.observe(el);
    });
});



htmx.on("messages", (event) => {
    // event.detail.value.forEach(createToast)
    $("#message_modal").modal("show");
});


document.addEventListener("DOMContentLoaded", function () {
    const banner = document.getElementById("cookieBanner");

    if (!banner) return;

    const acceptBtn = document.getElementById("acceptCookies");
    const rejectBtn = document.getElementById("rejectCookies");

    const consent = localStorage.getItem("cookie_consent");

    if (consent !== "accepted") {
        setTimeout(() => {
            banner.style.display = "block";
        }, 5000);
    }

    acceptBtn.addEventListener("click", function () {
        localStorage.setItem("cookie_consent", "accepted");
        banner.style.display = "none";
    });

    rejectBtn.addEventListener("click", function () {
        localStorage.setItem("cookie_consent", "rejected");
        banner.style.display = "none";
    });
});
