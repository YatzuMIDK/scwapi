from fastapi import APIRouter, HTTPException, Query
from PIL import Image
import requests
from io import BytesIO

router = APIRouter()

@router.get("/gen")
def generate_image(avatar_url: str):
    try:
        # URLs de las imágenes
        bg_url = "https://cdn.discordapp.com/attachments/1187251830728708146/1229987656461451345/image_2024-04-16_225148457.png?ex=6661cd05&is=66607b85&hm=3ceaa6a47cde5304ad5134f81d5a8fa689234b4e96dfad01408484b8edd8d886&"
        avatar_response = requests.get(avatar_url)

        if avatar_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Avatar image not found")

        # Cargar las imágenes
        bg_image = Image.open(requests.get(bg_url, stream=True).raw)
        avatar_image = Image.open(BytesIO(avatar_response.content))

        # Redimensionar la imagen del avatar
        avatar_image = avatar_image.resize((491, 292))

        # Superponer el avatar en la imagen de fondo
        bg_image.paste(avatar_image, (10, 4), avatar_image)

        # Guardar la imagen resultante en un buffer
        buffer = BytesIO()
        bg_image.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating image: " + str(e))
