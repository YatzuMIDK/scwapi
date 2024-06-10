from fastapi import APIRouter, Response, HTTPException, Query
from easy_pil import Editor, Font
from io import BytesIO
import requests
import logging

router = APIRouter()

@router.get("/wlc")
def get_custom_image(
    avatar: str,
    user: str,
    background: str = "https://iili.io/JyT6hnn.jpg",  # Proporciona un valor predeterminado para el fondo
    txt1: str = "BIENVENIDO",
    txt2: str = "Disfruta tu estancia en el servidor",
    font_color: str = "white",
    circle_color: str = "white",
    sombra: str = "black"
):
    if not user:
        raise HTTPException(status_code=400, detail="El parámetro 'user' no puede estar vacío.")
    
    try:
        # Descargar la imagen del avatar
    avatar_response = requests.get(avatar)
    if avatar_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    avatar_image = Editor(BytesIO(avatar_response.content)).resize((200, 200)).circle_image()  # Tamaño del avatar

    # Descargar la imagen de fondo
    background_response = requests.get(background)
    if background_response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to download background image. Status code: {background_response.status_code}, Reason: {background_response.reason}")
    background_image = Editor(BytesIO(background_response.content)).resize((800, 400)).image  # Tamaño de la imagen de fondo

    # Cargar fuentes
    poppins = Font.montserrat(size=60, variant="bold")  # Tamaño de la fuente
    poppins_small = Font.montserrat(size=40, variant="regular")  # Tamaño de la fuente

    # Crear editor de imágenes
    editor = Editor(background_image)

    # Coordenadas centradas
    avatar_x = (800 - 200) // 2
    avatar_y = 50
    text_x = 400
    text_y1 = 270
    text_y2 = 320
    text_y3 = 370

    # Pegar el avatar en la imagen de fondo
    editor.paste(avatar_image.image, (avatar_x, avatar_y))  # Centrar avatar
    editor.ellipse((avatar_x, avatar_y), 200, 200, outline=circle_color, stroke_width=8)  # Círculo alrededor del avatar

    # Añadir texto a la imagen con efecto de sombra
    shadow_offset = 3
    editor.text((text_x + shadow_offset, text_y1 + shadow_offset), txt1, color=sombra, font=poppins, align="center")
    editor.text((text_x, text_y1), txt1, color=font_color, font=poppins, align="center")

    editor.text((text_x + shadow_offset, text_y2 + shadow_offset), user, color=sombra, font=poppins_small, align="center")
    editor.text((text_x, text_y2), user, color=font_color, font=poppins_small, align="center")

    editor.text((text_x + shadow_offset, text_y3 + shadow_offset), txt2, color=sombra, font=poppins_small, align="center")
    editor.text((text_x, text_y3), txt2, color=font_color, font=poppins_small, align="center")

    # Guardar la imagen en un buffer
    img_buffer = BytesIO()
    editor.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    # Devolver la imagen como respuesta
    return Response(content=img_buffer.getvalue(), media_type="image/png")

except Exception as e:
    logging.error(f"Error generating image: {e}")
    raise HTTPException(status_code=500, detail=str(e))
