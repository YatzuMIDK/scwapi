from PIL import Image, ImageDraw, ImageFont
import requests
import os

def generate_ph_comment(username: str, comment: str, avatar_url: str) -> str:
    # Cargar la fuente
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        raise Exception("Font path not found")
    font = ImageFont.truetype(font_path, 16)
    small_font = ImageFont.truetype(font_path, 12)
    
    # Crear una imagen en blanco
    img = Image.new('RGB', (500, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Descargar y pegar el avatar
    response = requests.get(avatar_url, stream=True)
    response.raise_for_status()
    avatar = Image.open(response.raw).resize((50, 50))
    img.paste(avatar, (10, 10))

    # Agregar el nombre de usuario y el comentario
    d.text((70, 10), username, font=font, fill=(0, 0, 0))
    d.text((70, 40), comment, font=small_font, fill=(0, 0, 0))

    # Guardar la imagen
    file_path = f"comment_{username}.png"
    img.save(file_path)

    return file_path
