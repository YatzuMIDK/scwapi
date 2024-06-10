from fastapi import APIRouter, HTTPException
from utils.scraper import get_player_info

router = APIRouter()

@router.get("/{player_name}")
async def get_player(player_name: str):
    try:
        player_info = get_player_info(player_name)
        if not player_info:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        return player_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
