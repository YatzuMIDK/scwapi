from fastapi import APIRouter, HTTPException
import wikipediaapi
import requests

router = APIRouter()

@router.get("/buscar/{query}")
def search_wikipedia(query: str):
    wiki_wiki = wikipediaapi.Wikipedia('es')
    page = wiki_wiki.page(query)

    if not page.exists():
        raise HTTPException(status_code=404, detail="Page not found")

    summary = page.summary[0:500] + "..."  # Obtener los primeros 500 caracteres del resumen

    # Buscar una imagen relacionada utilizando la API de Wikimedia
    image_url = None
    response = requests.get(f"https://es.wikipedia.org/api/rest_v1/page/summary/{query}")

    if response.status_code == 200:
        data = response.json()
        if "thumbnail" in data and "source" in data["thumbnail"]:
            image_url = data["thumbnail"]["source"]

    return {"datos": summary, "imagen": image_url}
