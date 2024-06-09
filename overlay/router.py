from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random
import asyncio
from datetime import datetime

router = APIRouter()

# Definición de símbolos y premios para la máquina tragaperras
symbols = ["🍒", "🔔", "🍋", "🍉", "⭐", "7️⃣"]
payouts = {
    ("🍒", "🍒", "🍒"): 10,
    ("🔔", "🔔", "🔔"): 20,
    ("🍋", "🍋", "🍋"): 30,
    ("🍉", "🍉", "🍉"): 40,
    ("⭐", "⭐", "⭐"): 50,
    ("7️⃣", "7️⃣", "7️⃣"): 100
}

class SlotBet(BaseModel):
    bet_amount: float

class SlotResult(BaseModel):
    bet_amount: float
    symbols: list
    won: bool
    payout: float

@router.post("/sm/bet", response_model=SlotResult)
async def spin_slot_machine(bet: SlotBet):
    if bet.bet_amount <= 0:
        raise HTTPException(status_code=400, detail="Bet amount must be greater than zero.")

    # Esperar 3 segundos para simular el giro de la máquina
    await asyncio.sleep(3)

    # Generar los símbolos aleatorios para la máquina tragaperras
    result = random.choices(symbols, k=3)

    # Determinar si el usuario ganó
    won = tuple(result) in payouts
    payout = bet.bet_amount * payouts[tuple(result)] if won else 0.0

    return SlotResult(
        bet_amount=bet.bet_amount,
        symbols=result,
        won=won,
        payout=payout
    )

# Definición de nombres de caballos
horse_names = [
    "Relampago",
    "Tormenta China",
    "Pinto",
    "Storm",
    "Flash",
    "Cometa",
    "Tornado",
    "Eclipse"
]

class HorseBet(BaseModel):
    horse_number: int  # Número del caballo (1-8, por ejemplo)
    bet_amount: float

class RaceResult(BaseModel):
    bet_horse: int
    winning_horse: int
    won: bool
    payout: float
    positions: str  # La lista de posiciones como un solo string

@router.post("/cc/bet", response_model=RaceResult)
async def place_horse_race_bet(bet: HorseBet):
    valid_horses = list(range(1, 9))  # Suponiendo que hay 8 caballos en la carrera

    # Validar el número del caballo
    if bet.horse_number not in valid_horses:
        raise HTTPException(status_code=400, detail="Invalid horse number. It must be between 1 and 8.")

    # Guardar el tiempo de inicio
    start_time = datetime.now()

    # Esperar 30 segundos para simular la duración de la carrera
    await asyncio.sleep(30)

    # Simular los tiempos de llegada de cada caballo
    race_times = {horse: round(random.uniform(29.5, 30.5), 2) for horse in valid_horses}
    sorted_horses = sorted(race_times.items(), key=lambda item: item[1])

    # Guardar el tiempo de fin y calcular la duración
    end_time = datetime.now()
    duration = end_time - start_time

    # Crear la lista de posiciones con los números y nombres de caballos y marcar el caballo apostado con una flecha
    positions_list = [
        f"{idx + 1}. {horse[0]} - {horse_names[horse[0] - 1]} ({horse[1]:.2f}s)" + (" ⬅️ Tu caballo" if horse[0] == bet.horse_number else "")
        for idx, horse in enumerate(sorted_horses)
    ]

    # Unir la lista de posiciones en un solo string
    positions_str = "\n".join(positions_list)

    winning_horse = sorted_horses[0][0]

    # Determinar si el usuario ganó
    won = (bet.horse_number == winning_horse)
    payout = bet.bet_amount * 7 if won else 0.0  # Pago 7:1 por ejemplo

    return RaceResult(
        bet_horse=bet.horse_number,
        winning_horse=winning_horse,
        won=won,
        payout=payout,
        positions=positions_str
    )

class RouletteBet(BaseModel):
    bet_type: str  # "number", "color", "parity"
    bet_value: str  # "0-36" for number, "red" or "black" for color, "even" or "odd" for parity
    bet_amount: float

class RouletteResult(BaseModel):
    bet_type: str
    bet_value: str
    winning_number: int
    winning_color: str
    winning_parity: str
    won: bool
    payout: float

# Mapa de colores para los números
color_map = {
    0: "green", 1: "red", 2: "black", 3: "red", 4: "black", 5: "red", 6: "black", 7: "red", 8: "black", 9: "red",
    10: "black", 11: "black", 12: "red", 13: "black", 14: "red", 15: "black", 16: "red", 17: "black", 18: "red",
    19: "red", 20: "black", 21: "red", 22: "black", 23: "red", 24: "black", 25: "red", 26: "black", 27: "red",
    28: "black", 29: "black", 30: "red", 31: "black", 32: "red", 33: "black", 34: "red", 35: "black", 36: "red"
}

@router.post("/rt/bet", response_model=RouletteResult)
async def place_roulette_bet(bet: RouletteBet):
    valid_bet_types = {"number", "color", "parity"}
    valid_colors = {"red", "black"}
    valid_parities = {"even", "odd"}

    # Validar el tipo de apuesta
    if bet.bet_type not in valid_bet_types:
        raise HTTPException(status_code=400, detail="Invalid bet type. It must be 'number', 'color', or 'parity'.")

    # Validar el valor de la apuesta
    if bet.bet_type == "number":
        if not (bet.bet_value.isdigit() and 0 <= int(bet.bet_value) <= 36):
            raise HTTPException(status_code=400, detail="Invalid bet value for type 'number'. It must be between 0 and 36.")
    elif bet.bet_type == "color":
        if bet.bet_value not in valid_colors:
            raise HTTPException(status_code=400, detail="Invalid bet value for type 'color'. It must be 'red' or 'black'.")
    elif bet.bet_type == "parity":
        if bet.bet_value not in valid_parities:
            raise HTTPException(status_code=400, detail="Invalid bet value for type 'parity'. It must be 'even' or 'odd'.")

    # Esperar 30 segundos
    await asyncio.sleep(3)

    # Simular el giro de la ruleta
    winning_number = random.randint(0, 36)
    winning_color = color_map[winning_number]
    winning_parity = "even" if winning_number % 2 == 0 else "odd"

    # Determinar si el usuario ganó
    if bet.bet_type == "number":
        won = (int(bet.bet_value) == winning_number)
        payout = bet.bet_amount * 35 if won else 0.0
    elif bet.bet_type == "color":
        won = (bet.bet_value == winning_color)
        payout = bet.bet_amount * 2 if won else 0.0
    elif bet.bet_type == "parity":
        won = (bet.bet_value == winning_parity)
        payout = bet.bet_amount * 2 if won else 0.0

    return RouletteResult(
        bet_type=bet.bet_type,
        bet_value=bet.bet_value,
        winning_number=winning_number,
        winning_color=winning_color,
        winning_parity=winning_parity,
        won=won,
        payout=payout
    )
