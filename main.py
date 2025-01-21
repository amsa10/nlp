# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

app = FastAPI()

class ReportRequest(BaseModel):
    topic: str

@app.post("/generate-report/")
async def generate_report(request: ReportRequest):
    topic = request.topic

    # Define the GPT prompt with HTML-like structure for headings, paragraphs, and lists
    prompt = f"""
    Напишите академическую статью по теме '{topic}' на академическом русском языке. Следуйте указанной структуре:
    1. Введение
    2. Применение в Казахстане
    3. Мировой опыт
    4. Модели
    5. Что можно сделать в Казахстане
    6. Предлагаемые направления для реализации в Казахстане.
    7. Этапы реализации

    Используйте теги HTML для форматирования:
    - <h2> для заголовков
    - <p> для абзацев
    - <ul> и <li> для списков
    """

    try:
        # Send the prompt to the OpenAI API to generate a report using GPT-4
        response = openai.Completion.create(
            model="gpt-4",  # Use GPT-4 instead of GPT-3
            prompt=prompt,
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Get the generated text and clean up if necessary
        report = response.choices[0].text.strip()

        # Return the report as HTML (directly without plain text)
        return {"report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
