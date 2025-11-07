// Custom JavaScript for SAU Lab Management System

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

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

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
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
