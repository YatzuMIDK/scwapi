from fastapi import APIRouter, HTTPException
import requests
import time

router = APIRouter()

STEAM_API_URL = "https://store.steampowered.com/api/appdetails"

def get_game_details(appid: int):
    response = requests.get(STEAM_API_URL, params={"appids": appid})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Steam API")
    
    data = response.json()
    if not data[str(appid)]["success"]:
        raise HTTPException(status_code=404, detail="Game not found")

    return data[str(appid)]["data"]

@router.get("/game/{appid}")
def get_game_info(appid: int):
    start_time = time.time()
    
    game_data = get_game_details(appid)
    
    end_time = time.time()
    latency = end_time - start_time

    title = game_data.get("name")
    url = f"https://store.steampowered.com/app/{appid}"
    price_overview = game_data.get("price_overview", {})
    price = price_overview.get("final_formatted", "Free")
    description = game_data.get("detailed_description")
    developer = ", ".join(game_data.get("developers", []))
    publisher = ", ".join(game_data.get("publishers", []))
    image = game_data.get("header_image")
    
    release_date = game_data.get("release_date", {}).get("date")
    if release_date:
        # Intentar convertir la fecha de lanzamiento a un timestamp UNIX
        try:
            release_timestamp = int(time.mktime(time.strptime(release_date, "%d %b, %Y")))
        except ValueError:
            release_timestamp = "Unknown"
    else:
        release_timestamp = "Unknown"

    size = game_data.get("size", "Unknown")  # Supongamos que el tamaño del juego se proporciona en algún campo llamado 'size'
    if size != "Unknown":
        size_in_mb = float(size) / (1024 * 1024)  # Convertir bytes a megabytes
    else:
        size_in_mb = "Unknown"

    # Aquí se debería traducir la descripción al español, se deja en inglés por simplicidad
    # En producción, se podría usar una biblioteca de traducción automática
    description_es = description  # Simplificación para mantener la misma descripción

    return {
        "titulo": title,
        "web": url,
        "precio": price,
        "descripcion": description_es,
        "desarrollador": developer,
        "editor": publisher,
        "imagen": image,
        "lanzado": release_timestamp,
        "peso": size_in_mb,
        "latency_ms": latency * 1000  # Convertir segundos a milisegundos
        }
