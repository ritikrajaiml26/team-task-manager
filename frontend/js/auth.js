// Auto-detect backend URL (works for both local and production)
const BASE_URL = window.location.origin;

async function submitLogin(role) {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  const errorEl = document.getElementById('auth-error');
  errorEl.textContent = '';

  if (!username || !password) {
    errorEl.textContent = 'Please enter username and password.';
    return;
  }

  try {
    const res = await fetch(`${BASE_URL}/api/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      if (errData.detail) throw new Error(errData.detail);
      
      // Extract field-level errors from DRF
      const errors = [];
      for (const key in errData) {
        if (Array.isArray(errData[key])) {
          errors.push(`${key}: ${errData[key][0]}`);
        }
      }
      throw new Error(errors.length > 0 ? errors.join(' | ') : 'Invalid credentials');
    }

    const data = await res.json();
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);

    const userRes = await fetch(`${BASE_URL}/api/users/me/`, {
      headers: { Authorization: 'Bearer ' + data.access }
    });
    const user = await userRes.json();

    if (role === 'Admin' && user.role !== 'Admin') {
      throw new Error('Admin credentials required');
    }
    if (role === 'Member' && user.role === 'Admin') {
      throw new Error('Please login through the admin portal');
    }

    window.location.href = role === 'Admin' ? 'admin-dashboard.html' : 'dashboard.html';
  } catch (error) {
    errorEl.textContent = error.message;
  }
}

async function submitRegister(role) {
  const fullName = document.getElementById('full_name').value.trim();
  const username = document.getElementById('username').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const errorEl = document.getElementById('auth-error');
  errorEl.textContent = '';

  if (!fullName || !username || !email || !password) {
    errorEl.textContent = 'All fields are required.';
    return;
  }

  try {
    const res = await fetch(`${BASE_URL}/api/users/signup/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        email,
        password,
        first_name: fullName,
        role: role
      })
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      if (errData.detail) throw new Error(errData.detail);
      
      // Extract field-level errors from DRF
      const errors = [];
      for (const key in errData) {
        if (Array.isArray(errData[key])) {
          errors.push(`${key}: ${errData[key][0]}`);
        }
      }
      throw new Error(errors.length > 0 ? errors.join(' | ') : 'Registration failed');
    }

    window.location.href = role === 'Admin' ? 'admin-login.html' : 'login.html';
  } catch (error) {
    errorEl.textContent = error.message;
  }
}
