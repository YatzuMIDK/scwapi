from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from PIL import Image
import requests
from io import BytesIO

router = APIRouter()

@router.get("/gen")
def generate_image(avatar_url: str, mode: int = 1):
    try:
        if mode == 1:
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

        elif mode == 2:
            # URLs de las imágenes
            bg_url = "https://cdn.discordapp.com/attachments/560593330270896129/1113902772740427847/e3b05e47a826212e51ecb7aeda31a39240d3ccd6.gif?ex=6650390c&is=664ee78c&hm=b89ff022c38e0a06db670d1d6e5d4138e84107f5e2a5a4719617bb4bd7b8193a&"
            image_response = requests.get(avatar_url)

            if image_response.status_code != 200:
                raise HTTPException(status_code=404, detail="Image not found")

            # Cargar las imágenes
            bg_image = Image.open(requests.get(bg_url, stream=True).raw)
            image = Image.open(BytesIO(image_response.content))

            # Obtener dimensiones de la imagen de entrada
            w, h = image.size

            # Contener la imagen de fondo en las dimensiones de la imagen de entrada
            bg_image.thumbnail((w, h), Image.ANTIALIAS)

            # Obtener nuevas dimensiones de la imagen de fondo
            ow, oh = bg_image.size

            # Superponer la imagen de fondo centrada en la imagen de entrada
            image.paste(bg_image, ((w - ow) // 2, (h - oh) // 2), bg_image)

            # Guardar la imagen resultante en un buffer
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            return StreamingResponse(buffer, media_type="image/png")

        else:
            raise HTTPException(status_code=400, detail="Invalid mode selected")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating image: " + str(e))
