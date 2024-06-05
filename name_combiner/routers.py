from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/combine/{name1}/{name2}")
def combine_names(name1: str, name2: str):
    combined_name = name1[:len(name1)//2] + name2[len(name2)//2:]
    compatibility = random.randint(50, 100)
    message = f"La compatibilidad entre {name1} y {name2} es del {compatibility}%."
    return {"combined_name": combined_name, "compatibility": compatibility, "message": message}
