from pydantic import BaseModel
from typing import List

class GameState(BaseModel):
    board: List[List[int]]
    current_player: int
    winner: int = None
