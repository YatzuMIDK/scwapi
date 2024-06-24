from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import random

router = APIRouter()

class Car(BaseModel):
    name: str

class RaceRequest(BaseModel):
    cars: List[Car]
    entry_fee: float
    user_car_name: str
    win_probability: float  # Probabilidad de ganar para el auto del usuario (0 a 1)

class RaceResponse(BaseModel):
    race: str
    prize: float
    position: int

@router.post("/start-race", response_model=RaceResponse)
async def start_race(race_request: RaceRequest):
    if len(race_request.cars) != 8:
        raise HTTPException(status_code=400, detail="The race must have exactly 8 cars.")
    if not (0 <= race_request.win_probability <= 1):
        raise HTTPException(status_code=400, detail="Win probability must be between 0 and 1.")
    
    # Simulate race times for each car
    race_times = {car.name: random.uniform(10.0, 20.0) for car in race_request.cars}

    # Adjust race time for the user's car based on win probability
    if random.random() <= race_request.win_probability:
        race_times[race_request.user_car_name] = min(race_times.values()) - random.uniform(0.1, 1.0)  # Ensure it's the fastest

    # Sort the cars based on their race times
    sorted_cars = sorted(race_request.cars, key=lambda car: race_times[car.name])

    # Assign positions and calculate prizes
    prize_pool = race_request.entry_fee * 8
    prize_distribution = [0.5, 0.25, 0.15, 0.10]  # Distribution of prize pool

    total_prize = 0
    user_position = 0

    positions_str = "Tabla de posiciones:\n"

    for i, car in enumerate(sorted_cars):
        position = i + 1
        race_time = race_times[car.name]
        positions_str += f"{position}. {car.name} - {race_time:.2f} seg\n"

        if car.name == race_request.user_car_name:
            user_position = position
            if position <= 4:
                total_prize = prize_pool * prize_distribution[position - 1]

    return RaceResponse(race=positions_str, prize=total_prize, position=user_position)
