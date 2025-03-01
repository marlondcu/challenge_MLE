import fastapi
from pydantic import BaseModel, root_validator, ValidationError
from fastapi import HTTPException
import pandas as pd
from typing import List
from challenge.model import DelayModel 

app = fastapi.FastAPI()

model = DelayModel()

OPERA_MAP = {
    "Latin American Wings": "OPERA_Latin_American_Wings",
    "Grupo LATAM": "OPERA_Grupo_LATAM",
    "Sky Airline": "OPERA_Sky_Airline",
    "Copa Air": "OPERA_Copa_Air",
    "Aerolineas Argentinas": None  
}

VALID_MONTHS = [3, 4, 7, 10, 11, 12]

def preprocess_input(data: dict):
    try:
        processed_data = {key: 0 for key in [
            "OPERA_Latin_American_Wings", "MES_7", "MES_10", "OPERA_Grupo_LATAM", 
            "MES_12", "TIPOVUELO_I", "MES_4", "MES_11", "OPERA_Sky_Airline", "OPERA_Copa_Air", "OPERA_Aerolineas_Argentinas"
        ]}

        opera = data.get("OPERA")
        if opera in OPERA_MAP:
            processed_data[OPERA_MAP[opera]] = 1
        else:
            raise HTTPException(status_code=400, detail=f"Invalid OPERA value: {opera}")

        mes = data.get("MES")
        if mes not in VALID_MONTHS:
            raise HTTPException(status_code=400, detail=f"Invalid MES value: {mes}")
        mes_key = f"MES_{mes}"
        if mes_key in processed_data:
            processed_data[mes_key] = 1
        
        tipovuelo = data.get("TIPOVUELO")
        if tipovuelo == "I":
            processed_data["TIPOVUELO_I"] = 1
        elif tipovuelo == "N":
            pass  
        else:
            raise HTTPException(status_code=400, detail=f"Invalid TIPOVUELO value: {tipovuelo}")
        
        return processed_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}

@app.post("/predict", status_code=200)
async def post_predict(request: dict) -> dict:
    try:
        if "flights" not in request:
            raise HTTPException(status_code=400, detail="Missing 'flights' key in request")

        flights = request["flights"]
        if not isinstance(flights, list) or not flights:
            raise HTTPException(status_code=400, detail="'flights' must be a non-empty list")

        processed_inputs = [preprocess_input(flight) for flight in flights]
        input_data = pd.DataFrame(processed_inputs)

        predictions = model.predict(input_data)
        return {"predict": predictions}
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))