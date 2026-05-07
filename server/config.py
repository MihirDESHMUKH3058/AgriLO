from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "agrilo_db"

    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # 15 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Payments
    RAZORPAY_KEY_ID: str = "rzp_test_placeholder"
    RAZORPAY_KEY_SECRET: str = "rzp_secret_placeholder"

    
    # AI Services
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # Model Paths
    LEAF_MODEL_PATH: str = os.path.join(BASE_DIR, "models/final_model.h5")
    SOIL_MODEL_PATH: str = os.path.join(BASE_DIR, "models/soil_model.pkl")
    LABEL_ENCODER_PATH: str = os.path.join(BASE_DIR, "models/label_encoder.pkl")
    CLASS_INDICES_PATH: str = os.path.join(BASE_DIR, "models/class_indices.json")
    
    ROOT_MODEL_PATH: str = os.path.join(BASE_DIR, "models/root_model.h5")
    ROOT_CLASS_INDICES_PATH: str = os.path.join(BASE_DIR, "models/root_class_indices.json")
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173", 
        "http://localhost:3000",
        "https://agri-lo-ivory.vercel.app",
        "https://agri-lo.vercel.app",
        "https://agri-lo-six.vercel.app",
        "https://agri-lo-six.vercel.app/"
    ]
    
    # App Info
    APP_NAME: str = "Agri-Lo API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = int(os.environ.get("PORT", 10000))

    # MQTT Hardware
    MQTT_BROKER: str = os.getenv("MQTT_BROKER", "5c53b5296e584933bd06c1060b482f7d.s1.eu.hivemq.cloud")
    MQTT_PORT: int = int(os.getenv("MQTT_PORT", 8883))
    MQTT_USER: str = os.getenv("MQTT_USER", "Admin")
    MQTT_PASSWORD: str = os.getenv("MQTT_PASSWORD", "QJbkE4b!Pg9A!@n")
    MQTT_USE_TLS: bool = os.getenv("MQTT_USE_TLS", "true").lower() == "true"
    MQTT_TOPIC: str = "farm/soil/node01/data"
    SOIL_RAW_SCALE: float = 0.1 # Raw 800 -> 80 mg/kg
    
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
