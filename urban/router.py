from fastapi import APIRouter, HTTPException
import requests
import re
from bs4 import BeautifulSoup
from googletrans import Translator

router = APIRouter()

@router.get("/define")
async def define_word(word: str):
    try:
        # URL de Urban Dictionary para buscar la palabra
        url = f"https://www.urbandictionary.com/define.php?term={word}"
        
        # Hacer la solicitud a Urban Dictionary
        response = requests.get(url)
        
        # Comprobar si la solicitud fue exitosa
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al obtener la definición de Urban Dictionary")

        # Parsear la respuesta HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # Extraer la definición
        meaning_div = soup.find("div", {"class": "meaning"})
        if not meaning_div:
            raise HTTPException(status_code=404, detail="Definición no encontrada")

        # Extraer el texto de la definición
        definition = meaning_div.text.strip()

        # Extraer el ejemplo
        example_div = soup.find("div", {"class": "example"})
        if not example_div:
            example = ""
        else:
            example = example_div.text.strip()

        # Traducir la definición y el ejemplo al español
        translator = Translator()
        translated_definition = translator.translate(definition, dest='es').text
        translated_example = translator.translate(example, dest='es').text if example else ""

        return {
            "word": word,
            "definition": translated_definition,
            "example": translated_example
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
