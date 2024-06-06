from fastapi import APIRouter, HTTPException
import requests

router = APIRouter()

@router.get("/game/{game_name}")
def get_steam_game_info(game_name: str):
    try:
        # Buscar el juego en Steam para obtener su AppID
        search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=mx"
        search_response = requests.get(search_url)
        search_data = search_response.json()
        
        if not search_data['items']:
            raise HTTPException(status_code=404, detail="Game not found")
        
        appid = search_data['items'][0]['id']
        
        # Obtener detalles del juego usando AppID
        details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=spanish"
        details_response = requests.get(details_url)
        details_data = details_response.json()
        
        if not details_data[str(appid)]['success']:
            raise HTTPException(status_code=404, detail="Game details not found")

        game_details = details_data[str(appid)]['data']
        
        # Obtener número de jugadores actuales
        players_url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
        players_response = requests.get(players_url)
        players_data = players_response.json()
        players_count = players_data.get('response', {}).get('player_count', 'N/A')

        # Extraer los datos requeridos
        game_info = {
            "titulo": game_details.get('name', 'N/A'),
            "web_del_producto": game_details.get('website', 'N/A'),
            "precio": game_details.get('price_overview', {}).get('final_formatted', 'Free') if game_details.get('is_free') is not True else 'Free',
            "descripcion": game_details.get('short_description', 'N/A'),
            "desarrollador": ", ".join(game_details.get('developers', ['N/A'])),
            "editor": ", ".join(game_details.get('publishers', ['N/A'])),
            "imagen": game_details.get('header_image', 'N/A'),
            "fecha_de_publicacion": game_details.get('release_date', {}).get('date', 'N/A'),
            "jugadores_actuales": players_count
        }
        
        return game_info
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching game details: " + str(e))
