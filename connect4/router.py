from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uuid

router = APIRouter()

# Definición del tablero de juego
ROWS = 6
COLUMNS = 7
PLAYER_EMOJIS = {1: "🟡", 2: "🔴"}
EMPTY_EMOJI = "⬛"
COLUMN_NUMBERS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

class Game(BaseModel):
    board: List[List[str]]
    player_turn: int
    winner: int = 0
    is_full: bool = False

games: Dict[str, Game] = {}

def create_board() -> List[List[str]]:
    return [[EMPTY_EMOJI for _ in range(COLUMNS)] for _ in range(ROWS)]

def check_winner(board: List[List[str]], player: str) -> bool:
    # Verificar filas, columnas y diagonales
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == player and board[r][c + 1] == player and board[r][c + 2] == player and board[r][c + 3] == player:
                return True

    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == player and board[r + 1][c] == player and board[r + 2][c] == player and board[r + 3][c] == player:
                return True

    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == player and board[r + 1][c + 1] == player and board[r + 2][c + 2] == player and board[r + 3][c + 3] == player:
                return True

    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == player and board[r - 1][c + 1] == player and board[r - 2][c + 2] == player and board[r - 3][c + 3] == player:
                return True

    return False

def check_full(board: List[List[str]]) -> bool:
    return all(cell != EMPTY_EMOJI for row in board for cell in row)

def board_to_string(board: List[List[str]]) -> str:
    board_str = "\n".join(["".join(row) for row in board])
    column_numbers_str = "".join(COLUMN_NUMBERS)
    return f"{board_str}\n{column_numbers_str}"

@router.post("/game_create")
def game_create():
    game_id = str(uuid.uuid4())
    games[game_id] = Game(board=create_board(), player_turn=1)
    return {"game_id": game_id, "game": games[game_id]}

@router.post("/game_move/{game_id}")
def game_move(game_id: str, column: int, player: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game = games[game_id]

    if game.winner != 0:
        raise HTTPException(status_code=400, detail="Game already finished")

    if game.is_full:
        raise HTTPException(status_code=400, detail="Game board is full")

    if game.player_turn != player:
        raise HTTPException(status_code=400, detail="It's not your turn")

    if column < 0 or column >= COLUMNS:
        raise HTTPException(status_code=400, detail="Invalid column")

    # Encontrar la fila vacía más baja
    for row in range(ROWS - 1, -1, -1):
        if game.board[row][column] == EMPTY_EMOJI:
            game.board[row][column] = PLAYER_EMOJIS[player]
            break
    else:
        # Si la columna está llena, perder el turno
        game.player_turn = 2 if game.player_turn == 1 else 1
        raise HTTPException(status_code=400, detail="Column is full, turn lost")

    # Verificar si hay ganador
    if check_winner(game.board, PLAYER_EMOJIS[player]):
        game.winner = player
    else:
        # Cambiar turno de jugador
        game.player_turn = 2 if game.player_turn == 1 else 1

    # Verificar si el tablero está lleno
    if check_full(game.board):
        game.is_full = True

    return {"game_id": game_id, "game": games[game_id]}

@router.get("/game_status/{game_id}")
def game_status(game_id: str):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    board_str = board_to_string(game.board)
    
    return {
        "game_id": game_id,
        "board": board_str,
        "player_turn": game.player_turn,
        "winner": game.winner,
        "is_full": game.is_full
    }
