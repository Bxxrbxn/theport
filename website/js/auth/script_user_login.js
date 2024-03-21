document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Basic validation
        if (!email || !password) {
            alert('Please fill in both email and password');
            return;
        }

        // Prepare data to be sent
        const data = {
            email: email,
            password: password
        };

        // Replace 'your_login_endpoint' with the actual endpoint
        fetch('your_login_endpoint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle login success
                // Redirect or show success message
                window.location.href = 'success_page_url'; // Replace with actual success page URL
            } else {
                // Handle login failure
                alert('Login failed: ' + data.message); // Show error message from server
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Login failed: An error occurred. Please try again later.');
        });
    });
});