// ==================== PAGINATION & SEARCH ====================

let currentPage = 1;
const cardsPerPage = 6;
let statusFilter = 'all';
let categoryFilter = 'all';

// Change page with smooth transitions
function changePage(direction) {
    currentPage += direction;
    applyFilters(false);
}

// Enhanced search/filter function
function filterEvents() {
    currentPage = 1;
    applyFilters(false);
}

function setStatusFilter(filter) {
    statusFilter = filter;
    const buttons = document.querySelectorAll('.status-filter-btn');
    buttons.forEach(btn => {
        btn.classList.toggle('is-active', btn.dataset.filter === filter);
    });
    currentPage = 1;
    applyFilters(true);
}

function setCategoryFilter(category) {
    categoryFilter = category || 'all';
    currentPage = 1;
    applyFilters(true);
}

function applyFilters(shouldScroll) {
    const eventsContainer = document.getElementById('eventsContainer');
    if (!eventsContainer) return;
    let searchInput = document.getElementById('eventSearch');
    let filter = searchInput ? searchInput.value.toUpperCase() : '';
    const categorySelect = document.getElementById('eventCategory');
    if (categorySelect) categoryFilter = categorySelect.value || categoryFilter;
    let cards = document.getElementsByClassName('event-card');
    let filteredCards = [];
    let noResults = document.getElementById('noResults');
    const paginationDiv = document.querySelector('.d-flex.justify-content-center.align-items-center.mt-4');
    updateStatusCounts();

    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].querySelector(".card-title").innerText;
        let location = cards[i].querySelector(".card-text").innerText;
        let category = cards[i].dataset.category || '';
        let searchText = (title + " " + location + " " + category).toUpperCase();

        let statusMatch = true;
        if (statusFilter === 'upcoming') {
            statusMatch = cards[i].classList.contains('is-upcoming') || cards[i].classList.contains('is-soon');
        } else if (statusFilter === 'expired') {
            statusMatch = cards[i].classList.contains('is-expired');
        }

        let categoryMatch = true;
        if (categoryFilter !== 'all') {
            categoryMatch = category.trim().toLowerCase() === categoryFilter.trim().toLowerCase();
        }

        if (searchText.indexOf(filter) > -1 && statusMatch && categoryMatch) {
            filteredCards.push(cards[i]);
        }
    }

    // Pagination based on filtered list
    const totalPages = Math.max(1, Math.ceil(filteredCards.length / cardsPerPage));
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;
    const start = (currentPage - 1) * cardsPerPage;
    const end = start + cardsPerPage;

    // Hide all cards first
    for (let i = 0; i < cards.length; i++) {
        cards[i].style.display = "none";
    }

    // Add fade effect and show paginated cards
    filteredCards.forEach((card, index) => {
        if (index >= start && index < end) {
            card.style.display = "block";
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                card.style.animation = 'fadeIn 0.5s ease';
            }, 60);
        }
    });

    // Update pagination controls
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const pageIndicator = document.getElementById('pageIndicator');
    if (paginationDiv && prevBtn && nextBtn && pageIndicator) {
        if (totalPages <= 1) {
            paginationDiv.style.display = 'none';
        } else {
            paginationDiv.style.display = 'flex';
        }
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
        pageIndicator.innerText = `Page ${currentPage} of ${totalPages}`;
    }

    if (filteredCards.length === 0) {
        if (!noResults) {
            noResults = document.createElement('div');
            noResults.id = 'noResults';
            noResults.className = 'col-12 text-center py-5';
            noResults.innerHTML = `
                <i class="fas fa-search fa-3x text-muted mb-3"></i>
                <h4 class="text-muted">No events found</h4>
                <p class="text-muted">Try searching with different keywords</p>
            `;
            const container = document.getElementById('eventsContainer');
            if (container) container.appendChild(noResults);
        }
        noResults.style.display = 'block';
    } else {
        if (noResults) noResults.style.display = 'none';
    }

    if (shouldScroll && eventsContainer) {
        eventsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function updateStatusCounts() {
    const cards = document.getElementsByClassName('event-card');
    let upcoming = 0;
    let expired = 0;
    for (let i = 0; i < cards.length; i++) {
        if (cards[i].classList.contains('is-expired')) {
            expired++;
        } else if (cards[i].classList.contains('is-upcoming') || cards[i].classList.contains('is-soon')) {
            upcoming++;
        }
    }
    const all = cards.length;
    const allEl = document.querySelector('[data-count="all"]');
    const upcomingEl = document.querySelector('[data-count="upcoming"]');
    const expiredEl = document.querySelector('[data-count="expired"]');
    if (allEl) allEl.textContent = all;
    if (upcomingEl) upcomingEl.textContent = upcoming;
    if (expiredEl) expiredEl.textContent = expired;
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

    updateStatusCounts();
    applyFilters(false);
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
