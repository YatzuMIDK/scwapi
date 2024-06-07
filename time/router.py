from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import pytz

router = APIRouter()

# Modelo de respuesta para la marca de tiempo en formato UNIX
class UnixTimestampResponse(BaseModel):
    unix_timestamp: int

# Endpoint para transformar marcas de tiempo TZ a UNIX
@router.get("/to_unix", response_model=UnixTimestampResponse)
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
