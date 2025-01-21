# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if openai.api_key is None:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

app = FastAPI()

class ReportRequest(BaseModel):
    topic: str

@app.post("/generate-report/")
async def generate_report(request: ReportRequest):
    topic = request.topic

    # Define the GPT-4 prompt with HTML-like structure for the report
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
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=1500,
            n=1,
            stop=None,
            temperature=0.7
        )

        report = response.choices[0].text.strip()
        return {"report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

