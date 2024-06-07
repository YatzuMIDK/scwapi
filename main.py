from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from connect4.router import router as connect4_router
from steam.router import router as steam_router
from tiktok.router import router as tiktok_router
from name_combiner.router import router as name_combiner_router
from cheems.router import router as cheems_router
from wiki.router import router as wiki_router
from img.router import router as img_router
from ph_comment.router import router as ph_comment_router
from bj.router import router as bj_router
from tiempo.router import router as tiempo_router
import uvicorn
import time
import psutil

app = FastAPI()

# Registrar la hora de inicio
start_time = datetime.utcnow()

# Incluir los routers de Connect4, Steam, TikTok, Name Combiner y Cheems
app.include_router(connect4_router, prefix="/connect4", tags=["Connect4"])
app.include_router(steam_router, prefix="/steam", tags=["Steam"])
app.include_router(tiktok_router, prefix="/tiktok", tags=["TikTok"])
app.include_router(name_combiner_router, prefix="/name_combiner", tags=["NameCombiner"])
app.include_router(cheems_router, prefix="/cheems", tags=["Cheems"])
app.include_router(wiki_router, prefix="/wiki", tags=["Wiki"])
app.include_router(img_router, prefix="/img", tags=["Img"])
app.include_router(ph_comment_router, prefix="/ph_comment", tags=["PHComment"])
app.include_router(bj_router, prefix="/bj", tags=["Blackjack"])
app.include_router(tiempo_router, prefix="/tiempo", tags=["Time"])

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root(request: Request):
    current_time = datetime.utcnow()
    uptime = current_time - start_time
    uptime_str = str(uptime).split(".")[0]  # Eliminar microsegundos para una mejor presentación

    # Obtener todas las rutas disponibles
    routes = [route.path for route in app.routes if hasattr(route, "path")]

    # Obtener la latencia de la solicitud actual en segundos
    process_time = request.headers.get("X-Process-Time", "unknown")

    # Obtener el uso de CPU y RAM en MB
    process = psutil.Process()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = process.memory_info().rss / (1024 ** 2)  # Convertir bytes a MB

    return JSONResponse(content={
        "uptime": uptime_str,
        "dev": "@schwift.alv",
        "latency_seconds": process_time,
        "cpu_usage_percent": cpu_usage,
        "ram_usage_mb": ram_usage
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
