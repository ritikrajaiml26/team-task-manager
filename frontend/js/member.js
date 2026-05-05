// Ensure auth.js is loaded so BASE_URL is available
document.addEventListener('DOMContentLoaded', () => {
  const token = localStorage.getItem('accessToken');
  if (!token) {
    window.location.href = 'login.html';
    return;
  }
  
  // Basic token check and role verification
  fetch(`${BASE_URL}/api/users/me/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => {
    if (data.role === 'Admin') {
      window.location.href = 'admin-dashboard.html'; // redirect admins
    } else {
      document.getElementById('member-name').textContent = data.first_name || data.username;
      initMemberDashboard();
    }
  })
  .catch(() => {
    window.location.href = 'login.html';
  });
});

function logout() {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  window.location.href = 'login.html';
}

function getHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
  };
}

async function initMemberDashboard() {
  await fetchMemberStats();
  await fetchMemberTasks();
}

async function fetchMemberStats() {
  try {
    const res = await fetch(`${BASE_URL}/api/tasks/dashboard/`, { headers: getHeaders() });
    if (!res.ok) throw new Error("Failed to fetch stats");
    
    const data = await res.json();
    
    document.getElementById('stat-total').textContent = data.total_tasks;
    document.getElementById('stat-todo').textContent = data.todo;
    document.getElementById('stat-progress').textContent = data.in_progress;
    document.getElementById('stat-done').textContent = data.done;
    document.getElementById('stat-overdue').textContent = data.overdue;
  } catch (error) {
    console.error("Stats Error:", error);
  }
}

async function fetchMemberTasks() {
  try {
    const container = document.getElementById('tasks-container');
    container.innerHTML = '<p class="form-meta">Loading tasks...</p>';
    
    const res = await fetch(`${BASE_URL}/api/tasks/`, { headers: getHeaders() });
    if (!res.ok) throw new Error("Failed to fetch tasks");
    
    const data = await res.json();
    // Assuming pagination is enabled, data might be {count, results: []}
    const tasks = data.results ? data.results : data;
    
    if (tasks.length === 0) {
      container.innerHTML = '<p class="form-meta">You have no tasks assigned. Good job!</p>';
      return;
    }
    
    container.innerHTML = '';
    
    tasks.forEach(task => {
      // Due date formatting
      const isOverdue = new Date(task.due_date) < new Date() && task.status !== 'Done';
      const dueColor = isOverdue ? 'color: #ef4444; font-weight: bold;' : '';
      
      const card = document.createElement('div');
      card.className = 'task-card';
      
      card.innerHTML = `
        <div class="task-details">
          <h4>${task.title}</h4>
          <div class="task-meta">
            <span class="badge badge-${task.priority}">${task.priority} Priority</span>
            <span style="${dueColor}">Due: ${task.due_date}</span>
          </div>
        </div>
        <div class="task-actions">
          <select class="status-select" onchange="updateTaskStatus(${task.id}, this.value)">
            <option value="To Do" ${task.status === 'To Do' ? 'selected' : ''}>To Do</option>
            <option value="In Progress" ${task.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
            <option value="Done" ${task.status === 'Done' ? 'selected' : ''}>Done</option>
          </select>
        </div>
      `;
      container.appendChild(card);
    });
    
  } catch (error) {
    console.error("Tasks Error:", error);
    document.getElementById('tasks-container').innerHTML = '<p class="form-meta" style="color:red">Failed to load tasks.</p>';
  }
}

async function updateTaskStatus(taskId, newStatus) {
  try {
    const res = await fetch(`${BASE_URL}/api/tasks/${taskId}/`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify({ status: newStatus })
    });
    
    if (!res.ok) throw new Error("Failed to update status");
    
    // Refresh stats after status update
    await fetchMemberStats();
    
  } catch (error) {
    alert(error.message);
    // revert selection visually by re-fetching
    fetchMemberTasks();
  }
}
