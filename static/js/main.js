// Custom JavaScript for SAU Lab Management System

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Auto-hide flash messages after 4 seconds (in-page alerts stay visible)
    document.querySelectorAll('.flash-alert').forEach(autoHideAlert);

    // Confirm actions
    const confirmButtons = document.querySelectorAll('[onclick*="confirm"]');
    confirmButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('onclick').match(/confirm\('([^']+)'\)/);
            if (message && !confirm(message[1])) {
                e.preventDefault();
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('Please fill in all required fields.', 'danger');
            }
        });
    });

    // Real-time status updates
    if (window.location.pathname.includes('/dashboard')) {
        updateStatusCounts();
        setInterval(updateStatusCounts, 30000); // Update every 30 seconds
    }
});

const ALERT_HIDE_DELAY = 4000;
const ALERT_ICONS = { danger: 'circle-exclamation', success: 'circle-check', warning: 'triangle-exclamation', info: 'circle-info' };

function autoHideAlert(alert) {
    setTimeout(() => {
        if (document.body.contains(alert)) {
            bootstrap.Alert.getOrCreateInstance(alert).close();
        }
    }, ALERT_HIDE_DELAY);
}

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show flash-alert`;
    alertDiv.setAttribute('role', 'alert');
    const icon = document.createElement('i');
    icon.className = `fas fa-${ALERT_ICONS[type] || ALERT_ICONS.info} me-2`;
    alertDiv.appendChild(icon);
    alertDiv.appendChild(document.createTextNode(message));
    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'btn-close';
    closeBtn.setAttribute('data-bs-dismiss', 'alert');
    closeBtn.setAttribute('aria-label', 'Close');
    alertDiv.appendChild(closeBtn);

    const container = document.querySelector('.content .page-container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    autoHideAlert(alertDiv);
}

function updateStatusCounts() {
    // This would typically make an AJAX call to get updated counts
    // For now, we'll just refresh the page data
    console.log('Updating status counts...');
}

// Equipment booking confirmation
function confirmBooking(equipmentName) {
    return confirm(`Are you sure you want to book ${equipmentName}?`);
}

// Equipment return confirmation
function confirmReturn(equipmentName) {
    return confirm(`Are you sure you want to return ${equipmentName}?`);
}

// Search functionality
function searchEquipment() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const equipmentCards = document.querySelectorAll('.card');
    
    equipmentCards.forEach(card => {
        const equipmentName = card.querySelector('.card-title').textContent.toLowerCase();
        const equipmentType = card.querySelector('.card-text').textContent.toLowerCase();
        
        if (equipmentName.includes(searchTerm) || equipmentType.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Filter by status
function filterByStatus(status) {
    const equipmentCards = document.querySelectorAll('.card');
    
    equipmentCards.forEach(card => {
        const statusBadge = card.querySelector('.badge');
        if (status === 'all' || statusBadge.textContent.toLowerCase().includes(status)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
