from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/game_info/{game_name}")
def get_game_info(game_name: str):
    # URL de ejemplo para la API de Steam
    url = f"https://store.steampowered.com/api/appdetails?appids={game_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Levantar una excepción para errores HTTP
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

    data = response.json()
    if not data or game_name not in data or not data[game_name]['success']:
        raise HTTPException(status_code=404, detail="Game not found or data unavailable")

    return data[game_name]['data']
