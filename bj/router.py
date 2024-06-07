from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
import uuid

router = APIRouter()

# Representación de una carta y una mano
class Card(BaseModel):
    suit: str
    rank: str
    value: int

    @property
    def display(self):
        return f"{self.rank}{self.suit}"

class Hand(BaseModel):
    cards: str  # Almacenará la representación combinada de las cartas
    value: int
    is_soft: bool  # Si la mano es "soft" (contiene un As contado como 11)

# Modelo de respuesta para crear un juego
class CreateGameResponse(BaseModel):
    game_id: str

# Modelo de respuesta para el estado del juego
class GameStateResponse(BaseModel):
    player_hand: Hand
    dealer_hand: Hand
    game_over: bool
    result: Optional[str]

# Baraja de cartas
suits = ['♥️', '♦️', '♣️', '♠️']
ranks = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
    ('7', 7), ('8', 8), ('9', 9), ('10', 10),
    ('J', 10), ('Q', 10), ('K', 10), ('A', 11)
]

# Funciones auxiliares
def create_deck() -> List[Card]:
    return [Card(suit=suit, rank=rank, value=value) for suit in suits for rank, value in ranks]

def draw_card(deck: List[Card]) -> Card:
    return deck.pop(random.randint(0, len(deck) - 1))

def calculate_hand_value(cards: List[Card]) -> (int, bool):
    value = sum(card.value for card in cards)
    is_soft = any(card.rank == 'A' for card in cards)
    # Ajustar el valor si la mano es "soft" y la suma es mayor que 21
    if value > 21 and is_soft:
        value -= 10
        is_soft = value <= 21
    return value, is_soft

# Clase del juego de Blackjack
class BlackjackGame:
    def __init__(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.game_over = False
        self.result = None
        self.deal_initial_cards()

    def deal_initial_cards(self):
        self.player_hand = [draw_card(self.deck), draw_card(self.deck)]
        self.dealer_hand = [draw_card(self.deck), draw_card(self.deck)]
        self.check_for_blackjack()

    def check_for_blackjack(self):
        player_value, _ = calculate_hand_value(self.player_hand)
        dealer_value, _ = calculate_hand_value(self.dealer_hand)
        if player_value == 21 or dealer_value == 21:
            self.game_over = True
            if player_value == 21 and dealer_value == 21:
                self.result = "Empate"
            elif player_value == 21:
                self.result = "Ganaste con un Blackjack!"
            else:
                self.result = "El dealer ha ganado con un Blackjack!"

    def hit(self):
        if self.game_over:
            return
        self.player_hand.append(draw_card(self.deck))
        player_value, _ = calculate_hand_value(self.player_hand)
        if player_value > 21:
            self.game_over = True
            self.result = "Has perdido! El dealer gana."

    def stand(self):
        if self.game_over:
            return
        self.play_dealer_hand()

    def play_dealer_hand(self):
        dealer_value, _ = calculate_hand_value(self.dealer_hand)
        while dealer_value < 17:
            self.dealer_hand.append(draw_card(self.deck))
            dealer_value, _ = calculate_hand_value(self.dealer_hand)
        self.determine_winner()

    def determine_winner(self):
        player_value, _ = calculate_hand_value(self.player_hand)
        dealer_value, _ = calculate_hand_value(self.dealer_hand)
        self.game_over = True
        if dealer_value > 21 or player_value > dealer_value:
            self.result = "Ganaste!"
        elif player_value < dealer_value:
            self.result = "El dealer gana!"
        else:
            self.result = "Empate"

    def get_hand(self, hand: List[Card]) -> Hand:
        value, is_soft = calculate_hand_value(hand)
        return Hand(cards="".join(card.display for card in hand), value=value, is_soft=is_soft)

games = {}

@router.post("/create", response_model=CreateGameResponse)
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = BlackjackGame()
    return CreateGameResponse(game_id=game_id)

@router.post("/hit/{game_id}", response_model=GameStateResponse)
def hit(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.hit()
    return get_game_state(game_id)

@router.post("/stand/{game_id}", response_model=GameStateResponse)
def stand(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.stand()
    return get_game_state(game_id)

@router.get("/game_state/{game_id}", response_model=GameStateResponse)
def get_game_state(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameStateResponse(
        player_hand=game.get_hand(game.player_hand),
        dealer_hand=game.get_hand(game.dealer_hand),
        game_over=game.game_over,
        result=game.result
    )
