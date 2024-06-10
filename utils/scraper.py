import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_player_info(player_name: str) -> dict:
    base_url = "https://www.transfermarkt.com"
    encoded_player_name = urllib.parse.quote(player_name)
    search_url = f"{base_url}/schnellsuche/ergebnis/schnellsuche?query={encoded_player_name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    try:
        player_link_tag = soup.find('a', {'class': 'spielprofil_tooltip'})
        if not player_link_tag:
            raise ValueError("No se encontró el enlace del jugador")
        
        player_link = player_link_tag['href']
        player_page = f"{base_url}{player_link}"
        
        response = requests.get(player_page, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        nombre = soup.find('h1', {'itemprop': 'name'})
        if not nombre:
            raise ValueError("No se encontró el nombre del jugador")
        nombre = nombre.text.strip()
        
        imagen_futbolista_tag = soup.find('img', {'class': 'bilderrahmen-fixed'})
        imagen_futbolista = imagen_futbolista_tag['src'] if imagen_futbolista_tag else ""
        
        club_tag = soup.find('a', {'class': 'vereinprofil_tooltip'})
        club = club_tag.text.strip() if club_tag else ""
        
        imagen_club_tag = club_tag.find('img') if club_tag else None
        imagen_club = imagen_club_tag['src'] if imagen_club_tag else ""
        
        valor_mercado_tag = soup.find('div', {'class': 'right-td'})
        valor_mercado = valor_mercado_tag.text.strip() if valor_mercado_tag else ""
        
        posición_tag = soup.find('div', string='Position:')
        posición = posición_tag.find_next_sibling('div').text.strip() if posición_tag else ""
        
        liga_tag = soup.find('span', {'class': 'hauptpunkt'}).find('a')
        liga = liga_tag.text.strip() if liga_tag else ""
        
        país_liga_tag = soup.find('img', {'class': 'flaggenrahmen'})
        país_liga = país_liga_tag['title'] if país_liga_tag else ""
        
        país_tag = soup.find('span', {'itemprop': 'nationality'})
        país = país_tag.text.strip() if país_tag else ""
        
        código_país_tag = país_tag.find_next_sibling('img') if país_tag else None
        código_país = código_país_tag['title'].lower() if código_país_tag else ""
        
        país_liga_img = soup.find('span', {'class': 'hauptpunkt'}).find_previous_sibling('img')
        código_país_liga = país_liga_img['title'].lower() if país_liga_img else ""
        
        player_info = {
            "nombre": nombre,
            "imagen_futbolista": imagen_futbolista,
            "club": club,
            "imagen_club": imagen_club,
            "valor_mercado": valor_mercado,
            "posición": posición,
            "liga": liga,
            "país_liga": país_liga,
            "código_país_liga": código_país_liga,
            "país": país,
            "código_país": código_país
        }
        
        return player_info
    except Exception as e:
        print(f"Error scraping Transfermarkt: {e}")
        return {}
