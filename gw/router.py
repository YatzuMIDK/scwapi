import time
import random
import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import asyncio
import aiohttp

router = APIRouter()

# Estructura para almacenar los sorteos
giveaways = {}

# Modelos de datos
class Giveaway(BaseModel):
    id: str
    winners_count: int
    duration: int  # Duration in seconds
    webhook_id: str
    webhook_token: str

class Participant(BaseModel):
    giveaway_id: str
    participant_id: str
    participant_name: str

# Endpoint para crear un sorteo
@router.post("/create/")
async def create_giveaway(giveaway: Giveaway, background_tasks: BackgroundTasks):
    giveaways[giveaway.id] = {
        "winners_count": giveaway.winners_count,
        "participants": [],
        "end_time": time.time() + giveaway.duration,
        "webhook_id": giveaway.webhook_id,
        "webhook_token": giveaway.webhook_token
    }
    background_tasks.add_task(end_giveaway, giveaway.id)
    return {"message": "Giveaway created", "giveaway_id": giveaway.id}

# Endpoint para registrar a los participantes
@router.post("/register/")
async def register_participant(participant: Participant):
    if participant.giveaway_id not in giveaways:
        raise HTTPException(status_code=404, detail="Giveaway not found")
    giveaways[participant.giveaway_id]["participants"].append({
        "id": participant.participant_id,
        "name": participant.participant_name
    })
    return {"message": "Participant registered"}

# Función para finalizar el sorteo y anunciar los ganadores
async def end_giveaway(giveaway_id: str):
    await asyncio.sleep(giveaways[giveaway_id]["end_time"] - time.time())
    participants = giveaways[giveaway_id]["participants"]
    if not participants:
        content = "No hubo participantes en el sorteo."
    else:
        winners = random.sample(participants, min(len(participants), giveaways[giveaway_id]["winners_count"]))
        content = f"¡Los ganadores del sorteo son: {', '.join(winner['name'] for winner in winners)}!"

    async with aiohttp.ClientSession() as session:
        webhook_url = f"https://discord.com/api/webhooks/{giveaways[giveaway_id]['webhook_id']}/{giveaways[giveaway_id]['webhook_token']}"
        await session.post(webhook_url, json={"content": content})

    del giveaways[giveaway_id]
