from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime

router = APIRouter()

@router.get("/pefil/{username}")
def get_roblox_profile(username: str):
    # Obtener la información del usuario por nombre de usuario
    user_url = f"https://api.roblox.com/users/get-by-username?username={username}"
    user_response = requests.get(user_url)
    
    if user_response.status_code != 200 or "Id" not in user_response.json():
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user_response.json()
    user_id = user_data["Id"]
    
    # Obtener la información del perfil del usuario
    profile_url = f"https://users.roblox.com/v1/users/{user_id}"
    profile_response = requests.get(profile_url)
    
    if profile_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile_data = profile_response.json()
    
    # Obtener información adicional
    friends_url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
    friends_response = requests.get(friends_url)
    friends_count = friends_response.json().get("count", 0)

    followers_url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
    followers_response = requests.get(followers_url)
    followers_count = followers_response.json().get("count", 0)

    following_url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
    following_response = requests.get(following_url)
    following_count = following_response.json().get("count", 0)

    avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false"
    avatar_response = requests.get(avatar_url)
    avatar_image = avatar_response.json().get("data", [{}])[0].get("imageUrl", "")

    return {
        "usuario": profile_data.get("name"),
        "apodo": profile_data.get("displayName"),
        "creado": datetime.strptime(profile_data.get("created"), "%Y-%m-%dT%H:%M:%S.%fZ").timestamp(),
        "conectado": profile_data.get("isOnline"),
        "baneado": profile_data.get("isBanned"),
        "amigos": friends_count,
        "seguidores": followers_count,
        "siguiendo": following_count,
        "avatar": avatar_image
    }
