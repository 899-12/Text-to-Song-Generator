from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline
import os
import numpy as np
import scipy.io.wavfile
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Generate lyrics using GPT-Neo
def generate_lyrics(prompt_text: str) -> str:
    text_gen = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
    result = text_gen(prompt_text, max_length=50, temperature=0.7, do_sample=True)
    lyrics = result[0]["generated_text"].replace("\n", " ")
    return f"♪ {lyrics} ♪"

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-music")
async def generate_music(prompt: str = Form(...)):
    final_lyrics = generate_lyrics(prompt)
    print("Generated Lyrics:", final_lyrics)

    # Generate audio
    audio = generate_audio(final_lyrics)

    # Convert to int16 for WAV
    audio = (audio * 32767).astype(np.int16)

    output_path = "static/generated_music.wav"
    scipy.io.wavfile.write(output_path, SAMPLE_RATE, audio)

    return JSONResponse(content={"url": f"/static/generated_music.wav"})
