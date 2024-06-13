from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime, timedelta
import re
import pytz

router = APIRouter()

# Modelo de solicitud para el tiempo relativo
class TimeRequest(BaseModel):
    time_str: str

# Modelo de respuesta para la marca de tiempo en formato UNIX
class UnixTimestampResponse(BaseModel):
    unix_timestamp: int

# Modelo de respuesta para la conversión de tiempo futuro
class FutureUnixTimestampResponse(BaseModel):
    current_unix_time: int
    future_unix_time: int

# Regex para parsear la cadena de tiempo
time_regex = re.compile(r'(\d+)([smhd])')

def parse_time_string(time_str: str) -> int:
    matches = time_regex.findall(time_str)
    total_seconds = 0
    for value, unit in matches:
        value = int(value)
        if unit == 's':
            total_seconds += value
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 'h':
            total_seconds += value * 3600
        elif unit == 'd':
            total_seconds += value * 86400
    return total_seconds

# Endpoint para transformar marcas de tiempo TZ a UNIX
@router.get("/", response_model=UnixTimestampResponse)
def to_unix(timestamp: str = Query(..., description="Timestamp in ISO 8601 format (e.g., '2024-06-06T12:34:56')")):
    try:
        # Parsear la marca de tiempo con la zona horaria UTC por defecto
        tz = pytz.UTC
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        dt = tz.localize(dt)

        # Convertir a timestamp UNIX
        unix_timestamp = int(dt.timestamp())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return UnixTimestampResponse(unix_timestamp=unix_timestamp)

# Endpoint para convertir cadenas de tiempo a tiempo Unix futuro
@router.post("/to_unix", response_model=FutureUnixTimestampResponse)
def convert_to_unix(request: TimeRequest):
    time_str = request.time_str
    try:
        total_seconds = parse_time_string(time_str)
        current_unix_time = int(datetime.utcnow().timestamp())
        future_unix_time = current_unix_time + total_seconds
        return {
            "unix_actual": current_unix_time,
            "unix_futuro": future_unix_time
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
