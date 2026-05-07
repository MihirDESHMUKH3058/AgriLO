from pydantic import Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid
import enum
from beanie import Document

# Define Enums
class UserRole(str, enum.Enum):
    FARMER = "farmer"
    EXPERT = "expert"
    ADMIN = "admin"

class QueryStatus(str, enum.Enum):
    OPEN = "open"
    ANSWERED = "answered"
    CLOSED = "closed"

class AppointmentStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    name: str = Field(max_length=100)
    email: str
    phone: Optional[str] = Field(default=None, max_length=15)
    hashed_password: str
    role: str = Field(default=UserRole.FARMER.value)
    language: str = Field(default="en")
    location: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = {}
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"

class AuthSession(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    refresh_token: str
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "auth_sessions"

class Scan(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    scan_type: str # leaf, soil, root
    crop_name: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Generic status/summary fields
    disease_detected: Optional[str] = None
    confidence: Optional[float] = None

    class Settings:
        name = "scans"

class AnalysisResult(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    scan_id: str
    
    result_data: Dict[str, Any] = {}
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "analysis_results"

class ExpertQuery(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    expert_id: Optional[str] = None
    scan_id: Optional[str] = None
    
    question: str
    answer: Optional[str] = None
    status: str = Field(default=QueryStatus.OPEN.value)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "expert_queries"

class ChatHistory(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    role: str # "user" or "bot"
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "chat_history"

class SupportTicket(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    subject: str
    message: str
    status: str = Field(default="Open")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "support_tickets"

class SoilData(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    node_id: str
    nitrogen: int
    phosphorus: int
    potassium: int
    ph: float
    moisture: float
    temperature: float
    ec: float

    class Settings:
        name = "soil_data"

class Appointment(Document):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str
    name: str # Contact name
    phone: str
    date: datetime
    address: str
    amount: float = 199.00
    payment_id: Optional[str] = None
    order_id: Optional[str] = None
    status: str = Field(default=AppointmentStatus.PENDING.value)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "appointments"
