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
        if (avatar_response.status_code != 200):
            raise HTTPException(status_code=400, detail="Failed to download avatar image.")
        avatar_image = Editor(BytesIO(avatar_response.content)).resize((600, 600)).circle_image()  # Aumentar tamaño del avatar

        # Descargar la imagen de fondo
        background_response = requests.get(background)
        if (background_response.status_code != 200):
            raise HTTPException(status_code=400, detail=f"Failed to download background image. Status code: {background_response.status_code}, Reason: {background_response.reason}")
        background_image = Editor(BytesIO(background_response.content)).resize((800, 400)).image  # Aumentar tamaño de la imagen de fondo

        # Cargar fuentes
        poppins = Font.montserrat(size=80, variant="bold")  # Aumentar tamaño de la fuente
        poppins_small = Font.montserrat(size=50, variant="regular")  # Aumentar tamaño de la fuente

        # Desplazamiento horizontal para centrar el contenido
        horizontal_shift = 63

        # Crear editor de imágenes
        editor = Editor(background_image)

        # Pegar el avatar en la imagen de fondo
        editor.paste(avatar_image.image, (750 + horizontal_shift, 100))  # Ajustar coordenadas
        editor.ellipse((750 + horizontal_shift, 100), 600, 600, outline=circle_color, stroke_width=10)  # Aumentar tamaño del círculo

        # Añadir texto a la imagen con efecto de sombra
        shadow_offset = 3
        editor.text((750 + horizontal_shift + shadow_offset, 550 + shadow_offset), txt1, color=sombra, font=poppins, align="center")
        editor.text((750 + horizontal_shift, 450), txt1, color=font_color, font=poppins, align="center")

        editor.text((750 + horizontal_shift + shadow_offset, 550 + shadow_offset), user, color=sombra, font=poppins_small, align="center")
        editor.text((750 + horizontal_shift, 550), user, color=font_color, font=poppins_small, align="center")

        editor.text((600 + horizontal_shift + shadow_offset, 620 + shadow_offset), txt2, color=sombra, font=poppins_small, align="center")
        editor.text((600 + horizontal_shift, 620), txt2, color=font_color, font=poppins_small, align="center")

        # Guardar la imagen en un buffer
        img_buffer = BytesIO()
        editor.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Devolver la imagen como respuesta
        return Response(content=img_buffer.getvalue(), media_type="image/png")

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))
