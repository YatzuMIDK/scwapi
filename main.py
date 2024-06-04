from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from connect4.routers import router as connect4_router
from steam.routers import router as steam_router
import uvicorn

app = FastAPI()

# Registrar la hora de inicio
start_time = datetime.utcnow()

# Incluir los routers de Connect4 y Steam
app.include_router(connect4_router, prefix="/connect4", tags=["Connect4"])
app.include_router(steam_router, prefix="/steam", tags=["Steam"])

@app.get("/")
async def root():
    current_time = datetime.utcnow()
    uptime = current_time - start_time
    uptime_str = str(uptime).split(".")[0]  # Eliminar microsegundos para una mejor presentación

    # Obtener todas las rutas disponibles
    routes = []
    for route in app.routes:
        if hasattr(route, "path"):
            routes.append(route.path)

    return JSONResponse(content={"uptime": uptime_str, "endpoints": routes})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
