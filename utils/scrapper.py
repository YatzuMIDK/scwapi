import requests
from bs4 import BeautifulSoup

def get_player_info(player_name: str) -> dict:
    base_url = "https://www.transfermarkt.com"
    search_url = f"{base_url}/schnellsuche/ergebnis/schnellsuche?query={player_name}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Encuentra el primer resultado de búsqueda
    try:
        player_link = soup.find('a', {'class': 'spielprofil_tooltip'})['href']
        player_page = f"{base_url}{player_link}"
        
        response = requests.get(player_page, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer información del jugador
        nombre = soup.find('h1', {'itemprop': 'name'}).text.strip()
        imagen_futbolista = soup.find('img', {'class': 'bilderrahmen-fixed'})['src']
        club = soup.find('a', {'class': 'vereinprofil_tooltip'}).text.strip()
        imagen_club = soup.find('a', {'class': 'vereinprofil_tooltip'}).find('img')['src']
        valor_mercado = soup.find('div', {'class': 'right-td'}).text.strip()
        posición = soup.find('div', string='Position:').find_next_sibling('div').text.strip()
        liga = soup.find('span', {'class': 'hauptpunkt'}).find('a').text.strip()
        país_liga = soup.find('img', {'class': 'flaggenrahmen'})['title']
        país = soup.find('span', {'itemprop': 'nationality'}).text.strip()
        código_país = soup.find('span', {'itemprop': 'nationality'}).find_next_sibling('img')['title'].lower()
        
        # Obtener código del país de la liga
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
