from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
import uuid
import asyncio
from datetime import datetime

router = APIRouter()

# Modelos para el Blackjack
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

class CreateGameResponse(BaseModel):
    game_id: str

class GameStateResponse(BaseModel):
    player_hand: Hand
    dealer_hand: Hand
    game_over: bool
    result: Optional[str]

suits = ['♥️', '♦️', '♣️', '♠️']
ranks = [
    ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
    ('7', 7), ('8', 8), ('9', 9), ('10', 10),
    ('J', 10), ('Q', 10), ('K', 10), ('A', 11)
]

def create_deck() -> List[Card]:
    return [Card(suit=suit, rank=rank, value=value) for suit in suits for rank, value in ranks]

def draw_card(deck: List[Card]) -> Card:
    return deck.pop(random.randint(0, len(deck) - 1))

def calculate_hand_value(cards: List[Card]) -> (int, bool):
    value = sum(card.value for card in cards)
    is_soft = any(card.rank == 'A' for card in cards)
    if value > 21 and is_soft:
        value -= 10
        is_soft = value <= 21
    return value, is_soft

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

@router.post("/blackjack/create", response_model=CreateGameResponse)
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = BlackjackGame()
    return CreateGameResponse(game_id=game_id)

@router.post("/blackjack/hit/{game_id}", response_model=GameStateResponse)
def hit(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.hit()
    return get_game_state(game_id)

@router.post("/blackjack/stand/{game_id}", response_model=GameStateResponse)
def stand(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game.stand()
    return get_game_state(game_id)

@router.get("/blackjack/game_state/{game_id}", response_model=GameStateResponse)
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

# Modelos y endpoints para la máquina tragaperras
class SlotBet(BaseModel):
    bet_amount: float

class SlotResult(BaseModel):
    bet_amount: float
    symbols: list
    won: bool
    payout: float

symbols = ["🍒", "🔔", "🍋", "🍉", "⭐", "7️⃣"]
payouts = {
    ("🍒", "🍒", "🍒"): 10,
    ("🔔", "🔔", "🔔"): 20,
    ("🍋", "🍋", "🍋"): 30,
    ("🍉", "🍉", "🍉"): 40,
    ("⭐", "⭐", "⭐"): 50,
    ("7️⃣", "7️⃣", "7️⃣"): 100
}

@router.post("/slot_machine/bet", response_model=SlotResult)
async def spin_slot_machine(bet: SlotBet):
    if bet.bet_amount <= 0:
        raise HTTPException(status_code=400, detail="Bet amount must be greater than zero.")

    await asyncio.sleep(3)

    result = random.choices(symbols, k=3)

    won = tuple(result) in payouts
    payout = bet.bet_amount * payouts[tuple(result)] if won else 0.0

    return SlotResult(
        bet_amount=bet.bet_amount,
        symbols=result,
        won=won,
        payout=payout
    )

# Modelos y endpoints para la carrera de caballos
class HorseBet(BaseModel):
    horse_number: int
    bet_amount: float

class RaceResult(BaseModel):
    bet_horse: int
    winning_horse: int
    won: bool
    payout: float
    positions: str

horse_names = [
    "Relampago", "Tormenta China", "Pinto", "Storm",
    "Flash", "Cometa", "Tornado", "Eclipse"
]

@router.post("/horse_race/bet", response_model=RaceResult)
async def place_horse_race_bet(bet: HorseBet):
    valid_horses = list(range(1, 9))

    if bet.horse_number not in valid_horses:
        raise HTTPException(status_code=400, detail="Invalid horse number. It must be between 1 and 8.")

    start_time = datetime.now()
    await asyncio.sleep(30)

    race_times = {horse: round(random.uniform(29.5, 30.5), 2) for horse in valid_horses}
    sorted_horses = sorted(race_times.items(), key=lambda item: item[1])

    end_time = datetime.now()
    duration = end_time - start_time

    positions_list = [
        f"{idx + 1}. {horse[0]} - {horse_names[horse[0] - 1]} ({horse[1]:.2f}s)" + (" ⬅️ Tu caballo" if horse[0] == bet.horse_number else "")
        for idx, horse in enumerate(sorted_horses)
    ]

    positions_str = "\n".join(positions_list)

    winning_horse = sorted_horses[0][0]

    won = (bet.horse_number == winning_horse)
    payout = bet.bet_amount * 7 if won else 0.0

    return RaceResult(
        bet_horse=bet.horse_number,
        winning_horse=winning_horse,
        won=won,
        payout=payout,
        positions=positions_str
    )

# Modelos y endpoints para la ruleta
class RouletteBet(BaseModel):
    bet_type: str
    bet_value: strclass RouletteBet(BaseModel):
    bet_type: str  # Tipo de apuesta ("number", "color", "parity")
    bet_value: str  # Valor de la apuesta (número específico, "rojo" o "negro", "par" o "impar")
    bet_amount: float

class RouletteResult(BaseModel):
    bet_amount: float
    bet_type: str
    bet_value: str
    winning_number: int
    winning_color: str
    won: bool
    payout: float

roulette_numbers = list(range(0, 37))
roulette_colors = {
    0: "verde",
    1: "rojo", 2: "negro", 3: "rojo", 4: "negro", 5: "rojo", 6: "negro",
    7: "rojo", 8: "negro", 9: "rojo", 10: "negro", 11: "negro", 12: "rojo",
    13: "negro", 14: "rojo", 15: "negro", 16: "rojo", 17: "negro", 18: "rojo",
    19: "rojo", 20: "negro", 21: "rojo", 22: "negro", 23: "rojo", 24: "negro",
    25: "rojo", 26: "negro", 27: "rojo", 28: "negro", 29: "negro", 30: "rojo",
    31: "negro", 32: "rojo", 33: "negro", 34: "rojo", 35: "negro", 36: "rojo"
}

@router.post("/roulette/bet", response_model=RouletteResult)
async def place_roulette_bet(bet: RouletteBet):
    if bet.bet_amount <= 0:
        raise HTTPException(status_code=400, detail="Bet amount must be greater than zero.")

    await asyncio.sleep(5)

    winning_number = random.choice(roulette_numbers)
    winning_color = roulette_colors[winning_number]
    won = False
    payout = 0.0

    if bet.bet_type == "number" and bet_value.isdigit() and int(bet_value) == winning_number:
        won = True
        payout = bet.bet_amount * 35
    elif bet.bet_type == "color" and bet.bet_value.lower() == winning_color:
        won = True
        payout = bet.bet_amount * 2
    elif bet.bet_type == "parity":
        if bet.bet_value.lower() == "par" and winning_number != 0 and winning_number % 2 == 0:
            won = True
            payout = bet.bet_amount * 2
        elif bet.bet_value.lower() == "impar" and winning_number % 2 != 0:
            won = True
            payout = bet.bet_amount * 2

    return RouletteResult(
        bet_amount=bet.bet_amount,
        bet_type=bet.bet_type,
        bet_value=bet.bet_value,
        winning_number=winning_number,
        winning_color=winning_color,
        won=won,
        payout=payout
    )

# Modelo y endpoint para el juego 7 y 11
class DiceRollResult(BaseModel):
    dice1: int
    dice2: int
    total: int
    won: bool

@router.post("/game/7_11", response_model=DiceRollResult)
async def play_seven_eleven():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    won = total in {7, 11}

    return DiceRollResult(
        dice1=dice1,
        dice2=dice2,
        total=total,
        won=won
    )

# Modelos y endpoint para apostar en un partido de fútbol
class FootballBet(BaseModel):
    home_team: str
    away_team: str
    bet_amount: float
    bet_type: str  # "local", "visitante" o "empate"

class FootballMatchResult(BaseModel):
    first_half: str
    first_half_goals: List[str]
    second_half: str
    second_half_goals: List[str]
    final_score: str
    final_goals: List[str]
    winning_team: str
    bet_amount: float
    won: bool

@router.post("/football_match/bet", response_model=FootballMatchResult)
async def place_football_bet(bet: FootballBet):
    if bet.bet_amount <= 0:
        raise HTTPException(status_code=400, detail="Bet amount must be greater than zero.")
    if bet.bet_type not in ["local", "visitante", "empate"]:
        raise HTTPException(status_code=400, detail="Invalid bet type. It must be 'local', 'visitante' or 'empate'.")

    home_goals_first_half = random.randint(0, 3)
    away_goals_first_half = random.randint(0, 3)
    home_goals_second_half = random.randint(0, 3)
    away_goals_second_half = random.randint(0, 3)

    home_goals_total = home_goals_first_half + home_goals_second_half
    away_goals_total = away_goals_first_half + away_goals_second_half

    first_half_goals = [f"Min {random.randint(1, 45)}: {bet.home_team} {home_goals_first_half}",
                        f"Min {random.randint(1, 45)}: {bet.away_team} {away_goals_first_half}"]
    second_half_goals = [f"Min {random.randint(46, 90)}: {bet.home_team} {home_goals_second_half}",
                         f"Min {random.randint(46, 90)}: {bet.away_team} {away_goals_second_half}"]
    
    final_goals = first_half_goals + second_half_goals

    winning_team = "Empate"
    if home_goals_total > away_goals_total:
        winning_team = bet.home_team
    elif away_goals_total > home_goals_total:
        winning_team = bet.away_team

    won = False
    if (bet.bet_type == "local" and winning_team == bet.home_team) or \
       (bet.bet_type == "visitante" and winning_team == bet.away_team) or \
       (bet.bet_type == "empate" and winning_team == "Empate"):
        won = True

    return FootballMatchResult(
        first_half=f"{bet.home_team} {home_goals_first_half} - {away_goals_first_half} {bet.away_team}",
        first_half_goals=first_half_goals,
        second_half=f"{bet.home_team} {home_goals_second_half} - {away_goals_second_half} {bet.away_team}",
        second_half_goals=second_half_goals,
        final_score=f"{bet.home_team} {home_goals_total} - {away_goals_total} {bet.away_team}",
        final_goals=final_goals,
        winning_team=winning_team,
        bet_amount=bet.bet_amount,
        won=won
    )
