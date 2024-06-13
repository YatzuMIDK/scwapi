from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter()

class MinesweeperRequest(BaseModel):
    rows: int
    cols: int
    bombs: int

def generate_minesweeper_board(rows: int, cols: int, bombs: int):
    # Crear un tablero vacío
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Colocar las bombas aleatoriamente
    bomb_positions = set()
    while len(bomb_positions) < bombs:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        if (r, c) not in bomb_positions:
            bomb_positions.add((r, c))
            board[r][c] = '💣'
    
    # Calcular los números alrededor de las bombas
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r, c in bomb_positions:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '💣':
                board[nr][nc] += 1
                
    return board

def board_to_discord_format(board):
    discord_board = ""
    for row in board:
        for cell in row:
            if cell == '💣':
                discord_board += "||💣||"
            elif cell == 0:
                discord_board += "||:white_large_square:||"
            else:
                discord_board += f"||:{cell}:||"
        discord_board += "\n"
    return discord_board

@router.post("/")
def generate_minesweeper(request: MinesweeperRequest):
    rows, cols, bombs = request.rows, request.cols, request.bombs
    if rows <= 0 or cols <= 0 or bombs <= 0 or bombs >= rows * cols:
        raise HTTPException(status_code=400, detail="Invalid board dimensions or number of bombs")
    
    board = generate_minesweeper_board(rows, cols, bombs)
    discord_board = board_to_discord_format(board)
    
    return {"board": discord_board}
