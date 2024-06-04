from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/game_info/{game_name}")
def get_game_info(game_name: str):
    # Implement your logic to fetch game information from Steam
    # Here is an example using a hypothetical API
    url = f"https://api.steampowered.com/.../get_game_details?name={game_name}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching game details")
    return response.json()
