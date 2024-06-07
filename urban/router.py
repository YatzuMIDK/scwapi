from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import requests
from googletrans import Translator

router = APIRouter()
translator = Translator()

class UrbanDefinitionResponse(BaseModel):
    word: str
    definition: str
    example: str

@router.get("/define", response_model=UrbanDefinitionResponse)
def define_word(word: str = Query(..., description="Word to define in Urban Dictionary")):
    try:
        # Buscar la definición en Urban Dictionary
        response = requests.get(f"https://api.urbandictionary.com/v0/define?term={word}")
        data = response.json()

        if not data["list"]:
            raise HTTPException(status_code=404, detail="La palabra no existe en el urban dictionary")

        # Obtener la primera definición
        definition = data["list"][0]["definition"]
        example = data["list"][0]["example"]

        # Traducir la definición y el ejemplo al español
        translated_definition = translator.translate(definition, dest='es').text
        translated_example = translator.translate(example, dest='es').text

        return UrbanDefinitionResponse(
            word=word,
            definition=translated_definition,
            example=translated_example
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
