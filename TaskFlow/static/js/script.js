// TaskFlow

document.addEventListener("DOMContentLoaded", function() {
    // Auto-hide alerts
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = "0";
                alert.style.transition = "opacity 0.5s";
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });


    // Form validation
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add("was-validated");
        });
    });


    // Minimum date for datetime inputs
    const dateInputs = document.querySelectorAll("input[type='datetime-local']");
    const now = new Date().toISOString().slice(0, 16);
    dateInputs.forEach(input => input.min = now);
});