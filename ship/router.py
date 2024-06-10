from easy_pil import Editor, Font, Canvas
from io import BytesIO
from fastapi import APIRouter, Response, HTTPException
import requests
import random

router = APIRouter()

@router.get("/")
def image(avatar1: str, avatar2: str, num: int = None, bg_url: str = None):
    # Generar un número aleatorio si num no está proporcionado
    if num is None:
        num = random.randint(1, 100)

    # Descargar y preparar la imagen de fondo
    if bg_url is None:
        background_path = "img/bg_ship.jpg"
    else:
        background_response = requests.get(bg_url)
        if background_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download background image.")
        background_image = BytesIO(background_response.content)
        background_path = background_image

    # Preparar fuentes y editor
    poppins = Font.poppins(size=80)
    gen = Editor(background_path).resize((900, 300))

    # Descargar y preparar avatares
    avatar_response = requests.get(avatar1)
    if avatar_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    profile = Editor(BytesIO(avatar_response.content)).resize((200, 200)).circle_image()

    avatar_response_2 = requests.get(avatar2)
    if avatar_response_2.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    profile_2 = Editor(BytesIO(avatar_response_2.content)).resize((200, 200)).circle_image()

    # Corazón
    corazon = Editor("img/cora.png").resize((240, 240))

    # Dibujar el rectángulo con bordes circulares
    rect_width, rect_height = 500, 150
    rect_x, rect_y = (gen.image.width - rect_width) // 2, 125
    rect_color = (0, 0, 0, 150)  # Color negro semi-transparente
    rect_radius = 30

    canvas = Canvas((rect_width, rect_height), color=rect_color)
    canvas.rectangle((0, 0, rect_width, rect_height), radius=rect_radius)

    gen.paste(canvas, (rect_x, rect_y), canvas.image)

    # Agregar el corazón y el texto
    gen.paste(corazon, (330, 36))
    gen.text((380, 110), f"{num}%", font=poppins, color="white")
    
    # Agregar los avatares
    gen.paste(profile, (100, 50))
    gen.ellipse((100, 50), 200, 200, outline="red", stroke_width=4)
    gen.paste(profile_2, (600, 50))
    gen.ellipse((600, 50), 200, 200, outline="red", stroke_width=4)

    # Convertir la imagen en bytes y devolverla como respuesta
    img_buffer = BytesIO()
    gen.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return Response(content=img_buffer.getvalue(), media_type="image/png")
