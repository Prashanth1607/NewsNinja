# 🥷 NewsNinja - Stealthy News Aggregator

Your personal **news ninja** that silently gathers headlines and Reddit reactions, then delivers audio briefings straight to your ears.  
**No scroll, just soul.**

---

## ✨ FEATURES

- 🗞️ **Scrape premium news websites** *(bypassing paywalls)*
- 🕵️‍♂️ **Extract live Reddit reactions** *(even from JS-heavy threads)*
- 🔊 **AI-powered audio summaries** *(text-to-speech with ElevenLabs)*
- ⚡ **Real-time updates** *(powered by Bright Data's MCP magic)*

---

## 🛠️ PREREQUISITES

- Python 3.9+
- [Bright Data](https://brightdata.com) account
- [ElevenLabs](https://elevenlabs.io) account

---

## 🚀 QUICK START

### 1. Clone the Dojo

```bash
git clone https://github.com/AIwithhassan/newsninja.git
cd newsninja

2. Install Dependencies
pipenv install
pipenv shell

3. Ninja Secrets (Environment Setup)
cp .env.example .env

Edit .env and add your secrets:
# Bright Data
BRIGHTDATA_MCP_KEY="your_mcp_api_key"
BROWSER_AUTH="your_browser_auth_token"

# ElevenLabs 
ELEVENLABS_API_KEY="your_text_to_speech_key"

⚙️ Prepare Your Weapons (Bright Data Setup)
Create an MCP Zone: Create Zone

Enable browser authentication

Copy and paste credentials into .env


🏃‍♂️ RUNNING THE NINJA
First Terminal (Backend):
pipenv run python backend.py

Second Terminal (Frontend):
pipenv run streamlit run frontend.py

📁 PROJECT STRUCTURE
.
├── frontend.py          # Streamlit UI
├── backend.py           # API & data processing  
├── utils.py             # UTILS  
├── news_scraper.py      # News Scraper  
├── reddit_scraper.py    # Reddit Scraper  
├── models.py            # Pydantic model
├── Pipfile              # Dependency scroll
├── .env.example         # Secret map template
└── requirements.txt     # Alternative dependency list


📝 NOTES
First scrape takes 15-20 seconds (good ninjas are patient).

Reddit scraping uses real browser emulation via MCP.

Keep .env file secret — ninjas never reveal their tools.

