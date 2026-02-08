// ==================== PAGINATION & SEARCH ====================

let currentPage = 1;
const cardsPerPage = 6;

// Change page with smooth transitions
function changePage(direction) {
    currentPage += direction;
    
    const page1 = document.querySelectorAll('.page-1');
    const page2 = document.querySelectorAll('.page-2');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageIndicator = document.getElementById('pageIndicator');

    // Add fade effect
    const allCards = document.querySelectorAll('.event-card');
    allCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
    });

    setTimeout(() => {
        if (currentPage === 1) {
            page1.forEach(el => el.style.display = 'block');
            page2.forEach(el => el.style.display = 'none');
            prevBtn.disabled = true;
            nextBtn.disabled = false;
        } else {
            page1.forEach(el => el.style.display = 'none');
            page2.forEach(el => el.style.display = 'block');
            prevBtn.disabled = false;
            nextBtn.disabled = true;
        }

        // Animate visible cards
        const visibleCards = document.querySelectorAll('.event-card[style*="display: block"], .event-card:not([style*="display: none"])');
        visibleCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 200);
        });

        pageIndicator.innerText = `Page ${currentPage} of 2`;

        // Smooth scroll to top of events section
        const eventsContainer = document.getElementById('eventsContainer');
        if (eventsContainer) {
            eventsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }, 300);
}

// Enhanced search/filter function
function filterEvents() {
    let filter = document.getElementById('eventSearch').value.toUpperCase();
    let cards = document.getElementsByClassName('event-card');
    let visibleCount = 0;
    let noResults = document.getElementById('noResults');

    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].querySelector(".card-title").innerText;
        let location = cards[i].querySelector(".card-text").innerText;
        let category = cards[i].querySelector(".badge").innerText;
        
        // Search in title, location, and category
        let searchText = (title + " " + location + " " + category).toUpperCase();
        
        if (searchText.indexOf(filter) > -1) {
            cards[i].style.display = "";
            visibleCount++;
            // Fade in animation
            cards[i].style.animation = 'fadeIn 0.5s ease';
        } else {
            cards[i].style.display = "none";
        }
    }

    // Show/hide pagination when searching
    const paginationDiv = document.querySelector('.d-flex.justify-content-center.align-items-center.mt-4');
    if (filter.length > 0) {
        if (paginationDiv) paginationDiv.style.display = 'none';
        
        // Show "no results" message
        if (visibleCount === 0) {
            if (!noResults) {
                noResults = document.createElement('div');
                noResults.id = 'noResults';
                noResults.className = 'col-12 text-center py-5';
                noResults.innerHTML = `
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No events found</h4>
                    <p class="text-muted">Try searching with different keywords</p>
                `;
                document.getElementById('eventsContainer').appendChild(noResults);
            }
            noResults.style.display = 'block';
        } else {
            if (noResults) noResults.style.display = 'none';
        }
    } else {
        if (paginationDiv) paginationDiv.style.display = 'flex';
        if (noResults) noResults.style.display = 'none';
        // Reset to page 1 when search is cleared
        currentPage = 1;
        changePage(0);
    }
}

// ==================== SMOOTH SCROLL FEATURES ====================

// Scroll to top on page load
window.addEventListener('load', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Scroll to top when footer links are clicked
document.addEventListener('DOMContentLoaded', function() {
    const footerLinks = document.querySelectorAll('footer a');
    
    footerLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!shouldHandleFooterLinkClick(e, this)) return;
            e.preventDefault();
            smoothScrollToTopThenNavigate(this.href);
        });
    });

    // Add transition to event cards
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach(card => {
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    });
});

// ==================== SCROLL TO TOP BUTTON ====================

// Show/hide scroll to top button
window.onscroll = function() {
    const scrollBtn = document.getElementById("scrollBtn");
    if (scrollBtn) {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            scrollBtn.style.display = "block";
            scrollBtn.style.opacity = "1";
        } else {
            scrollBtn.style.opacity = "0";
            setTimeout(() => {
                scrollBtn.style.display = "none";
            }, 300);
        }
    }
};

// Scroll to top function
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ==================== SEARCH INPUT ENHANCEMENTS ====================

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('eventSearch');
    
    if (searchInput) {
        // Add search icon feedback
        searchInput.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = '#2563eb';
            } else {
                this.style.borderColor = '#e5e7eb';
            }
        });

        // Clear search on Escape key
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
                filterEvents();
                this.blur();
            }
        });
    }
});

function shouldHandleFooterLinkClick(event, link) {
    if (event.defaultPrevented) return false;
    if (event.button !== 0) return false;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return false;
    if (link.target && link.target !== '_self') return false;
    if (link.hostname !== window.location.hostname) return false;
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#')) return false;
    return true;
}

function smoothScrollToTopThenNavigate(href) {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion || window.scrollY === 0) {
        window.location.href = href;
        return;
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });

    const maxWaitMs = 800;
    const start = performance.now();

    function checkPosition() {
        if (window.scrollY <= 0 || performance.now() - start > maxWaitMs) {
            window.location.href = href;
            return;
        }
        requestAnimationFrame(checkPosition);
    }

    requestAnimationFrame(checkPosition);
}
