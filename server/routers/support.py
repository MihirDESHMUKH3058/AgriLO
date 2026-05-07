from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependencies import get_current_user
import models

router = APIRouter()

class TicketRequest(BaseModel):
    subject: str
    message: str

@router.post("/ticket")
async def create_ticket(
    ticket: TicketRequest,
    current_user: models.User = Depends(get_current_user)
):
    # Save to DB
    new_ticket = models.SupportTicket(
        user_id=current_user.id,
        subject=ticket.subject,
        message=ticket.message
    )
    await new_ticket.insert()
    
    return {"status": "success", "message": "Ticket submitted successfully", "ticket_id": str(new_ticket.id)}
