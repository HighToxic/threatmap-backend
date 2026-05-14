import asyncio
import json
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌍 Lista de locais reais (Polos Tecnológicos e Países com alto tráfego)
REAL_LOCATIONS = [
    {"name": "São Paulo, BR", "lat": -23.5505, "lng": -46.6333},
    {"name": "Nova York, EUA", "lat": 40.7128, "lng": -74.0060},
    {"name": "Pequim, CN", "lat": 39.9042, "lng": 116.4074},
    {"name": "Moscou, RU", "lat": 55.7558, "lng": 37.6173},
    {"name": "Frankfurt, DE", "lat": 50.1109, "lng": 8.6821},
    {"name": "Tóquio, JP", "lat": 35.6762, "lng": 139.6503},
    {"name": "Londres, UK", "lat": 51.5074, "lng": -0.1278},
    {"name": "Seul, KR", "lat": 37.5665, "lng": 126.9780},
    {"name": "Sydney, AU", "lat": -33.8688, "lng": 151.2093},
    {"name": "Cidade do Cabo, ZA", "lat": -33.9249, "lng": 18.4241},
    {"name": "Toronto, CA", "lat": 43.6510, "lng": -79.3470},
    {"name": "Nova Delhi, IN", "lat": 28.6139, "lng": 77.2090}
]

ATTACK_TYPES = ["DDoS", "Malware", "Phishing", "Brute Force"]

async def generate_attack_data():
    while True:
        # Sorteia dois locais diferentes para não ter ataque de um lugar para ele mesmo
        source = random.choice(REAL_LOCATIONS)
        dest = random.choice(REAL_LOCATIONS)
        while source["name"] == dest["name"]:
            dest = random.choice(REAL_LOCATIONS)

        attack = {
            "id": f"atk_{random.randint(1000, 9999)}",
            "type": random.choice(ATTACK_TYPES),
            "source": source,
            "dest": dest,
            "timestamp": datetime.now().isoformat()
        }
        yield attack
        await asyncio.sleep(random.uniform(2.0, 6.0))

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for attack in generate_attack_data():
            await websocket.send_text(json.dumps(attack))
    except Exception as e:
        print(f"Conexão fechada: {e}")
