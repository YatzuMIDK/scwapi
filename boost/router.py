from fastapi import FastAPI, Header, HTTPException
from typing import Dict

app = FastAPI()

# Simulación de una base de datos de usuarios mejorando servidores de Discord
boosted_servers = {
    "server1": {"boosters": ["user1", "user2", "user3"], "boosts": 3},
    "server2": {"boosters": ["user4", "user5"], "boosts": 2},
    "server3": {"boosters": ["user6"], "boosts": 1}
}

# Función para verificar el token del bot
def verify_bot_token(token: str = Header(...)):
    # Aquí puedes agregar la lógica para verificar el token del bot
    # Por ahora, solo se verifica si el token no está vacío
    if not token:
        raise HTTPException(status_code=401, detail="Token del bot no proporcionado o inválido")

# Endpoint para obtener la información de los usuarios mejorando un servidor de Discord
@app.get("/server/{server_id}")
async def get_boosted_servers(server_id: str, token: str = Header(...)):
    # Verificar el token del bot
    verify_bot_token(token)
    
    # Verificar si el servidor existe en la base de datos
    if server_id not in boosted_servers:
        raise HTTPException(status_code=404, detail="Servidor no encontrado")
    
    # Obtener la información del servidor
    server_info = boosted_servers[server_id]
    
    # Devolver la información del servidor
    return {
        "server_id": server_id,
        "boosters": server_info["boosters"],
        "boosts": server_info["boosts"]
    }
