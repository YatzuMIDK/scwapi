from easy_pil import Editor, Font
from io import BytesIO
from fastapi import APIRouter, Response, HTTPException
import requests
import random
from PIL import Image, ImageDraw

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
    corazon = Editor("img/cora.png").resize((240, 260))

    # Dibujar el rectángulo con bordes circulares
    rect_width, rect_height = 750, 250  # Ajustar el tamaño del rectángulo
    rect_color = (0, 0, 0, 230)  # Color negro más oscuro semi-transparente
    rect_radius = 30

    # Calcular la posición para centrar el rectángulo
    image_width, image_height = gen.image.size
    rect_x = (image_width - rect_width) // 2
    rect_y = (image_height - rect_height) // 2

    # Crear una nueva imagen para el rectángulo con bordes redondeados
    rectangle_img = Image.new('RGBA', (rect_width, rect_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle_img)
    
    # Dibuja un rectángulo con bordes redondeados
    def round_rectangle(draw, xy, rad, fill=None):
        x1, y1, x2, y2 = xy
        draw.rectangle([x1 + rad, y1, x2 - rad, y2], fill=fill)
        draw.rectangle([x1, y1 + rad, x2, y2 - rad], fill=fill)
        draw.pieslice([x1, y1, x1 + rad * 2, y1 + rad * 2], 180, 270, fill=fill)
        draw.pieslice([x2 - rad * 2, y1, x2, y1 + rad * 2], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - rad * 2, x1 + rad * 2, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - rad * 2, y2 - rad * 2, x2, y2], 0, 90, fill=fill)

    round_rectangle(draw, [0, 0, rect_width, rect_height], rect_radius, fill=rect_color)

    # Pegar el rectángulo en la imagen de fondo
    gen.image.paste(rectangle_img, (rect_x, rect_y), mask=rectangle_img)

    # Agregar el corazón y el texto
    gen.paste(corazon, (330, 36))
    gen.text((380, 110), f"{num}%", font=poppins, color="white")
    
    # Agregar los avatares
    gen.paste(profile, (100, 50))
    gen.ellipse((100, 50), 200, 200, outline="magenta", stroke_width=4)
    gen.paste(profile_2, (600, 50))
    gen.ellipse((600, 50), 200, 200, outline="magenta", stroke_width=4)

    # Convertir la imagen en bytes y devolverla como respuesta
    img_buffer = BytesIO()
    gen.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

    return Response(content=img_buffer.getvalue(), media_type="image/png")
