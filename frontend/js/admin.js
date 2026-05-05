// Ensure auth.js is loaded so BASE_URL is available
document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    window.location.href = 'admin-login.html';
    return;
  }
  
  // Basic token check and role verification
  fetch(`${BASE_URL}/api/users/me/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => {
    if (data.role !== 'Admin') {
      window.location.href = 'dashboard.html'; // redirect members
    } else {
      document.getElementById('admin-name').textContent = data.first_name || data.username;
      initAdminDashboard();
    }
  })
  .catch(() => {
    window.location.href = 'admin-login.html';
  });
});

function logout() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  window.location.href = 'admin-login.html';
}

function getHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  };
}

async function initAdminDashboard() {
  await fetchAdminData();
  await loadProjects();
  await loadUsers();
}

async function fetchAdminData() {
  try {
    const res = await fetch(`${BASE_URL}/api/tasks/admin-dashboard/`, { headers: getHeaders() });
    if (!res.ok) throw new Error("Failed to fetch dashboard data");
    
    const data = await res.json();
    
    // Update global metrics
    const summary = data.global_summary;
    document.getElementById('stat-total').textContent = summary.total_tasks;
    document.getElementById('stat-todo').textContent = summary.todo;
    document.getElementById('stat-progress').textContent = summary.in_progress;
    document.getElementById('stat-done').textContent = summary.done;
    document.getElementById('stat-overdue').textContent = summary.overdue;

    // Update users table
    const tbody = document.getElementById('users-tbody');
    tbody.innerHTML = '';
    
    data.users.forEach(u => {
      const tr = document.createElement('tr');
      const overdueBadge = u.overdue > 0 ? `<span class="badge bg-red">${u.overdue} Overdue</span>` : '0';
      
      tr.innerHTML = `
        <td>
          <div style="font-weight: 500">${u.name || u.username}</div>
          <div style="font-size: 0.8rem; color: var(--text-secondary)">${u.email}</div>
        </td>
        <td>${u.total_tasks}</td>
        <td>${u.todo}</td>
        <td>${u.in_progress}</td>
        <td>${u.done}</td>
        <td>${overdueBadge}</td>
        <td>
          <div style="background: #e2e8f0; height: 8px; border-radius: 4px; width: 100px; overflow: hidden; display: inline-block; vertical-align: middle;">
            <div style="background: var(--primary); height: 100%; width: ${u.progress}%"></div>
          </div>
          <span style="font-size: 0.8rem; margin-left: 0.5rem;">${u.progress}%</span>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    console.error(error);
  }
}

async function loadProjects() {
  try {
    const res = await fetch(`${BASE_URL}/api/projects/list/`, { headers: getHeaders() });
    const data = await res.json();
    const projects = data.results ? data.results : data;
    const select = document.getElementById('task-project');
    select.innerHTML = '<option value="">-- Select Project --</option>';
    
    projects.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = p.name;
      select.appendChild(opt);
    });
  } catch (error) {
    console.error("Failed to load projects", error);
  }
}

async function loadUsers() {
  try {
    const res = await fetch(`${BASE_URL}/api/users/all-users/`, { headers: getHeaders() });
    const data = await res.json();
    // API returns {count, results: [...]}
    const users = data.results || [];
    
    const select = document.getElementById('task-user');
    select.innerHTML = '<option value="">-- Assign To --</option>';
    
    users.forEach(u => {
      const opt = document.createElement('option');
      opt.value = u.id;
      opt.textContent = `${u.first_name || u.username} (${u.role})`;
      select.appendChild(opt);
    });
  } catch (error) {
    console.error("Failed to load users", error);
  }
}

async function createProject() {
  const nameInput = document.getElementById('new-project-name');
  const msgEl = document.getElementById('project-msg');
  msgEl.style.color = '#ef4444';
  
  if (!nameInput.value.trim()) {
    msgEl.textContent = "Project name is required.";
    return;
  }
  
  try {
    const res = await fetch(`${BASE_URL}/api/projects/create/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({ name: nameInput.value.trim() })
    });
    
    if (!res.ok) throw new Error("Failed to create project");
    
    msgEl.style.color = '#10b981';
    msgEl.textContent = "Project created successfully!";
    nameInput.value = '';
    
    // Refresh project dropdown
    await loadProjects();
    
    setTimeout(() => msgEl.textContent = '', 3000);
  } catch (error) {
    msgEl.textContent = error.message;
  }
}

async function createTask() {
  const msgEl = document.getElementById('task-msg');
  msgEl.style.color = '#ef4444';
  
  const payload = {
    project: document.getElementById('task-project').value,
    title: document.getElementById('task-title').value.trim(),
    assigned_to: document.getElementById('task-user').value,
    priority: document.getElementById('task-priority').value,
    due_date: document.getElementById('task-due').value,
    status: 'To Do'
  };
  
  if (!payload.project || !payload.title || !payload.assigned_to || !payload.due_date) {
    msgEl.textContent = "Please fill all fields.";
    return;
  }
  
  try {
    const res = await fetch(`${BASE_URL}/api/tasks/create/`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload)
    });
    
    if (!res.ok) {
      const err = await res.json().catch(()=>({}));
      throw new Error(err.detail || "Failed to create task");
    }
    
    msgEl.style.color = '#10b981';
    msgEl.textContent = "Task assigned successfully!";
    
    // clear form except project/user might be kept for rapid entry
    document.getElementById('task-title').value = '';
    document.getElementById('task-due').value = '';
    
    // Refresh the admin dashboard table
    await fetchAdminData();
    
    setTimeout(() => msgEl.textContent = '', 3000);
  } catch (error) {
    msgEl.textContent = error.message;
  }
}
