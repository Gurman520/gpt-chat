async function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&grant_type=password`
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            window.location.href = '/chat';
        } else {
            const error = await response.json();
            alert(`Login failed: ${error.detail}`);
        }
    } catch (error) {
        alert('Network error during login');
    }
}

async function register() {
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    
    if (password !== confirm) {
        alert('Passwords do not match');
        return;
    }

    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (response.ok) {
            alert('Registration successful! Please login.');
            showTab('login');
        } else {
            const error = await response.json();
            alert(`Registration failed: ${error.detail}`);
        }
    } catch (error) {
        alert('Network error during registration');
    }
}

function showTab(tabName) {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    
    document.getElementById(`${tabName}-form`).style.display = 'block';
    document.querySelector(`.tab[onclick="showTab('${tabName}')"]`).classList.add('active');
}