from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from googletrans import Translator, LANGUAGES

router = APIRouter()
translator = Translator()

class TranslationResponse(BaseModel):
    texto: str
    traduccion: str
    source_lang: str
    target_lang: str

@router.get("/", response_model=TranslationResponse)
def translate_text(
    texto: str = Query(..., description="Text to translate"),
    target_lang: str = Query(..., description="Target language code (e.g., 'es' for Spanish)")
):
    try:
        # Validar si el idioma de destino es válido
        if target_lang not in LANGUAGES:
            raise HTTPException(status_code=400, detail="Invalid target language code")

        # Realizar la traducción
        traduccion = translator.translate(texto, dest=target_lang)
        
        return TranslationResponse(
            texto=texto,
            traduccion=traduccion.text,
            source_lang=traduccion.src,
            target_lang=target_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
