from easy_pil import Editor, Font
from io import BytesIO
from fastapi import APIRouter, Response, HTTPException
import requests

router = APIRouter()

@router.get("/")
def image(avatar1: str, avatar2: str, num: int, bg_url: str = None):

    if bg_url is None:
        background_path = "https://i.postimg.cc/KzJQfnpL/images-2024-06-07-T022236-205.jpg"
    else:
        background_response = requests.get(bg_url)
        if background_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download background image.")
        background_image = BytesIO(background_response.content)
        background_path = background_image

    poppins = Font.poppins(size=80)
    gen = Editor(background_path).resize((900, 300))

    avatar_response = requests.get(avatar1)
    if avatar_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    profile = Editor(BytesIO(avatar_response.content)).resize((200, 200)).circle_image()

    avatar_response_2 = requests.get(avatar2)
    if avatar_response_2.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    profile_2 = Editor(BytesIO(avatar_response_2.content)).resize((200, 200)).circle_image()

    corazon = Editor("img/cora.png").resize((240, 240))

    gen.paste(corazon, (330, 36))
    gen.text((380, 110), f"{num}%", font=poppins, color="white")
    gen.paste(profile, (100, 50))
    gen.ellipse((100, 50), 200, 200, outline="red", stroke_width=4)
    gen.paste(profile_2, (600, 50))
    gen.ellipse((600, 50), 200, 200, outline="red", stroke_width=4)

    img_buffer = BytesIO()
    gen.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return Response(content=img_buffer.getvalue(), media_type="image/png")
