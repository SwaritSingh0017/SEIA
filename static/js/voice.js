const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let isListening  = false;
let voiceMode    = false;
 
function initSpeech() {
  if (!SR) return false;
  recognition = new SR();
  recognition.continuous     = false;
  recognition.interimResults = true;
  recognition.lang           = 'en-US';
 
  recognition.onresult = (e) => {
    const t = Array.from(e.results).map(r => r[0].transcript).join('');
    const input = document.getElementById('user-input');
    if (input) input.value = t;
    if (e.results[e.results.length - 1].isFinal) {
      stopListening();
      if (typeof sendMessage === 'function') sendMessage(t);
    }
  };
  recognition.onerror = () => stopListening();
  recognition.onend   = () => stopListening();
  return true;
}
 
function startListening() {
  if (!recognition && !initSpeech()) return;
  try {
    recognition.start();
    isListening = true;
    updateMicUI(true);
    const vi = document.getElementById('voice-indicator');
    if (vi) vi.classList.remove('hidden');
  } catch(e) {}
}
 
function stopListening() {
  if (recognition && isListening) { try { recognition.stop(); } catch(e) {} }
  isListening = false;
  updateMicUI(false);
  const vi = document.getElementById('voice-indicator');
  if (vi) vi.classList.add('hidden');
}
 
function toggleListening() { isListening ? stopListening() : startListening(); }
 
// ── Text-to-Speech ──
function speak(text) {
  if (!voiceMode || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const clean = text
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/[*_`#>]/g, '')
    .replace(/\n/g, '. ')
    .replace(/[\uD800-\uDFFF]/g, '')
    .trim();
  if (!clean) return;
  const u = new SpeechSynthesisUtterance(clean);
  const voices = window.speechSynthesis.getVoices();
  const pick = voices.find(v => v.name.includes('Google') && v.lang === 'en-US')
            || voices.find(v => v.lang.startsWith('en') && v.localService)
            || voices.find(v => v.lang.startsWith('en'))
            || voices[0];
  if (pick) u.voice = pick;
  u.rate = 0.92; u.pitch = 1.05; u.volume = 1;
  window.speechSynthesis.speak(u);
}
 
function toggleVoiceMode() {
  voiceMode = !voiceMode;
  const btn = document.getElementById('voice-mode-btn');
  if (btn) {
    btn.textContent = voiceMode ? '🔊 Voice ON' : '🔇 Voice OFF';
    btn.classList.toggle('active', voiceMode);
  }
  if (voiceMode) speak('Voice mode active. I will speak all my responses.');
}
 
function updateMicUI(on) {
  const btn = document.getElementById('mic-btn');
  if (!btn) return;
  btn.innerHTML    = on ? '🔴' : '🎙️';
  btn.classList.toggle('listening', on);
  btn.title = on ? 'Listening… click to stop' : 'Click to speak';
}
 
window.addEventListener('load', () => {
  initSpeech();
  if (window.speechSynthesis) {
    window.speechSynthesis.getVoices();
    setTimeout(() => window.speechSynthesis.getVoices(), 600);
  }
});
 
