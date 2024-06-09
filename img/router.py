from fastapi import APIRouter, Response, HTTPException
from easy_pil import Editor, Font
from io import BytesIO
import requests
import logging

router = APIRouter()

@router.get("/welcomecard/")
def get_custom_image(avatar: str, background: str, ctx1: str="BIENVENIDO", ctx2: str="user", ctx3: str="Disfruta tu estancia en el servidor"):
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
        editor.ellipse((250 + horizontal_shift, 90), 150, 150, outline="white", stroke_width=5)

        # Añadir texto a la imagen
        editor.text((320 + horizontal_shift, 260), ctx1, color="white", font=poppins, align="center")
        editor.text((320 + horizontal_shift, 315), ctx2, color="white", font=poppins_small, align="center")
        editor.text((320 + horizontal_shift, 350), ctx3, color="white", font=poppins_small, align="center")

        # Guardar la imagen en un buffer
        img_buffer = BytesIO()
        editor.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Devolver la imagen como respuesta
        return Response(content=img_buffer.getvalue(), media_type="image/png")

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))
