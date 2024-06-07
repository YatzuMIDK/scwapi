from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from .ph_comment import generate_ph_comment

router = APIRouter()

class CommentRequest(BaseModel):
    username: str
    comment: str
    avatar_url: str

@router.post("/create_comment_image")
async def create_comment_image(request: CommentRequest):
    try:
        file_path = generate_ph_comment(request.username, request.comment, request.avatar_url)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="Error generating image")
        return {"image_url": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
