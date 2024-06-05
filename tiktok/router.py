from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/profile/{username}")
def get_tiktok_profile(username: str):
    try:
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Profile not found")

        soup = BeautifulSoup(response.text, 'html.parser')
        user_info = {}

        # Extract profile data
        user_info["username"] = username
        user_info["nickname"] = soup.find("h1", {"data-e2e": "user-title"}).text if soup.find("h1", {"data-e2e": "user-title"}) else ""
        user_info["bio"] = soup.find("h2", {"data-e2e": "user-bio"}).text if soup.find("h2", {"data-e2e": "user-bio"}) else ""
        user_info["followers"] = soup.find("strong", {"title": "Followers"}).text if soup.find("strong", {"title": "Followers"}) else ""
        user_info["following"] = soup.find("strong", {"title": "Following"}).text if soup.find("strong", {"title": "Following"}) else ""
        user_info["likes"] = soup.find("strong", {"title": "Likes"}).text if soup.find("strong", {"title": "Likes"}) else ""
        user_info["avatar"] = soup.find("img", {"class": "avatar"})['src'] if soup.find("img", {"class": "avatar"}) else ""

        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching profile details: " + str(e))
