# Yeh core agent loop hai jo user ki message query ko leta hai, 
# LLM ke sath communicate karta hai, agar LLM koi tool call karna chahey 
# toh us tool ko execute karta hai, aur phir result ko wapas LLM ko bhej kar 
# final response generate karta hai (max 5 iterations ki limit ke sath taake infinite loop na bane).

from ast import arg
from email import message
import json
from typing import List, Dict, Any
from urllib import response
from sqlalchemy.orm import Session
from app.llm.factory import get_llm_client
from backend.app.tools.registery import TOOL_SCHEMAS, AGENT_SYSTEM_PROMPT
from backend.app.tools.orders_tool import get_order_status, update_shipping_address,cancel_order

def run_agent_loop(db: Session, user_id: int, user_message: str) ->str:
    # llm client ko intialize krrta he (factory paatren sey fake ya gorg client mile ga)
    llm_client = get_llm_client()

    # conersation message list banta he jisme system prompot aur user ka message hoota he 
    messages: List[Dict[str, Any]] = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    max_iterations = 5
    iteration = 0

    # Agent loop shuru hoota he 
    while iteration < max_iterations:
        iteration += 1 

        # LLm se response lete he 
        response_text = llm_client.generate_response(messages)

        # Check karte hain ke kya LLM ne koi tool call karne ki demand ki hai?
        # (Hum yahan simple JSON parsing ya text matching handle karte hain)
        if "TOOL_CALL:" in response_text:
            try:
                # Example format jo llm de sakta hai: TOOL_CALL: get_order_status {"order_id": 1}
                parts = response_text.split("TOOL_CALL:")
                tool_part = parts[1].strip()

                # Tool name aur arguments alag karte hain 
                tool_name = tool_part.split(" ")[0]
                args_json_str = tool_part[len(tool_name):].strip()
                args = json.loads(args_json_str) if args_json_str else {}

                # Tool execution result
                tool_result = {}
                
                # Tool mapping aur execution with security check (user_id hamesha backend/session se pass hoga)
                if tool_name == "get_order_status":
                    tool_result = get_order_status(db, user_id=user_id, order_id=args.get("order_id"))
                elif tool_name == "update_shipping_address":
                    tool_result = update_shipping_address(db, user_id=user_id, order_id=args.get("order_id"), new_address=args.get("new_address"))
                elif tool_name == "cancel_order":
                    tool_result = cancel_order(db, user_id=user_id, order_id=args.get("order_id"))
                else:
                    tool_result = {"status": "error", "message": f"Unknown tool: {tool_name}"}
                
                # Assistant aur Tool output messages history mein append karte hain
                messages.append({"role": "assistant", "content": response_text})
                messages.append({"role": "system", "content": f"Tool Output: {json.dumps(tool_result)}"})
                
                # Loop continue karega taake LLM tool output ko read karke final natural response de sake
                continue
                
            except Exception as e:
                return f"Agent execution error while running tool: {str(e)}"
        
        # Agar koi tool call nahi hai, toh yeh final text response hai jo user ko return ho jayega
        return response_text
        
    return "Agent reached maximum iteration limit without final answer."



