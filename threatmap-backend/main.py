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

# 🌍 Lista de locais reais (Polos Tecnológicos, Datacenters e Hubs de Internet)
REAL_LOCATIONS = [
    # América do Sul
    {"name": "São Paulo, BR", "lat": -23.5505, "lng": -46.6333},
    {"name": "Rio de Janeiro, BR", "lat": -22.9068, "lng": -43.1729},
    {"name": "Buenos Aires, AR", "lat": -34.6037, "lng": -58.3816},
    {"name": "Santiago, CL", "lat": -33.4489, "lng": -70.6693},
    {"name": "Bogotá, CO", "lat": 4.7110, "lng": -74.0721},

    # América do Norte
    {"name": "Nova York, EUA", "lat": 40.7128, "lng": -74.0060},
    {"name": "San Francisco, EUA", "lat": 37.7749, "lng": -122.4194},
    {"name": "Miami, EUA", "lat": 25.7617, "lng": -80.1918},
    {"name": "Chicago, EUA", "lat": 41.8781, "lng": -87.6298},
    {"name": "Toronto, CA", "lat": 43.6510, "lng": -79.3470},
    {"name": "Cidade do México, MX", "lat": 19.4326, "lng": -99.1332},

    # Europa
    {"name": "Londres, UK", "lat": 51.5074, "lng": -0.1278},
    {"name": "Frankfurt, DE", "lat": 50.1109, "lng": 8.6821},
    {"name": "Amsterdã, NL", "lat": 52.3676, "lng": 4.9041},
    {"name": "Paris, FR", "lat": 48.8566, "lng": 2.3522},
    {"name": "Madri, ES", "lat": 40.4168, "lng": -3.7038},
    {"name": "Moscou, RU", "lat": 55.7558, "lng": 37.6173},
    {"name": "Estocolmo, SE", "lat": 59.3293, "lng": 18.0686},

    # Ásia e Oriente Médio
    {"name": "Pequim, CN", "lat": 39.9042, "lng": 116.4074},
    {"name": "Hong Kong, HK", "lat": 22.3193, "lng": 114.1694},
    {"name": "Tóquio, JP", "lat": 35.6762, "lng": 139.6503},
    {"name": "Seul, KR", "lat": 37.5665, "lng": 126.9780},
    {"name": "Singapura, SG", "lat": 1.3521, "lng": 103.8198},
    {"name": "Nova Delhi, IN", "lat": 28.6139, "lng": 77.2090},
    {"name": "Mumbai, IN", "lat": 19.0760, "lng": 72.8777},
    {"name": "Dubai, AE", "lat": 25.2048, "lng": 55.2708},
    {"name": "Tel Aviv, IL", "lat": 32.0853, "lng": 34.7818},

    # África e Oceania
    {"name": "Cidade do Cabo, ZA", "lat": -33.9249, "lng": 18.4241},
    {"name": "Joanesburgo, ZA", "lat": -26.2041, "lng": 28.0473},
    {"name": "Cairo, EG", "lat": 30.0444, "lng": 31.2357},
    {"name": "Sydney, AU", "lat": -33.8688, "lng": 151.2093},
    {"name": "Melbourne, AU", "lat": -37.8136, "lng": 144.9631}
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
