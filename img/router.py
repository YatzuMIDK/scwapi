from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageEnhance
import requests
from io import BytesIO

router = APIRouter()

@router.get("/generate_image")
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

        elif mode == 3:
            # URLs de las imágenes
            flag_url = "https://upload.wikimedia.org/wikipedia/commons/f/f3/Rainbow_flag_6_colors.svg"
            image_response = requests.get(avatar_url)
            flag_response = requests.get(flag_url)

            if image_response.status_code != 200:
                raise HTTPException(status_code=404, detail="Input image not found")
            if flag_response.status_code != 200:
                raise HTTPException(status_code=404, detail="Flag image not found")

            # Cargar las imágenes
            input_image = Image.open(BytesIO(image_response.content))
            flag_image = Image.open(BytesIO(flag_response.content)).convert("RGBA")

            # Redimensionar la imagen de la bandera para que coincida con la imagen de entrada
            flag_image = flag_image.resize(input_image.size, Image.ANTIALIAS)

            # Ajustar la opacidad de la bandera
            flag_opacity = 0.5  # Opacidad de la bandera (0.0 a 1.0)
            flag_image = ImageEnhance.Brightness(flag_image).enhance(flag_opacity)

            # Superponer la bandera en la imagen de entrada
            combined_image = Image.alpha_composite(input_image.convert("RGBA"), flag_image)

            # Guardar la imagen resultante en un buffer
            buffer = BytesIO()
            combined_image.save(buffer, format="PNG")
            buffer.seek(0)

            return StreamingResponse(buffer, media_type="image/png")

        else:
            raise HTTPException(status_code=400, detail="Invalid mode selected")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating image: " + str(e))
