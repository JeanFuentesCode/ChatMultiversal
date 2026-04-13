import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Cambiamos el import para traer la función grupal
from ia_logic import get_group_chat_response 

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Servidor de Brothers Online"}

@app.post("/chat")
async def chat(data: dict):
    user_message = data.get("message")
    
    # Aquí es donde ocurre la magia: llamamos a la función que orquesta a los 3
    conversation = get_group_chat_response(user_message)
    
    # Devolvemos la lista completa de respuestas
    return {"responses": conversation}