// Main JavaScript file for Student Performance Analyzer

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.classList.add('fade-in');
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Password strength meter
    const passwordInput = document.querySelector('input[type="password"]');
    if (passwordInput) {
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'progress mt-2';
        strengthMeter.style.height = '5px';
        
        const strengthBar = document.createElement('div');
        strengthBar.className = 'progress-bar';
        strengthBar.style.width = '0%';
        
        strengthMeter.appendChild(strengthBar);
        passwordInput.parentNode.appendChild(strengthMeter);
        
        passwordInput.addEventListener('input', function() {
            const val = passwordInput.value;
            let strength = 0;
            
            if (val.length >= 6) strength += 20;
            if (val.length >= 8) strength += 20;
            if (val.match(/[a-z]+/)) strength += 20;
            if (val.match(/[A-Z]+/)) strength += 20;
            if (val.match(/[0-9]+/)) strength += 20;
            
            strengthBar.style.width = strength + '%';
            
            if (strength < 40) {
                strengthBar.className = 'progress-bar bg-danger';
            } else if (strength < 80) {
                strengthBar.className = 'progress-bar bg-warning';
            } else {
                strengthBar.className = 'progress-bar bg-success';
            }
        });
    }

    // Performance data form validation
    const performanceForm = document.querySelector('#performance-form');
    if (performanceForm) {
        const attendanceInput = document.querySelector('#attendance_percentage');
        const studyHoursInput = document.querySelector('#study_hours');
        const previousGradeInput = document.querySelector('#previous_grade');
        
        const validateNumericInput = function(input, min, max) {
            input.addEventListener('input', function() {
                const value = parseFloat(input.value);
                if (isNaN(value) || value < min || value > max) {
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                    input.classList.add('is-valid');
                }
            });
        };
        
        if (attendanceInput) validateNumericInput(attendanceInput, 0, 100);
        if (studyHoursInput) validateNumericInput(studyHoursInput, 0, 168);
        if (previousGradeInput) validateNumericInput(previousGradeInput, 0, 100);
    }

    // Confirmation for delete actions
    const deleteButtons = document.querySelectorAll('.delete-confirm');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
});
