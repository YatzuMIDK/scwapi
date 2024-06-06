from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/profile/{username}")
def get_tiktok_profile(username: str):
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, como Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Profile not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        user_info = {}

        # Extract profile data using more robust selectors
        user_info["username"] = username
        user_info["nickname"] = soup.find("h1", {"data-e2e": "user-title"}).text if soup.find("h1", {"data-e2e": "user-title"}) else ""
        user_info["bio"] = soup.find("h2", {"data-e2e": "user-bio"}).text if soup.find("h2", {"data-e2e": "user-bio"}) else ""
        
        followers_elem = soup.find("strong", {"title": "Followers"})
        user_info["followers"] = followers_elem.text if followers_elem else ""

        following_elem = soup.find("strong", {"title": "Following"})
        user_info["following"] = following_elem.text if following_elem else ""

        likes_elem = soup.find("strong", {"title": "Likes"})
        user_info["likes"] = likes_elem.text if likes_elem else ""

        avatar_elem = soup.find("img", {"class": "avatar"})
        user_info["avatar"] = avatar_elem['src'] if avatar_elem else ""

        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching profile details: " + str(e))
