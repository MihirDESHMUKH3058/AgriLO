from fastapi import APIRouter, HTTPException, Depends
from models import SoilData
from typing import List

router = APIRouter()

@router.get("/latest", response_model=SoilData)
async def get_latest_soil_data():
    # Filter for non-zero NPK to avoid showing sensor errors
    result_obj = await SoilData.find(
        {"$or": [{"nitrogen": {"$gt": 0}}, {"phosphorus": {"$gt": 0}}, {"potassium": {"$gt": 0}}]}
    ).sort(-SoilData.timestamp).first_or_none()
    
    if result_obj:
        print(f"[DEBUG] Fetching latest soil data: {result_obj.nitrogen}, {result_obj.phosphorus}, {result_obj.potassium}")
    else:
        print("[DEBUG] No soil data found in DB")
    
    if not result_obj:
        raise HTTPException(status_code=404, detail="No sensor data found")
    
    return result_obj

@router.get("/history", response_model=List[SoilData])
async def get_soil_history(
    limit: int = 10
):
    result = await SoilData.find().sort(-SoilData.timestamp).limit(limit).to_list()
    return result
