// Smart Recipe Finder - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Fade in animations
    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '1';
        }, index * 100);
    });

    // Handle favorite button clicks
    const favoriteButtons = document.querySelectorAll('.btn-favorite');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', handleFavoriteClick);
    });

    // Ingredient tag input enhancement
    const ingredientInput = document.getElementById('ingredientInput');
    if (ingredientInput) {
        setupIngredientInput(ingredientInput);
    }

    // Search form enhancement
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearchSubmit);
    }

    // Recipe card click handlers
    const recipeCards = document.querySelectorAll('.recipe-card');
    recipeCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.btn-favorite')) {
                const recipeId = this.dataset.recipeId;
                if (recipeId) {
                    window.location.href = `/recipe/${recipeId}`;
                }
            }
        });
    });
});

// Handle favorite button clicks
async function handleFavoriteClick(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const button = e.currentTarget;
    const recipeId = button.dataset.recipeId;
    const icon = button.querySelector('i');
    
    // Optimistic UI update
    const isFavorited = button.classList.contains('active');
    button.classList.toggle('active');
    icon.classList.toggle('bi-heart');
    icon.classList.toggle('bi-heart-fill');
    
    try {
        const response = await fetch(`/favorite/${recipeId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Revert on error
            button.classList.toggle('active');
            icon.classList.toggle('bi-heart');
            icon.classList.toggle('bi-heart-fill');
            showToast('Error', data.message || 'Failed to update favorite', 'danger');
        } else {
            const action = data.favorited ? 'added to' : 'removed from';
            showToast('Success', `Recipe ${action} favorites!`, 'success');
        }
    } catch (error) {
        // Revert on error
        button.classList.toggle('active');
        icon.classList.toggle('bi-heart');
        icon.classList.toggle('bi-heart-fill');
        showToast('Error', 'Network error occurred', 'danger');
    }
}

// Setup ingredient input with tag support
function setupIngredientInput(input) {
    const container = input.parentElement;
    const tagsContainer = document.createElement('div');
    tagsContainer.className = 'tags-container mt-2';
    container.appendChild(tagsContainer);
    
    const tags = [];
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' || e.key === ',') {
            e.preventDefault();
            const value = input.value.trim();
            if (value && !tags.includes(value)) {
                tags.push(value);
                renderTags();
                input.value = '';
            }
        }
    });
    
    function renderTags() {
        tagsContainer.innerHTML = '';
        tags.forEach((tag, index) => {
            const tagElement = document.createElement('span');
            tagElement.className = 'ingredient-tag';
            tagElement.innerHTML = `
                ${tag}
                <button type="button" class="btn-close btn-close-sm ms-1" 
                        onclick="removeTag(${index})"></button>
            `;
            tagsContainer.appendChild(tagElement);
        });
        
        // Update hidden input for form submission
        let hiddenInput = document.getElementById('ingredientTags');
        if (!hiddenInput) {
            hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.id = 'ingredientTags';
            hiddenInput.name = 'ingredients';
            container.appendChild(hiddenInput);
        }
        hiddenInput.value = tags.join(',');
    }
    
    // Make removeTag available globally
    window.removeTag = function(index) {
        tags.splice(index, 1);
        renderTags();
    };
}

// Handle search form submission
function handleSearchSubmit(e) {
    const submitButton = e.target.querySelector('button[type="submit"]');
    const buttonText = submitButton.innerHTML;
    
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="loading-spinner"></span> Searching...';
    
    // Form will submit normally, but we show loading state
    // The state will reset on page reload
}

// Show toast notification
function showToast(title, message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <strong>${title}</strong>: ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                    data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });
    bsToast.show();
    
    // Remove from DOM after hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Filter recipes by dietary preference
function filterRecipes(filter) {
    const recipeCards = document.querySelectorAll('.recipe-card');
    const filterPills = document.querySelectorAll('.filter-pill');
    
    // Update active pill
    filterPills.forEach(pill => {
        if (pill.dataset.filter === filter) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });
    
    // Filter cards
    recipeCards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
            card.style.display = 'block';
            card.classList.add('fade-in');
        } else {
            card.style.display = 'none';
        }
    });
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Print recipe
function printRecipe() {
    window.print();
}

// Share recipe
async function shareRecipe(title, url) {
    if (navigator.share) {
        try {
            await navigator.share({
                title: title,
                url: url
            });
        } catch (error) {
            if (error.name !== 'AbortError') {
                copyToClipboard(url);
                showToast('Link Copied', 'Recipe link copied to clipboard!', 'success');
            }
        }
    } else {
        copyToClipboard(url);
        showToast('Link Copied', 'Recipe link copied to clipboard!', 'success');
    }
}

// Copy text to clipboard
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

// Format cooking time
function formatCookingTime(minutes) {
    if (minutes < 60) {
        return `${minutes} mins`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
}

// Calculate match percentage color
function getMatchScoreClass(score) {
    if (score >= 80) return 'high';
    if (score >= 50) return 'medium';
    return 'low';
}

// Lazy load images
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Call lazy load on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', lazyLoadImages);
} else {
    lazyLoadImages();
}

// Export functions for global use
window.filterRecipes = filterRecipes;
window.scrollToSection = scrollToSection;
window.printRecipe = printRecipe;
window.shareRecipe = shareRecipe;
window.showToast = showToast;