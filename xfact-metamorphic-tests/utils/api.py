import maritalk
import openai
import google.generativeai as genai
import os

def gpt_request(prompt):
    openai.api_key = ""
    response = openai.Completion.create(
        model="gpt-4o-mini",
        prompt=prompt,
        max_tokens=200
    )
    return response['choices'][0]['text'].strip()

def maritaca_request(prompt):
    model = maritalk.MariTalk(key="api key", model="sabia-2-small")
    response = model.generate(prompt, max_tokens=200)
    answer = response["answer"]
    return answer

def gemini_request(prompt):
    genai.configure(api_key="")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
