// Mobile Meals Center - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add to cart functionality
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Adding...';
            submitBtn.disabled = true;
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    // Show success message
                    showToast('Item added to cart!', 'success');
                    updateCartBadge();
                } else {
                    showToast('Error adding item to cart', 'error');
                }
            })
            .catch(error => {
                showToast('Error adding item to cart', 'error');
            })
            .finally(() => {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            });
        });
    });

    // Search form enhancements
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="q"]');
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 3) {
                    // Implement live search suggestions here
                    console.log('Searching for:', this.value);
                }
            }, 300);
        });
    }

    // Price range filter
    const priceRangeInputs = document.querySelectorAll('input[name="min_price"], input[name="max_price"]');
    priceRangeInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Auto-submit form when price range changes
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Geolocation for nearby restaurants
    const locationBtn = document.querySelector('#get-location-btn');
    if (locationBtn) {
        locationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                this.innerHTML = '<i class="bi bi-hourglass-split me-1"></i>Getting location...';
                this.disabled = true;
                
                navigator.geolocation.getCurrentPosition(
                    position => {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        
                        // Update hidden form fields or redirect with location params
                        window.location.href = `${window.location.pathname}?lat=${lat}&lng=${lng}`;
                    },
                    error => {
                        showToast('Unable to get your location', 'error');
                        this.innerHTML = '<i class="bi bi-geo-alt me-1"></i>Use My Location';
                        this.disabled = false;
                    }
                );
            } else {
                showToast('Geolocation is not supported by this browser', 'error');
            }
        });
    }

    // Order status updates (for restaurant dashboard)
    const statusForms = document.querySelectorAll('.status-update-form');
    statusForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitBtn = form.querySelector('button[type="submit"]');
            
            submitBtn.disabled = true;
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (response.ok) {
                    showToast('Order status updated!', 'success');
                    // Reload page to show updated status
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showToast('Error updating order status', 'error');
                }
            })
            .catch(error => {
                showToast('Error updating order status', 'error');
            })
            .finally(() => {
                submitBtn.disabled = false;
            });
        });
    });
});

// Utility functions
function showToast(message, type = 'info') {
    // Create toast element
    const toastHtml = `
        <div class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    // Add to toast container
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    // Initialize and show toast
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove element after hiding
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function updateCartBadge() {
    // Update cart badge count (if implemented)
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        // Fetch cart count from server or session storage
        fetch('/orders/cart-count/')
            .then(response => response.json())
            .then(data => {
                cartBadge.textContent = data.count;
                cartBadge.style.display = data.count > 0 ? 'flex' : 'none';
            })
            .catch(error => console.log('Error updating cart badge:', error));
    }
}

// Animation on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.fade-in-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    });
    
    elements.forEach(el => observer.observe(el));
}

// Initialize animations
document.addEventListener('DOMContentLoaded', animateOnScroll);
