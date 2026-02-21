// static/js/chat.js — SEIA Chat Logic
 
const MODE_COLORS = {
  friend:    '#10B981',
  partner:   '#8B5CF6',
  coder:     '#06B6D4',
  therapist: '#F97316',
  agent:     '#1D6EF5',
};
const MODE_LABELS = {
  friend:    '💚 Friend',
  partner:   '💜 Partner',
  coder:     '🩵 Coder',
  therapist: '🧡 Therapist',
  agent:     '💙 Agent',
};
 
let currentMode = 'friend';
 
// ── Render markdown-ish formatting ──
function renderContent(text) {
  return text
    .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');
}
 
function addBubble(role, content, mode, time, switchNotif) {
  const win = document.getElementById('chat-window');
  if (!win) return;
 
  // Hide welcome screen on first message
  const welcome = document.getElementById('chat-welcome');
  if (welcome) welcome.style.display = 'none';
 
  // Mode switch notification
  if (switchNotif) {
    const n = document.createElement('div');
    n.className = 'mode-switch-notif';
    n.textContent = `⚡ Switched to ${MODE_LABELS[mode] || mode}`;
    win.appendChild(n);
  }
 
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${role}`;
 
  if (role === 'bot' && mode) {
    const color = MODE_COLORS[mode] || '#1D6EF5';
    bubble.style.borderLeft = `3px solid ${color}`;
    // meta line
    const meta = document.createElement('div');
    meta.className = 'bubble-meta';
    const dot = document.createElement('div');
    dot.className = 'bubble-mode-dot';
    dot.style.background = color;
    const t = document.createElement('span');
    t.className = 'bubble-time';
    t.textContent = time || new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'});
    meta.appendChild(dot); meta.appendChild(t);
    bubble.appendChild(meta);
  }
 
  const body = document.createElement('div');
  body.innerHTML = renderContent(content);
  bubble.appendChild(body);
  win.appendChild(bubble);
  win.scrollTop = win.scrollHeight;
}
 
function showTyping() {
  const win = document.getElementById('chat-window');
  if (!win) return;
  const t = document.createElement('div');
  t.className = 'chat-bubble bot typing-indicator';
  t.id = 'typing';
  t.innerHTML = '<span></span><span></span><span></span>';
  win.appendChild(t);
  win.scrollTop = win.scrollHeight;
}
 
function hideTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}
 
function updateModeUI(mode) {
  currentMode = mode;
  const badge = document.getElementById('current-mode-badge');
  if (badge) {
    badge.textContent = MODE_LABELS[mode] || mode;
    badge.style.color = MODE_COLORS[mode] || '#1D6EF5';
  }
  // sidebar highlight
  document.querySelectorAll('.sidebar-mode-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.mode === mode);
  });
}
 
async function sendMessage(overrideText) {
  const input = document.getElementById('user-input');
  const text = (overrideText || input.value || '').trim();
  if (!text) return;
  if (input) input.value = '';
 
  addBubble('user', text, currentMode);
  showTyping();
 
  try {
    const res  = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    const data = await res.json();
    hideTyping();
 
    if (data.error) {
      addBubble('bot', '⚠️ ' + data.error, currentMode);
      return;
    }
 
    addBubble('bot', data.response, data.mode, null, data.mode_switched);
    updateModeUI(data.mode);
 
    // TTS if voice mode on
    if (typeof speak === 'function') speak(data.response);
 
    // Silent mood log
    if (data.auto_mood) {
      fetch('/api/mood/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ score: data.auto_mood, auto: true }),
      }).catch(() => {});
    }
  } catch (err) {
    hideTyping();
    addBubble('bot', 'Connection error. Please try again.', currentMode);
  }
}
 
async function loadHistory() {
  try {
    const res  = await fetch('/api/history');
    const msgs = await res.json();
    msgs.forEach(m => {
      addBubble(
        m.role === 'assistant' ? 'bot' : 'user',
        m.content, m.mode, m.time
      );
    });
    if (msgs.length > 0) {
      const last = msgs[msgs.length - 1];
      updateModeUI(last.mode || 'friend');
    }
  } catch(e) {}
}
 
async function resetChat() {
  if (!confirm('Clear all chat history? This cannot be undone.')) return;
  await fetch('/api/reset', { method: 'POST' });
  const win = document.getElementById('chat-window');
  if (win) win.innerHTML = '';
  const welcome = document.getElementById('chat-welcome');
  if (welcome) welcome.style.display = 'flex';
  updateModeUI('friend');
}
 
function switchMode(mode) {
  const phrases = {
    friend:    '',
    partner:   'seia close',
    coder:     'seia dev',
    therapist: 'seia listen',
    agent:     'seia work',
  };
  const phrase = phrases[mode];
  if (phrase) sendMessage(phrase);
}
 
function useHint(text) {
  const input = document.getElementById('user-input');
  if (input) { input.value = text; input.focus(); }
}
 
document.addEventListener('DOMContentLoaded', () => {
  loadHistory();
 
  const input = document.getElementById('user-input');
  if (input) {
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
    // auto-resize textarea
    input.addEventListener('input', () => {
      input.style.height = 'auto';
      input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    });
  }
});
 
