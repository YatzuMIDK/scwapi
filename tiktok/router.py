from fastapi import APIRouter, HTTPException
import httpx
from datetime import datetime

router = APIRouter()

@router.get("/profile/{username}")
async def get_tiktok_profile(username: str):
    async with httpx.AsyncClient() as client:
        profile_url = f"https://www.tiktok.com/@{username}"
        response = await client.get(profile_url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="User not found")

        # Parsing the TikTok profile page to extract information
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            user_data_script = soup.find('script', id='__NEXT_DATA__')
            user_data_json = user_data_script.string
            user_data = json.loads(user_data_json)
            user_info = user_data['props']['pageProps']['userInfo']

            # Extract user information
            user = user_info['user']
            stats = user_info['stats']

            return {
                "username": user.get("uniqueId"),
                "nickname": user.get("nickname"),
                "verified": user.get("verified"),
                "bio": user.get("signature"),
                "followers": stats.get("followerCount"),
                "following": stats.get("followingCount"),
                "likes": stats.get("heartCount"),
                "videos": stats.get("videoCount"),
                "avatar": user.get("avatarThumb"),
                "created_at": user.get("createTime")
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error parsing profile information")
