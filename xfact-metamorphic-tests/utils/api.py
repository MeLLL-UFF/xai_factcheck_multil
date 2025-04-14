import openai
import os
from dotenv import load_dotenv

load_dotenv()


def query_model(model_name, prompt, cache_dir=None, metadata=None):
    """
    Consulta o modelo via API do OpenAI (incluindo modelos via base_url customizado como Sabia-3 e Gemini).

    Parâmetros:
    - model_name: "gpt-4-turbo", "sabia-3", "gemini-1.5-flash"
    - prompt: string formatada com os dados da notícia
    - cache_dir: ignorado por enquanto
    - metadata: dicionário com metadados da entrada (opcional)

    Retorna:
    - dicionário com a resposta, o modelo e o prompt usado.
    """

    if "sabia" in model_name.lower():
        client = openai.OpenAI(
            api_key=os.getenv("MARITACA_API_KEY"),
            base_url="https://chat.maritaca.ai/api",
        )
        model_id = "sabia-3"

    elif "gemini" in model_name.lower():
        client = openai.OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta",
        )
        model_id = "gemini-2.0-flash"

    elif "gpt" in model_name.lower():
        client = openai.OpenAI(api_key=os.getenv("OPEN_API_KEY"))
        model_id = "gpt-4-turbo"
    else:
        raise ValueError(f"[✗] Modelo não reconhecido: {model_name}")

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"[ERROR] {str(e)}"

    return {
        "model": model_name,
        "prompt": prompt,
        "response": answer,
        "metadata": metadata
    }
