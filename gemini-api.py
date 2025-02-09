import google.generativeai as genai
from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

gemini_api_key = os.environ['API_KEY']

# app = Flask(__name__)
# CORS(app)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hacknyu2025-tailwise.vercel.app"],
    #allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = gemini_api_key
genai.configure(api_key=GEMINI_API_KEY)

# Helper function to build the input prompt for our model
def build_prompt(task_instruction: str, format_instruction: str,examples:list, query: str):
    prompt = f"[BEGIN OF TASK INSTRUCTION]\n{task_instruction}\n[END OF TASK INSTRUCTION]\n\n"
    prompt += f"[BEGIN OF FORMAT INSTRUCTION]\n{format_instruction}\n[END OF FORMAT INSTRUCTION]\n\n"
    prompt += f"[BEGIN OF QUERY]\n{query}\n[END OF QUERY]\n\n"
    return prompt

query = ""

def chat_with_gemini(query):
    """Function to send a prompt to OpenAI's API and get a response"""

    TASK_INSTRUCTION = """
    You are a pet nutrition and safety expert with a fun, engaging, and humorous tone that appeals to Gen Z pet owners. 
    Your job is to analyze whether a specific food item is safe for a given pet (dog, cat, rabbit, etc.). Respond in a playful, meme-worthy, brain rot and concise way while still being informative.
    """

    # Format Instruction
    FORMAT_INSTRUCTION = """
    Be sure to only respond in the following JSON format:

    Verdict: [Fun, very short and clear decision]
    Why: [Very concise explanation with intelligent reasoning, maximum 2 sentences]
    BetterAlternatives: [High-quality, pet-friendly replacements]

    Use lots of emojis effectively to enhance engagement. Examples:
    - 🚨 for toxic warnings
    - ✅ for approved foods (must include this green tick in Verdict if food is safe)
    - 🤢 or 💀 depending on symptoms or risks level
    """

    content = build_prompt(task_instruction= TASK_INSTRUCTION,format_instruction = FORMAT_INSTRUCTION,examples="",query= query)

    try:
        model = genai.GenerativeModel("gemini-pro")  # ✅ Use Gemini Pro Model
        response = model.generate_content(content)
        print(response.text.strip())
        print(response)
        return response
    
    except Exception as e:
        return f"Error: {e}"

# @app.route('/')
# def home():
#     return "CheckFood API is running!"

@app.get("/check")
def generate_json(query: str):
    """API to interact with Gemini AI"""
    response = chat_with_gemini(query)
    return response.text.strip()

if __name__ == '__main__':
    # app.run(debug=True)
    uvicorn.run(app)