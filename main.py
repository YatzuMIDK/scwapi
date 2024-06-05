from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from connect4.routers import router as connect4_router
from steam.routers import router as steam_router
from tiktok.routers import router as tiktok_router
import uvicorn
import time
import psutil

app = FastAPI()

# Registrar la hora de inicio
start_time = datetime.utcnow()

# Incluir los routers de Connect4, Steam y TikTok
app.include_router(connect4_router, prefix="/connect4", tags=["Connect4"])
app.include_router(steam_router, prefix="/steam", tags=["Steam"])
app.include_router(tiktok_router, prefix="/tiktok", tags=["TikTok"])

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

    # Obtener el uso de CPU y RAM
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    ram_usage = memory_info.percent

    return JSONResponse(content={
        "uptime": uptime_str,
        "endpoints": routes,
        "latency_seconds": process_time,
        "cpu_usage_percent": cpu_usage,
        "ram_usage_percent": ram_usage
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
