# Import libraries
from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline
import os
from dotenv import load_dotenv
import replicate

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load HTML templates
templates = Jinja2Templates(directory="templates")

# Retrieve Replicate API token
replicate_token = os.getenv("REPLICATE_API_TOKEN")

# Ensure API token is set
if not replicate_token:
    raise ValueError("Replicate API Token not found. Set REPLICATE_API_TOKEN in your environment variables.")

# Function to generate lyrics using Hugging Face's GPT-NEO model
def generate_lyrics(prompt):
    # Initialize text generation pipeline with Hugging Face's GPT-NEO model
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B', device=0)  # device=0 to use GPU if available
    # Generate lyrics based on the prompt
    response = generator(prompt, max_length=50, temperature=0.7, do_sample=True)
    # Extract generated text from response
    output = response[0]['generated_text']
    # Format the generated lyrics
    cleaned_output = output.replace("\n", " ")
    formatted_lyrics = f"♪ {cleaned_output} ♪"
    return formatted_lyrics

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-music")
async def generate_music(prompt: str = Form(...), duration: int = Form(...)):
    # Generate lyrics using GPT-Neo
    lyrics = generate_lyrics(prompt)
    prompt_with_lyrics = lyrics
    print("Generated Lyrics:", prompt_with_lyrics)
    
    # Running Bark model from Replicate for text-to-music generation
    output = replicate.run(
        "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
        input={
            "prompt": prompt_with_lyrics,  # Use generated lyrics
            "text_temp": 0.7,
            "output_full": False,
            "waveform_temp": 0.7,
            "history_prompt": "announcer"
        }
    )

    print("Replicate Output:", output)
    
    # Extract music URL
    music_url = output.get('audio_out')
    if not music_url:
        return JSONResponse(content={"error": "Failed to generate music."}, status_code=500)

    return JSONResponse(content={"url": music_url})
