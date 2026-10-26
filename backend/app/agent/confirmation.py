# Kuch tools destructive/sensitive hote hain (jaise order cancel karna ya shipping address badalna). Yeh actions bina user ki explicit confirmation ke direct execute nahi honi chahiyein.
# Is step mein hum ek confirmation mechanism banayenge jahan destructive tool pehle "needs_confirmation" return karega, aur user ke confirm karne ke baad hi actual execution hogi.

from typing import Dict, Any, Optional
import uuid

# In-memory store jo pending actions ko temporarily hold karega confirmation ke liye
# Production mein isay Redis ya Database table mein rakha jata hai
PENDING_CONFIRMATIONS: Dict[str, Dict[str, Any]] = {}

def create_pending_confirmation(tool_name: str, tool_args: Dict[str, Any], user_id: int) -> str:
    """Ek unique confirmation token banata hai aur action ko pending list mein save kar leta hai."""
    confirmation_token = str(uuid.uuid4())
    
    PENDING_CONFIRMATIONS[confirmation_token] = {
        "tool_name": tool_name,
        "tool_args": tool_args,
        "user_id": user_id,
        "status": "pending"
    }
    
    return confirmation_token

def get_pending_confirmation(token: str) -> Optional[Dict[str, Any]]:
    """Token ke zariye pending action details fetch karta hai."""
    return PENDING_CONFIRMATIONS.get(token)

def clear_pending_confirmation(token: str):
    """Action execute hone ke baad token ko store se hata deta hai."""
    if token in PENDING_CONFIRMATIONS:
        del PENDING_CONFIRMATIONS[token]