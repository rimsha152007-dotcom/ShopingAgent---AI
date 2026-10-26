#Agar koi user ya agent bar bar aisi request kare jo 
#fail ho jaye (maslan non-existent orders, unauthorized access,ya lagataar tool execution errors), 
#toh system ko pata chalnachahiye. Agar 2 dafa se zyada tool calls fail ho jayein, toh session ko 
#"escalated to human" mark kar diya jata hai taake human customer support agent manually intervene kar sake.

from typing import Dict, Any

FAILED_TOOL_CALLS: Dict[str, int] = {}
ESCALATED_SESSIONS: Dict[str, bool] = {}

def track_tool_failure(session_id: str) -> bool:
    """
    Track the number of failed tool calls for a given session.
    If the number of failures exceeds 2, mark the session as escalated.

    Args:
        session_id (str): The unique identifier for the session.
    """
    current_failures = FAILED_TOOL_CALLS.get(session_id, 0)+1
    FAILED_TOOL_CALLS[session_id] = current_failures

    if current_failures >= 2:
        ESCALATED_SESSIONS[session_id] = True
        return True

    return False

def is_session_escalated(session_id: str) -> bool:
    """
    Check if a session has been escalated to human support.
    """
    return ESCALATED_SESSIONS.get(session_id, False)

def reset_session_tracking(session_id: str):
    """
    Reset the tracking for a given session. This can be used after a session has been resolved or closed.
    """
    if session_id in FAILED_TOOL_CALLS:
        del FAILED_TOOL_CALLS[session_id]
    if session_id in ESCALATED_SESSIONS:
        del ESCALATED_SESSIONS[session_id]