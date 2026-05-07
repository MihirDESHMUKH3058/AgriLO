import paho.mqtt.client as mqtt
import json
import logging
import ssl
import time
from config import settings
from datetime import datetime
from pymongo import MongoClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sync PyMongo Client for MQTT Callbacks (runs in separate thread)
mongo_client = MongoClient(settings.MONGODB_URL)
db = mongo_client[settings.MONGODB_DB_NAME]
soil_collection = db["soil_data"]

class MQTTService:
    def __init__(self):
        # Use newer callback API if available or standard one
        self.client = mqtt.Client()
        
        # Configure TLS and Auth for HiveMQ Cloud
        if settings.MQTT_USE_TLS:
            self.client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        
        if settings.MQTT_USER and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        logger.info("MQTT Service initialized")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to HiveMQ Cloud: {settings.MQTT_BROKER}")
            client.subscribe(settings.MQTT_TOPIC)
        else:
            logger.error(f"Failed to connect to MQTT: Return Code {rc}")

    def on_disconnect(self, client, userdata, rc):
        logger.warning(f"Disconnected from MQTT (rc: {rc}). Reconnecting...")
        # Auto-reconnect logic
        try:
            client.reconnect()
        except Exception as e:
            logger.error(f"Reconnect failed: {e}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)
            logger.info(f"MQTT Message: {payload}")

            # Prepare record
            nitrogen = int(int(data.get("nitrogen", 0)) * settings.SOIL_RAW_SCALE)
            phosphorus = int(int(data.get("phosphorus", 0)) * settings.SOIL_RAW_SCALE)
            potassium = int(int(data.get("potassium", 0)) * settings.SOIL_RAW_SCALE)
            
            # Simple validation: ignore if NPK are all 0
            if nitrogen == 0 and phosphorus == 0 and potassium == 0:
                return

            doc = {
                "node_id": data.get("node_id", "unknown"),
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "ph": float(data.get("ph", 7.0)),
                "moisture": float(data.get("moisture", 0.0)),
                "temperature": float(data.get("temperature", 0.0)),
                "ec": float(data.get("ec", 0.0)),
                "timestamp": datetime.utcnow()
            }
            
            soil_collection.insert_one(doc)
            logger.info(f"Saved DB Record for node: {doc['node_id']}")

        except Exception as e:
            logger.error(f"MQTT process error: {e}")

    def start(self):
        try:
            logger.info(f"Connecting to {settings.MQTT_BROKER}:{settings.MQTT_PORT}...")
            self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT start error: {e}")

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

mqtt_service = MQTTService()
