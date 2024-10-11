import maritalk
import openai
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def gpt_request(prompt):
    openai.api_key = os.getenv("OPEN_API_KEY")
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=200
    )
    return response['choices'][0]['text'].strip()

def maritaca_request(prompt):
    model = maritalk.MariTalk(key=os.getenv("MARITACA_API_KEY"), model="sabia-2-small")
    response = model.generate(prompt, max_tokens=200)
    answer = response["answer"]
    return answer

def gemini_request(prompt):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
