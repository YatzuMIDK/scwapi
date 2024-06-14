from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from PIL import Image
from io import BytesIO
import pytesseract

router = APIRouter()

class ImageUrl(BaseModel):
    url: str

@router.post("/recognize-text/")
async def recognize_text(image_url: ImageUrl):
    try:
        response = requests.get(image_url.url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa

        image = Image.open(BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        
        return {"text": text}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching the image: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {e}")
