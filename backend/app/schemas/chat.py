from pydantic import BaseModel, Field

class chatRequest(BaseModel):
    user_id: int 
    session_id: str = Field(..., description="unique session identifier for the chat")
    message: str= Field(..., description="The message sent by the user to the AI agent")

class ChatREsponse(BaseModel):
    session_id: str
    response: str
    status: str ="success"    