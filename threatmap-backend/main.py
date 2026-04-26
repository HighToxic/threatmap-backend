import asyncio
import json
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permite que o Frontend conecte sem erros de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulador de dados
def generate_mock_attack():
    attack_types = ["DDoS", "Malware", "Phishing", "Brute Force"]
    return {
        "id": random.randint(10000, 99999),
        "type": random.choice(attack_types),
        "source": {
            "lat": random.uniform(-60, 60),
            "lng": random.uniform(-120, 120),
            "country": "Origem"
        },
        "dest": {
            "lat": random.uniform(-60, 60),
            "lng": random.uniform(-120, 120),
            "country": "Destino"
        }
    }

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Gera um ataque e envia como JSON
            attack = generate_mock_attack()
            await websocket.send_json(attack)
            # Espera entre 1 e 3 segundos para o próximo ataque
            await asyncio.sleep(random.uniform(1.0, 3.0)) 
    except Exception as e:
        print(f"Conexão encerrada: {e}")

# Para rodar localmente: uvicorn main:app --reload