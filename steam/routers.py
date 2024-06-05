from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/game_info/{game_name}")
def get_game_info(game_name: str):
    # Buscar el app ID usando el nombre del juego
    search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=us"
    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if not search_data['items']:
            raise HTTPException(status_code=404, detail="Game not found")
        
        app_id = search_data['items'][0]['id']
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=search_response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

    # Obtener los detalles del juego usando el app ID
    details_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        details_response = requests.get(details_url)
        details_response.raise_for_status()
        details_data = details_response.json()
        
        if not details_data[str(app_id)]['success']:
            raise HTTPException(status_code=404, detail="Game details not found or data unavailable")
        
        return details_data[str(app_id)]['data']
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=details_response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
