// static/js/mood.js — SEIA Mood Tracker
 
let moodChart = null;
 
async function loadMoodChart(days = 30) {
  try {
    const res  = await fetch(`/api/mood/history?days=${days}`);
    const data = await res.json();
    const ctx  = document.getElementById('mood-chart');
    if (!ctx) return;
 
    const labels = data.map(d => d.date);
    const scores = data.map(d => d.score);
 
    if (moodChart) moodChart.destroy();
 
    moodChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Mood',
          data: scores,
          fill: true,
          borderColor: '#1D6EF5',
          backgroundColor: (ctx) => {
            const g = ctx.chart.ctx.createLinearGradient(0,0,0,220);
            g.addColorStop(0, 'rgba(29,110,245,0.18)');
            g.addColorStop(1, 'rgba(29,110,245,0)');
            return g;
          },
          pointBackgroundColor: scores.map(s =>
            s >= 8 ? '#10B981' : s >= 5 ? '#1D6EF5' : '#EF4444'
          ),
          pointBorderColor: '#02050e',
          pointBorderWidth: 2,
          pointRadius: 5,
          tension: 0.4,
          borderWidth: 2.5,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0d1635',
            borderColor: 'rgba(29,110,245,0.3)',
            borderWidth: 1,
            titleColor: '#60a5fa',
            bodyColor: '#b0c4de',
            callbacks: {
              label: (ctx) => {
                const s = ctx.raw;
                const e = s >= 8 ? '😄' : s >= 6 ? '🙂' : s >= 4 ? '😐' : '😞';
                return ` Mood: ${s}/10  ${e}`;
              }
            }
          }
        },
        scales: {
          y: {
            min: 1, max: 10,
            grid: { color: 'rgba(29,110,245,0.06)' },
            ticks: {
              color: '#6b85b5', stepSize: 1,
              callback: v => {
                const e = {1:'😞',4:'😐',7:'🙂',10:'😄'};
                return e[v] ? `${v} ${e[v]}` : v;
              }
            }
          },
          x: {
            grid: { color: 'rgba(29,110,245,0.04)' },
            ticks: { color: '#6b85b5', maxRotation: 45 }
          }
        }
      }
    });
 
    // No data message
    const noData = document.getElementById('no-mood-data');
    if (noData) noData.style.display = data.length === 0 ? 'block' : 'none';
  } catch(e) {
    console.error('Mood chart error:', e);
  }
}
 
async function loadMoodStats() {
  try {
    const res  = await fetch('/api/mood/stats');
    const data = await res.json();
    const set  = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };
    set('mood-average', data.average || '–');
    set('mood-streak',  data.streak  || 0);
    set('mood-total',   data.total   || 0);
    set('mood-best',    data.best    || '–');
  } catch(e) {}
}
 
async function logMood() {
  const slider = document.getElementById('mood-slider');
  const note   = document.getElementById('mood-note');
  if (!slider) return;
  const score = parseInt(slider.value);
 
  try {
    const res  = await fetch('/api/mood/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score, note: note ? note.value : '', auto: false }),
    });
    const data = await res.json();
    if (data.success) {
      const ok = document.getElementById('mood-success');
      if (ok) { ok.style.display = 'block'; setTimeout(() => ok.style.display='none', 3000); }
      if (note) note.value = '';
      loadMoodChart();
      loadMoodStats();
    }
  } catch(e) {}
}
 
function updateMoodDisplay(val) {
  const score   = document.getElementById('mood-score-display');
  const emoji   = document.getElementById('mood-emoji-display');
  const emojis  = { 1:'😭',2:'😢',3:'😞',4:'😔',5:'😐',6:'🙂',7:'😊',8:'😄',9:'🤩',10:'🥳' };
  if (score) score.textContent = val;
  if (emoji) emoji.textContent = emojis[val] || '😐';
}
 
document.addEventListener('DOMContentLoaded', () => {
  const days = ['7d','14d','30d'];
 
  // days buttons
  document.querySelectorAll('.days-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.days-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadMoodChart(parseInt(btn.dataset.days));
    });
  });
 
  // slider live update
  const slider = document.getElementById('mood-slider');
  if (slider) {
    slider.addEventListener('input', () => updateMoodDisplay(slider.value));
    updateMoodDisplay(slider.value);
  }
 
  loadMoodChart(30);
  loadMoodStats();
});
 
