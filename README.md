# 🎵 Text-to-Song Generator (FastAPI + HuggingFace + Bark)

Turn your ideas into music! This web app generates lyrics from your prompt using Hugging Face’s GPT-Neo model and synthesizes audio using Bark. Built with FastAPI and styled with Jinja2 templates.

---

## 🚀 Features

- 🧠 AI-generated lyrics based on user input
- 🎤 Converts lyrics to vocals using Bark
- 🌐 Simple FastAPI web interface
- 🎧 Returns a `.wav` file you can play or download

---

## 🛠 Tech Stack

- **FastAPI** – Web framework
- **Hugging Face Transformers** – GPT-Neo for text generation
- **Bark** – Text-to-audio generation
- **Jinja2** – Template rendering
- **SciPy** – Save generated audio
- **dotenv** – Load environment variables

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/text-to-song-generator.git
cd text-to-song-generator
