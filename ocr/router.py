# combate/router.py
from fastapi import APIRouter, HTTPException
import random

router = APIRouter()

class Jugador(BaseModel):
    nombre: str
    salud: int
    tiro: int
    reflejos: float
    tipo_arma: int  # 0: desarmado, 1: pistolas, 2: subfusiles, 3: rifles de asalto, 4: francotirador, 5: arma cuerpo a cuerpo
    balas_45c: Optional[int] = 0  # Cantidad de balas de calibre .45c
    balas_9mm: Optional[int] = 0  # Cantidad de balas de calibre 9mm
    balas_556mm: Optional[int] = 0  # Cantidad de balas de calibre 5.56mm

# Ruta para el combate
@router.post("/")
async def combatir(jugador_atacante: Jugador, jugador_atacado: Jugador):
    # Validar si el jugador atacante tiene balas para el tipo de arma que posee
    if jugador_atacante.tipo_arma != 0 and jugador_atacante.balas_45c == 0 and jugador_atacante.balas_9mm == 0 and jugador_atacante.balas_556mm == 0:
        raise HTTPException(status_code=400, detail=f"{jugador_atacante.nombre} no tiene balas para su arma y no puede atacar.")

    # Validar si el jugador atacado tiene balas para el tipo de arma que posee
    if jugador_atacado.tipo_arma != 0 and jugador_atacado.balas_45c == 0 and jugador_atacado.balas_9mm == 0 and jugador_atacado.balas_556mm == 0:
        raise HTTPException(status_code=400, detail=f"{jugador_atacado.nombre} no tiene balas para su arma y no puede atacar.")

    # Simular la probabilidad de éxito del ataque del jugador atacante
    probabilidad_exito = jugador_atacante.tiro / 100.0

    if random.random() <= probabilidad_exito:
        # El ataque tiene éxito, reducir la salud del jugador atacado
        jugador_atacado.salud -= jugador_atacante.tiro

        if jugador_atacado.tipo_arma in [0, 4, 5]:
            # Jugador atacado no puede contraatacar, solo puede esquivar
            mensaje = f"{jugador_atacado.nombre} esquiva el ataque de {jugador_atacante.nombre}."
        else:
            # Ver si el jugador atacado puede reaccionar y contraatacar
            probabilidad_reaccion = jugador_atacado.reflejos / 100.0
            if random.random() <= probabilidad_reaccion:
                # El jugador atacado realiza un contraataque
                tipo_arma_atacado = jugador_atacado.tipo_arma
                if tipo_arma_atacado == 1:
                    # Pistolas
                    jugador_atacado.balas_9mm -= 1
                elif tipo_arma_atacado == 2:
                    # Subfusiles
                    jugador_atacado.balas_9mm -= 1
                    jugador_atacado.balas_45c -= 1
                elif tipo_arma_atacado == 3:
                    # Rifles de asalto
                    jugador_atacado.balas_556mm -= 1

                probabilidad_exito_contraataque = jugador_atacado.tiro / 100.0
                if random.random() <= probabilidad_exito_contraataque:
                    # El contraataque tiene éxito, reducir la salud del jugador atacante
                    jugador_atacante.salud -= jugador_atacado.tiro
                    mensaje = f"{jugador_atacado.nombre} realiza un contraataque exitoso con su arma {tipo_arma_atacado}. {jugador_atacante.nombre} pierde {jugador_atacado.tiro} de salud."
                else:
                    mensaje = f"{jugador_atacado.nombre} intenta un contraataque con su arma {tipo_arma_atacado} pero falla."
            else:
                mensaje = f"{jugador_atacado.nombre} no puede reaccionar a tiempo y es golpeado por {jugador_atacante.nombre}."

    else:
        mensaje = f"{jugador_atacante.nombre} falla el ataque."

    # Devolver el estado actualizado de los jugadores
    return {
        "mensaje": mensaje,
        "jugador_atacante": jugador_atacante.dict(),
        "jugador_atacado": jugador_atacado.dict()
            }
