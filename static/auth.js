// Authentication JavaScript

// Signup Form Handler
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.style.display = 'none';
        
        const formData = {
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            newsletter: document.getElementById('newsletter').checked,
            terms: document.getElementById('terms').checked
        };
        
        // Validate terms
        if (!formData.terms) {
            showError('Please agree to the Terms of Service');
            return;
        }
        
        try {
            const response = await fetch('/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redirect to main application
                window.location.href = '/';
            } else {
                showError(result.error || 'Signup failed. Please try again.');
            }
        } catch (error) {
            console.error('Signup error:', error);
            showError('Network error. Please try again.');
        }
    });
}

// Login Form Handler
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.style.display = 'none';
        
        const formData = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Redirect to main application
                window.location.href = '/';
            } else {
                showError(result.error || 'Login failed. Please try again.');
            }
        } catch (error) {
            console.error('Login error:', error);
            showError('Network error. Please try again.');
        }
    });
}

// Show error message
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

// Google Sign In (placeholder)
const googleButtons = document.querySelectorAll('.btn-google');
googleButtons.forEach(button => {
    button.addEventListener('click', () => {
        alert('Google Sign In would be implemented here with OAuth 2.0');
    });
});



