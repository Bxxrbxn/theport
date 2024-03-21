document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');
    const btnSubmit = document.getElementById('btn-submit');
    const emailInput = document.getElementById('email');
    const btnEmailCheck = document.getElementById('btn-email');

    btnEmailCheck.addEventListener('click', function() {
        const email = emailInput.value;
        fetch('/api/check-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({email: email}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.isAvailable) {
                alert('This email is available.');
            } else {
                alert('This email is already in use.');
                emailInput.focus();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });

    btnSubmit.addEventListener('click', function(e) {
        e.preventDefault();
        if (validateForm()) {
            const formData = new FormData(registrationForm);
            fetch('/api/register', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Registration successful.');
                    window.location.href = '/login';
                } else {
                    alert('Registration failed: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
        }
    });

    function validateForm() {
        // Implement form validation logic here
        // Check for empty fields, password match, etc.
        // Return true if validation passes, false otherwise
        // This is just a placeholder, implement actual validation logic
        return true;
    }
});