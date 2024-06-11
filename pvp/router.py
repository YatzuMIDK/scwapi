from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

class Game(BaseModel):
    game_id: int
    player_health: int = 200
    machine_health: int = 200
    winner: str = None
    player_move: str = None
    machine_move: str = None
    status: str = None

moves = {
    "Puñetazo": {"probability": 0.1, "damage": 20},
    "Corte superior": {"probability": 0.2, "damage": 30},
    "Patada baja": {"probability": 0.15, "damage": 25},
    "Super golpe": {"probability": 0.05, "damage": 40},
    "Cabezazo": {"probability": 0.1, "damage": 35}
}

def attack(player_move: str) -> int:
    if player_move not in moves:
        raise HTTPException(status_code=400, detail="Movimiento no válido")

    if random.random() < moves[player_move]["probability"]:
        return moves[player_move]["damage"]
    else:
        return 0

@app.post("/start_game")
async def start_game():
    game_id = random.randint(1, 1000)  # Generar un ID de juego aleatorio
    return {"game_id": game_id}

@app.post("/fight/{game_id}")
async def player_attack(game_id: int, player_move: str):
    game = Game(game_id=game_id)
    game.player_move = player_move
    damage = attack(player_move)

    game.machine_move = random.choice(list(moves.keys()))
    machine_damage = attack(game.machine_move)

    game.machine_health -= damage
    game.player_health -= machine_damage

    if game.machine_health <= 0:
        game.winner = "Jugador"
        game.status = f"¡La máquina ha perdido! El jugador gana con {game.player_health} de salud restante."
    elif game.player_health <= 0:
        game.winner = "Máquina"
        game.status = f"¡El jugador ha perdido! La máquina gana con {game.machine_health} de salud restante."
    else:
        game.status = f"El jugador usó {player_move} y {game.machine_move} la máquina. Salud del jugador: {game.player_health}, Salud de la máquina: {game.machine_health}"

    return game

@app.get("/game_info/{game_id}")
async def get_game_info(game_id: int):
    # Aquí deberías tener una lógica para recuperar el estado del juego del almacenamiento de datos
    # Por ahora, simplemente devolvemos un juego ficticio
    return {
        "game_id": game_id,
        "player_health": 200,
        "machine_health": 200,
        "winner": None,
        "player_move": "Puñetazo",
        "machine_move": "Corte superior",
        "status": "La partida está en curso..."
    }
