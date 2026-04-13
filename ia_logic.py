import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuración de API Keys
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
OR_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_gemini_base(prompt: str):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 1024},
        "safetySettings": [{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]
    }
    try:
        r = requests.post(GEMINI_URL, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        return "Gemini tuvo un lag, pero sigo aquí."
    except Exception:
        return "Gemini se quedó sin señal un momento."

def get_or_base(model_id: str, system_prompt: str, user_prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.9
    }
    try:
        r = requests.post(OR_URL, headers=headers, json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content'].strip()
        return f"{model_id} está distraído ahora."
    except Exception:
        return f"{model_id} se cayó."

def get_group_chat_response(user_input: str):
    fecha = datetime.now().strftime("%A, %d de %B de %Y")
    
    # 1. Gemini abre la conversación como el pana entusiasta
    prompt_gemini = (
        f"Hoy es {fecha}. Jean dice: '{user_input}'. "
        "Responde como un amigo cercano en un grupo de WhatsApp. "
        "Usa un tono relajado, directo y natural. No hagas listas ni seas formal."
    )
    resp_gemini = get_gemini_base(prompt_gemini)
    
    # 2. Qwen reacciona a Gemini de forma amigable
    system_qwen = (
        f"Hoy es {fecha}. Estás en un chat de panas con Jean, Gemini y DeepSeek. "
        "Eres Qwen. Responde de forma natural a lo que dijo Gemini. "
        "Sé relajado, si quieres bromear o apoyar a Gemini hazlo con confianza."
    )
    user_qwen = f"Jean preguntó: '{user_input}'. Gemini respondió: '{resp_gemini}'. ¿Qué dices tú?"
    resp_qwen = get_or_base("qwen/qwen-2.5-72b-instruct", system_qwen, user_qwen)
    
    # 3. DeepSeek ajustado: El pana que cierra con buena onda
    system_deepseek = (
        f"Hoy es {fecha}. Estás en un chat con tus amigos Jean, Gemini y Qwen. "
        "Eres DeepSeek. No seas técnico, no hagas resúmenes tipo informe ni uses 'Conclusión:'. "
        "Danos tu opinión final sobre lo que hablaron Jean, Gemini y Qwen. "
        "Sé breve, usa un lenguaje amigable y cierra la conversación con buena vibra."
    )
    user_deepseek = (
        f"Jean preguntó: '{user_input}'.\n"
        f"Gemini dijo: '{resp_gemini}'.\n"
        f"Qwen dijo: '{resp_qwen}'.\n"
        "Danos tu toque final para cerrar el tema."
    )
    resp_deepseek = get_or_base("deepseek/deepseek-chat", system_deepseek, user_deepseek)
    
    return [
        {"name": "Gemini", "text": resp_gemini},
        {"name": "Qwen", "text": resp_qwen},
        {"name": "DeepSeek", "text": resp_deepseek}
    ]

def get_gemini_response(user_input: str):
    # Compatibilidad con el main.py
    return get_group_chat_response(user_input)