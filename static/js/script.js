// Theme Toggle Functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const body = document.body;
    
    // Check for saved theme preference or default to 'dark'
    const savedTheme = localStorage.getItem('theme') || 'dark';
    body.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Add animation class for smooth transition
            body.style.transition = 'all 0.3s ease';
            setTimeout(() => {
                body.style.transition = '';
            }, 300);
        });
    }
    
    function updateThemeIcon(theme) {
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
            } else {
                themeIcon.className = 'fas fa-moon';
            }
        }
    }
    
    // Service Card Click Handler
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('click', function() {
            const serviceId = this.getAttribute('data-service-id');
            if (serviceId) {
                window.location.href = `/service/${serviceId}`;
            }
        });
    });
    
    // File Input Handler for Admin Panel
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const display = this.parentElement.querySelector('.file-input-display');
            if (display) {
                if (this.files.length > 0) {
                    display.textContent = `Selected: ${this.files[0].name}`;
                } else {
                    display.textContent = 'Choose file...';
                }
            }
        });
    });
    
    // Account Type Toggle in Admin Form
    const accountTypeSelect = document.getElementById('account_type');
    if (accountTypeSelect) {
        accountTypeSelect.addEventListener('change', function() {
            updateAccountTypeUI(this.value);
        });
        
        // Initialize on page load
        updateAccountTypeUI(accountTypeSelect.value);
    }
    
    function updateAccountTypeUI(accountType) {
        const credentialsSection = document.getElementById('credentials-section');
        const cookiesSection = document.getElementById('cookies-section');
        const accountsTextarea = document.getElementById('accounts');
        const accountsLabel = document.getElementById('accounts-label');
        
        if (accountType === 'cookies') {
            if (credentialsSection) credentialsSection.style.display = 'none';
            if (cookiesSection) cookiesSection.style.display = 'block';
            if (accountsLabel) accountsLabel.textContent = 'Cookies Data';
            if (accountsTextarea) {
                accountsTextarea.placeholder = 'Enter cookies data, one per line...\nExample:\nsession_id=abc123; user_token=xyz789\nauth_cookie=def456; preference=premium';
            }
        } else {
            if (credentialsSection) credentialsSection.style.display = 'block';
            if (cookiesSection) cookiesSection.style.display = 'none';
            if (accountsLabel) accountsLabel.textContent = 'Accounts';
            if (accountsTextarea) {
                accountsTextarea.placeholder = 'Format: user|pass|expiry|additional OR email:pass\nOne account per line. All fields are optional.\nExample:\nuser@example.com|password123|2024-12-31|Premium\ntest@mail.com:pass456\njohn@example.com|mypass||Standard';
            }
        }
    }
    
    // Copy to Clipboard Functionality
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(function() {
                    // Show feedback
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    button.style.background = 'var(--success)';
                    
                    setTimeout(() => {
                        button.textContent = originalText;
                        button.style.background = '';
                    }, 2000);
                }).catch(function(err) {
                    console.error('Failed to copy text: ', err);
                });
            }
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.style.opacity = '0.7';
                submitButton.textContent = 'Processing...';
            }
        });
    });
});

// Service card hover effects
function addServiceCardEffects() {
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Initialize effects when DOM is loaded
document.addEventListener('DOMContentLoaded', addServiceCardEffects);

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.maxWidth = '300px';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}
