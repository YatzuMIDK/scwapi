from fastapi import APIRouter, HTTPException
from TikTokApi import TikTokApi

router = APIRouter()

@router.get("/profile/{username}")
def get_tiktok_profile(username: str):
    api = TikTokApi.get_instance()
    try:
        user = api.get_user(username)
        user_info = user.info_full()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return {
        "username": user_info.get('uniqueId'),
        "nickname": user_info.get('nickname'),
        "followers_count": user_info.get('followerCount'),
        "following_count": user_info.get('followingCount'),
        "likes_count": user_info.get('heartCount'),
        "videos_count": user_info.get('videoCount'),
        "bio": user_info.get('signature'),
        "profile_image_url": user_info.get('avatarLarger')
    }
