from fastapi import APIRouter, HTTPException
from .models import GameState
from .game_logic import check_winner

router = APIRouter()

# In-memory storage for simplicity
games = {}

@router.post("/game_create", response_model=str)
def create_game():
    game_id = str(len(games) + 1)
    games[game_id] = GameState(board=[[0]*7 for _ in range(6)], current_player=1)
    return game_id

@router.post("/play/{game_id}", response_model=GameState)
def play(game_id: str, player: int, column: int):
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    game = games[game_id]
    if game.current_player != player:
        raise HTTPException(status_code=400, detail="Not your turn")
    
    # Implement the logic to place the token in the column
    for row in reversed(game.board):
        if row[column] == 0:
            row[column] = player
            break
    else:
        raise HTTPException(status_code=400, detail="Column is full")

    winner = check_winner(game.board)
    if winner:
        game.winner = winner
    else:
        game.current_player = 2 if player == 1 else 1

    return game
