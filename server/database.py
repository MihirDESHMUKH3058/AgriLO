from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
import models

async def init_db():
    # Create Motor client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Initialize beanie with the models
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[
            models.User,
            models.AuthSession,
            models.Scan,
            models.AnalysisResult,
            models.ExpertQuery,
            models.ChatHistory,
            models.SupportTicket,
            models.SoilData,
            models.Appointment
        ]
    )

# Note: get_session is no longer needed with Beanie. 
# Document operations are global once init_beanie is called.
