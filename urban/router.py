from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageEnhance
import requests
from io import BytesIO

router = APIRouter()

@router.post("/overlay")
async def overlay_image(background_url: str, opacity: float = 0.5):
    try:
        # Cargar la imagen de fondo desde la URL
        response = requests.get(background_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Cannot download background image")

        background = Image.open(BytesIO(response.content))

        # Cargar la imagen superpuesta
        overlay_url = "https://i.postimg.cc/BQst1zJk/images-5.png"
        response = requests.get(overlay_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Cannot download overlay image")

        overlay = Image.open(BytesIO(response.content)).convert("RGBA")

        # Redimensionar la imagen superpuesta para que coincida con el tamaño de la imagen de fondo
        overlay = overlay.resize(background.size)

        # Ajustar la opacidad de la imagen superpuesta
        alpha = overlay.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        overlay.putalpha(alpha)

        # Superponer la imagen
        combined = Image.alpha_composite(background.convert("RGBA"), overlay)

        # Guardar la imagen resultante en un buffer
        buffer = BytesIO()
        combined.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
