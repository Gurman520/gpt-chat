
# Llama 3 Chat Application 🦙✨

## 📖 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running Llama Locally](#-running-llama-locally)
- [For Developers](#-for-developers)

## 🌟 About
Interactive chat application powered by Llama 3.1 AI. Provides a user-friendly interface with conversation history and Markdown-formatted responses.

## 🚀 Features
- 💬 Persistent conversation history
- ✨ Markdown support with code highlighting
- ⚡ FastAPI backend
- 📱 Responsive UI
- 🔄 Typing animations

## 🛠 Tech Stack
- **Backend**: Python + FastAPI
- **Frontend**: HTML/CSS/JS
- **AI**: Llama 3.1 (Docker)
- **DB**: SQLite

## ⚙️ Installation

### Requirements
- Python 3.9+
- Docker (optional)

```bash
# Clone repository
git clone https://github.com/your-repo/llama-chat.git
cd llama-chat

# Install dependencies
pip install -r requirements.txt

# Initialize DB
python -c "from app.models import init_db; init_db()"
```

## 🐋 Running Llama Locally

The source image of Docker Lama is used to run Llama.

[Link to the official project page](https://ollama.com/blog/ollama-is-now-available-as-an-official-docker-image)

Do CMD:
``` bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

docker exec -it ollama ollama run llama3:8b
```

## 👨‍💻 For Developers

### Run Application
```bash
uvicorn app.main:app --reload
```

<!-- ### Docker Build
```bash
docker-compose up -d --build
``` -->

---