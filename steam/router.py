from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup
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

def search_game_id(game_name: str):
    search_url = f"https://store.steampowered.com/search/?term={game_name}"
    response = requests.get(search_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error searching for game")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('a', class_='search_result_row')
    
    if result:
        game_url = result['href']
        appid = game_url.split('/')[-2]
        return int(appid)
    else:
        raise HTTPException(status_code=404, detail="Game not found")

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
        try:
            release_timestamp = int(time.mktime(time.strptime(release_date, "%d %b, %Y")))
        except ValueError:
            release_timestamp = "Unknown"
    else:
        release_timestamp = "Unknown"

    size = game_data.get("size", "Unknown")
    if size != "Unknown":
        size_in_mb = float(size) / (1024 * 1024)
    else:
        size_in_mb = "Unknown"

    description_es = description

    return {
        "title": title,
        "product_url": url,
        "price": price,
        "description_es": description_es,
        "developer": developer,
        "publisher": publisher,
        "image": image,
        "release_date_unix": release_timestamp,
        "size_mb": size_in_mb,
        "latency_ms": latency * 1000
    }

@router.get("/search/{game_name}")
def search_game(game_name: str):
    appid = search_game_id(game_name)
    return get_game_info(appid)
