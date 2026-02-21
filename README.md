# ⚡ SEIA — Sentient Emotional Interactive Agent
 
<div align="center">
 
![SEIA Banner](https://img.shields.io/badge/SEIA-v1.0-1D6EF5?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Cost](https://img.shields.io/badge/Cost-%240%2Fmonth-10B981?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
 
**One AI. Five personalities. Free forever.**
 
*Your therapist at 3am. Your senior dev at work. Your best friend on bad days. Your agent that gets things done.*
 
[Live Demo](https://seia.pythonanywhere.com) · [Report Bug](https://github.com/yourusername/SEIA/issues) · [Request Feature](https://github.com/yourusername/SEIA/issues)
 
</div>
 
---
 
## 🎯 What is SEIA?
 
SEIA is a full-stack AI personal assistant web application that adapts its personality to what you need. Unlike generic chatbots, SEIA:
 
- **Remembers** your conversations across sessions
- **Tracks** your mental health automatically from conversation tone
- **Executes** real-world tasks (WhatsApp, email, alarms) via n8n
- **Speaks** to you and listens via browser-native voice APIs
- **Costs absolutely nothing** to run — free forever stack
 
---
 
## 🎭 Five Personalities
 
| Mode | Trigger | Personality |
|------|---------|-------------|
| 💚 **Friend** | Default | Unfiltered, casual, brutally honest bestie |
| 💜 **Partner** | `seia close` | Warm, emotionally devoted companion |
| 🩵 **Coder** | `seia dev` | Senior engineer — reviews code, debugs, architects |
| 🧡 **Therapist** | `seia listen` | Calm, empathetic, non-judgmental mental health support |
| 💙 **Agent** | `seia work` | Task executor — sends WhatsApp, sets alarms, fires n8n |
 
---
 
## 🆓 Free Forever Stack
 
| Component | Tool | Why Free |
|-----------|------|----------|
| Backend | Python Flask | Open source |
| Database | SQLite → Supabase | 500MB free tier, no expiry |
| AI | OpenRouter (Llama 3.1) | Free models, rate-limited |
| Voice | Web Speech API | Browser native |
| Automation | n8n self-hosted | Free on Render.com |
| Charts | Chart.js | MIT open source |
| Hosting | PythonAnywhere | Free tier, no sleep |
| Notifications | ntfy.sh | Completely free |
 
**Total monthly cost: $0.00**
 
---
 
## ✨ Features
 
- 🔐 **Full Auth System** — Signup, login, sessions, profile
- 💬 **Persistent Memory** — SEIA remembers your entire history
- 🧠 **Passive Mood Tracking** — Auto-detects emotional tone from messages
- 📊 **Mood Dashboard** — 30-day Chart.js trend graphs + streaks
- 🎙️ **Voice Mode** — Full bidirectional voice conversation (STT + TTS)
- ⚡ **n8n Automation** — WhatsApp, Telegram, Gmail, alarms, reminders
- 🛡️ **Crisis Safety Layer** — Detects distress and surfaces helpline resources
- 📓 **Private Journal** — Encrypted to your account
- ✅ **Task Manager** — Priorities, quick-add, voice commands
- ⭐ **Review System** — Public wall with per-mode ratings
 
---
 
## 🚀 Quick Start
 
### 1. Clone & setup
 
```bash
git clone https://github.com/yourusername/SEIA.git
cd SEIA
 
# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# OR: venv\Scripts\activate     # Windows
 
# Install dependencies
pip install -r requirements.txt
```
 
### 2. Configure API keys
 
```bash
# Edit key.env with your keys
cp key.env.example key.env
nano key.env   # or open in VS Code
```
 
Get your free keys:
- **OpenRouter** (AI): [openrouter.ai/keys](https://openrouter.ai/keys) — free, no card
- **n8n** (automation): Deploy free on [render.com](https://render.com)
- **Twilio** (WhatsApp): [console.twilio.com](https://console.twilio.com) — free sandbox
- **ntfy.sh** (notifications): No signup, just pick a topic name
 
### 3. Run
 
```bash
python app.py
# Open: http://localhost:5000
```
 
That's it. Sign up and start talking to SEIA.
 
---
 
## 📁 Project Structure
 
```
SEIA/
├── app.py                    # Flask factory + main routes
├── config.py                 # AI mode prompts + settings
├── models.py                 # DB: User, Message, Mood, Task, Journal, Review
├── requirements.txt
├── key.env                   # API keys (never commit!)
├── routes/
│   ├── auth.py               # /login /signup /logout /profile
│   ├── chat.py               # /api/chat — SEIA AI engine
│   ├── mood.py               # /api/mood/* — mood tracking
│   ├── tasks.py              # /api/tasks — task manager
│   ├── journal.py            # /api/journal — private journal
│   ├── reviews.py            # /api/reviews — review system
│   └── n8n_handler.py        # n8n webhook trigger
├── templates/
│   ├── landing.html          # Public landing page
│   ├── login.html / signup.html
│   ├── chat.html             # Main chat interface
│   ├── dashboard.html        # Mood charts + tasks
│   ├── profile.html / journal.html / reviews.html
└── static/
    ├── css/  main.css / chat.css / dashboard.css
    └── js/   chat.js / voice.js / mood.js / tasks.js
```
 
---
 
## 🔧 API Reference
 
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/chat` | POST | ✓ | Send message, get SEIA response |
| `/api/history` | GET | ✓ | Full conversation history |
| `/api/reset` | POST | ✓ | Clear chat history |
| `/api/mood/log` | POST | ✓ | Log mood score (1–10) |
| `/api/mood/history` | GET | ✓ | Mood history (`?days=30`) |
| `/api/mood/stats` | GET | ✓ | Average, streak, best |
| `/api/tasks` | GET/POST | ✓ | List / add tasks |
| `/api/tasks/<id>/toggle` | POST | ✓ | Toggle task done |
| `/api/tasks/<id>` | DELETE | ✓ | Delete task |
| `/api/journal` | GET/POST | ✓ | List / write journal entries |
| `/api/reviews` | GET/POST | ✓ | Reviews |
 
### Chat API example
 
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION" \
  -d '{"message": "seia dev — what is a Python decorator?"}'
```
 
Response:
```json
{
  "response": "A decorator is a function that takes another function...",
  "mode": "coder",
  "mode_label": "🩵 Coder",
  "mode_color": "#06B6D4",
  "mode_switched": true,
  "auto_mood": null,
  "n8n": null
}
```
 
---
 
## 🌐 Deploy to PythonAnywhere (Free)
 
1. Create free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Open Bash console:
```bash
git clone https://github.com/yourusername/SEIA.git
cd SEIA
pip3.10 install --user -r requirements.txt
```
3. **Web tab** → Add new web app → Manual configuration → Python 3.10
4. Set WSGI file to contents of `wsgi.py` (included in repo)
5. Set static files: URL `/static/` → Path `/home/USERNAME/SEIA/static`
6. Upload your `key.env`
7. Click **Reload** → Your app is live at `USERNAME.pythonanywhere.com`
 
---
 
## ⚡ n8n Automation Setup
 
SEIA's Agent mode sends a POST request to your n8n webhook with:
 
```json
{
  "message": "send a WhatsApp to +91XXXXXXXXXX saying hello",
  "seia_reply": "On it! Sending now...",
  "source": "seia-agent-mode"
}
```
 
Import `n8n_workflow.json` into your n8n instance for a pre-built workflow with:
- OpenRouter intent parser
- Switch router (WhatsApp / Telegram / Gmail / Alarm / Reminder)
- Twilio WhatsApp sender
- Gmail sender
- ntfy.sh alarm notifier
 
---
 
## 🎙️ Voice Mode
 
Uses 100% browser-native APIs:
 
- **Input**: [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API) — click mic, speak, auto-sends
- **Output**: [SpeechSynthesis API](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis) — SEIA speaks responses aloud
 
Best supported in: **Chrome**, **Edge**, **Safari**
 
---
 
## 🧠 Mental Health System
 
SEIA passively monitors your wellbeing:
 
1. **Auto-detection** — Scans every message for emotional keywords
2. **Silent logging** — Mood score (1–10) saved without interrupting conversation
3. **Trend visualization** — 30-day Chart.js graph in dashboard
4. **Streak tracking** — Consecutive days of engagement
5. **Crisis detection** — Specific phrases trigger compassionate helpline resources:
   - iCall India: 9152987821
   - Vandrevala Foundation: 1860-2662-345
 
---
 
## 🛠️ Tech Stack
 
```
Backend:    Python 3.10, Flask 3.0, Flask-Login, Flask-SQLAlchemy
Database:   SQLite (dev) / Supabase PostgreSQL (prod)
AI:         OpenRouter API — meta-llama/llama-3.1-8b-instruct:free
Voice:      Web Speech API (STT) + SpeechSynthesis API (TTS)
Automation: n8n (self-hosted on Render.com)
Charts:     Chart.js
Hosting:    PythonAnywhere free tier
Notifs:     ntfy.sh
```
 
---
 
## 🔮 Roadmap
 
- [ ] ChromaDB semantic memory (cross-session recall)
- [ ] ElevenLabs TTS for higher quality voice
- [ ] PWA — install on phone homescreen
- [ ] End-to-end encrypted journal entries
- [ ] Spotify control via n8n
- [ ] Smart home integration (Home Assistant)
- [ ] Daily news briefings by voice
- [ ] Multi-language support
 
---
 
## 🤝 Contributing
 
Pull requests welcome. For major changes, open an issue first.
 
```bash
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```
 
---
 
## 📄 License
 
MIT License — see [LICENSE](LICENSE) for details.
 
---
 
<div align="center">
 
Built with ❤️ by **Swarit Singh**
 
⚡ Free Forever · Open Source · Hackathon Ready
 
</div>
 
