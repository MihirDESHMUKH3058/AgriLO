from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import razorpay
from config import settings
from models import Appointment, User, AppointmentStatus
from datetime import datetime
import uuid
from dependencies import get_current_user

router = APIRouter()

# Initialize Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class OrderCreate(BaseModel):
    amount: float = 199.00
    currency: str = "INR"

class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    appointment_details: dict # name, phone, date, time, address

@router.get("/config")
async def get_payment_config(current_user: User = Depends(get_current_user)):
    return {"key": settings.RAZORPAY_KEY_ID}

@router.post("/create_order")
async def create_order(
    order: OrderCreate, 
    current_user: User = Depends(get_current_user)
):
    try:
        data = { "amount": int(order.amount * 100), "currency": order.currency, "receipt": str(uuid.uuid4()) }
        payment_order = client.order.create(data=data)
        return payment_order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify_payment")
async def verify_payment(
    payment: PaymentVerify, 
    current_user: User = Depends(get_current_user)
):
    try:
        # Verify signature
        params_dict = {
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_payment_id': payment.razorpay_payment_id,
            'razorpay_signature': payment.razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)
        
        # Create Appointment
        details = payment.appointment_details
        new_appointment = Appointment(
            user_id=current_user.id,
            name=details.get("name"),
            phone=details.get("phone"),
            address=details.get("address"),
            date=datetime.fromisoformat(details.get("date")), # Frontend sends ISO string
            amount=199.00,
            payment_id=payment.razorpay_payment_id,
            order_id=payment.razorpay_order_id,
            status=AppointmentStatus.CONFIRMED.value
        )
        await new_appointment.insert()
        
        return {"status": "success", "appointment_id": str(new_appointment.id)}
        
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e:
        print(f"Payment Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/book_direct")
async def book_direct(
    details: dict, 
    current_user: User = Depends(get_current_user)
):
    try:
        new_appointment = Appointment(
            user_id=current_user.id,
            name=details.get("name"),
            phone=details.get("phone"),
            address=details.get("address"),
            date=datetime.fromisoformat(details.get("date")), 
            amount=199.00,
            payment_id="pay_later",
            order_id="pay_later",
            status=AppointmentStatus.PENDING.value
        )
        await new_appointment.insert()
        
        return {"status": "success", "appointment_id": str(new_appointment.id)}
    except Exception as e:
        print(f"Booking Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my_appointments")
async def get_my_appointments(
    current_user: User = Depends(get_current_user)
):
    appointments = await Appointment.find(
        Appointment.user_id == current_user.id
    ).sort(-Appointment.created_at).to_list()
    
    return appointments
