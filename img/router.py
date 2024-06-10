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
    circle_color: str = "white"
):
    try:
        # Descargar la imagen del avatar
        avatar_response = requests.get(avatar)
        if avatar_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download avatar image.")
        avatar_image = Editor(BytesIO(avatar_response.content)).resize((150, 150)).circle_image()

        # Descargar la imagen de fondo
        background_response = requests.get(background)
        if background_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download background image. Status code: {background_response.status_code}, Reason: {background_response.reason}")
        background_image = Editor(BytesIO(background_response.content)).resize((800, 400)).image

        # Cargar fuentes
        poppins = Font.montserrat(size=50, variant="bold")
        poppins_small = Font.montserrat(size=25, variant="regular")

        # Desplazamiento horizontal para centrar el contenido
        horizontal_shift = 63

        # Crear editor de imágenes
        editor = Editor(background_image)

        # Pegar el avatar en la imagen de fondo
        editor.paste(avatar_image.image, (250 + horizontal_shift, 90))
        editor.ellipse((250 + horizontal_shift, 90), 150, 150, outline=circle_color, stroke_width=5)

        # Añadir texto a la imagen con efecto de sombra
        shadow_offset = 3
        editor.text((320 + horizontal_shift + shadow_offset, 260 + shadow_offset), txt1, color="black", font=poppins, align="center")
        editor.text((320 + horizontal_shift, 260), txt1, color=font_color, font=poppins, align="center")

        editor.text((320 + horizontal_shift + shadow_offset, 315 + shadow_offset), user, color="black", font=poppins_small, align="center")
        editor.text((320 + horizontal_shift, 315), user, color=font_color, font=poppins_small, align="center")

        editor.text((320 + horizontal_shift + shadow_offset, 350 + shadow_offset), txt2, color="black", font=poppins_small, align="center")
        editor.text((320 + horizontal_shift, 350), txt2, color=font_color, font=poppins_small, align="center")

        # Guardar la imagen en un buffer
        img_buffer = BytesIO()
        editor.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Devolver la imagen como respuesta
        return Response(content=img_buffer.getvalue(), media_type="image/png")

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))
