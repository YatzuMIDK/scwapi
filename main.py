from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from ocr.router import router as ocr_router
from casino.router import router as casino_router
from steam.router import router as steam_router
from urban.router import router as urban_router
from name_combiner.router import router as name_combiner_router
from cheems.router import router as cheems_router
from traducir.router import router as traducir_router
from ship.router import router as ship_router
from tiempo.router import router as tiempo_router
from img.router import router as img_router
from gw.router import router as gw_router
from bj.router import router as bj_router 
from pvp.router import router as pvp_router
import uvicorn
import time
import psutil

app = FastAPI()

# Registrar la hora de inicio
start_time = datetime.utcnow()

# Incluir los routers de Connect4, Steam, TikTok, Name Combiner y Cheems
app.include_router(ocr_router, prefix="/combat", tags=["Combate"])
app.include_router(casino_router, prefix="/casino", tags=["casino"])
app.include_router(steam_router, prefix="/steam", tags=["Steam"])
app.include_router(urban_router, prefix="/urban", tags=["Urban"])
app.include_router(name_combiner_router, prefix="/name_combiner", tags=["NameCombiner"])
app.include_router(cheems_router, prefix="/cheems", tags=["Cheems"])
app.include_router(traducir_router, prefix="/traducir", tags=["Traducir"])
app.include_router(ship_router, prefix="/ship", tags=["Shipeo"])
app.include_router(tiempo_router, prefix="/tiempo", tags=["Time"])
app.include_router(img_router, prefix="/img", tags=["Imagenes"])
app.include_router(gw_router, prefix="/gw", tags=["Sorteo"])
app.include_router(bj_router, prefix="/buscaminas", tags=["Putazos"])
app.include_router(pvp_router, prefix="/race", tags=["Carrera"])
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
        "cpu_usage_percent": cpu_usage,
        "ram_usage_mb": ram_usage
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
