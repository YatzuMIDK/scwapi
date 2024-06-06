from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter()

class CreateGameResponse(BaseModel):
    game_id: str

class DropPieceRequest(BaseModel):
    player: int
    column: int

class GameStateResponse(BaseModel):
    board: str
    current_player: int
    winner: Optional[int]

# Connect4 Game Logic
class Connect4:
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.winner = None

    def drop_piece(self, column: int) -> bool:
        if column < 0 or column >= 7:
            return False

        for row in reversed(range(6)):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                if self.check_winner(row, column):
                    self.winner = self.current_player
                self.current_player = 1 if self.current_player == 2 else 2
                return True
        return False

    def check_winner(self, row: int, column: int) -> bool:
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + dr * i, column + dc * i
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - dr * i, column - dc * i
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def is_full(self) -> bool:
        return all(self.board[0][col] != 0 for col in range(7))

    def get_board_with_emojis(self) -> str:
        emoji_map = {0: "⬛", 1: "🔴", 2: "🟡"}
        board_str = "\n".join("".join(emoji_map[cell] for cell in row) for row in self.board)
        return board_str + "\n1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"

games = {}

@router.post("/create", response_model=CreateGameResponse)
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = Connect4()
    return CreateGameResponse(game_id=game_id)

@router.post("/drop/{game_id}", response_model=GameStateResponse)
def drop_piece(game_id: str, request: DropPieceRequest):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.winner:
        raise HTTPException(status_code=400, detail="The game has already been won.")

    if game.current_player != request.player:
        raise HTTPException(status_code=400, detail="It is not the turn of this player.")

    if not game.drop_piece(request.column):
        raise HTTPException(status_code=400, detail="Invalid move")

    if game.is_full():
        game.winner = 0  # 0 indicates that the game is a draw

    return GameStateResponse(board=game.get_board_with_emojis(), current_player=game.current_player, winner=game.winner)

@router.get("/game_state/{game_id}", response_model=GameStateResponse)
def get_game_state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameStateResponse(board=game.get_board_with_emojis(), current_player=game.current_player, winner=game.winner)
