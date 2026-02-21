// static/js/tasks.js — SEIA Task Manager
 
async function loadTasks() {
  try {
    const res   = await fetch('/api/tasks');
    const tasks = await res.json();
    renderTasks(tasks);
  } catch(e) {}
}
 
function renderTasks(tasks) {
  const list = document.getElementById('task-list');
  if (!list) return;
 
  if (tasks.length === 0) {
    list.innerHTML = '<div class="task-empty">No tasks yet — add one above or ask SEIA in Agent mode!</div>';
    return;
  }
 
  list.innerHTML = tasks.map(t => `
    <div class="task-item" id="task-${t.id}">
      <button class="task-check ${t.done ? 'done' : ''}" onclick="toggleTask(${t.id})" title="Mark done"></button>
      <span class="task-title ${t.done ? 'done' : ''}">${escHtml(t.title)}</span>
      <span class="task-priority priority-${t.priority}">${t.priority}</span>
      <button class="task-del" onclick="deleteTask(${t.id})" title="Delete">✕</button>
    </div>
  `).join('');
}
 
async function addTask() {
  const input    = document.getElementById('task-input');
  const priority = document.getElementById('task-priority');
  const title    = input ? input.value.trim() : '';
  if (!title) return;
 
  try {
    const res  = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        priority: priority ? priority.value : 'normal',
      }),
    });
    const data = await res.json();
    if (data.success) {
      if (input) input.value = '';
      loadTasks();
    }
  } catch(e) {}
}
 
async function toggleTask(id) {
  try {
    await fetch(`/api/tasks/${id}/toggle`, { method: 'POST' });
    loadTasks();
  } catch(e) {}
}
 
async function deleteTask(id) {
  try {
    await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    const el = document.getElementById(`task-${id}`);
    if (el) { el.style.opacity = '0'; el.style.transform = 'translateX(20px)'; el.style.transition = 'all .2s'; setTimeout(() => el.remove(), 200); }
  } catch(e) {}
}
 
function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
 
document.addEventListener('DOMContentLoaded', () => {
  loadTasks();
 
  const input = document.getElementById('task-input');
  if (input) {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); addTask(); }
    });
  }
});
 
