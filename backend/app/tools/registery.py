from typing import List, Dict, Any 

 # 1 System prompot jo LLM ko batat he key usney e-commerce assistant ki tarah behave karna he
AGENT_SYSTEM_PROMPT = """
You are a helpful e-commerce customer support assistant for ShopAgent AI. 
You can help users check their order status, update shipping addresses, and cancel orders.
Always be polite, concise, and accurate. 
If a user asks to perform a destructive or sensitive action (like cancelling an order or changing an address), make sure to invoke the appropriate tool.
Never make up order details; always rely on the tool outputs.
"""

# 2 tools ki json schemas jo LLM ko batati he key tools ko kesy use krna he 
TOOL_SCHEMAS: List[Dict[str, Any]] = [
    {
        "name": "get_order_status",
        "description": "Get the curret status, items and total amount of a specific order by providing the order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer", 
                    "description": "The unique identifier of the order to check."
                    }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "update_shipping_address",
        "description": "Update the shipping address for an active order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer", 
                    "description": "The unique ID of the order."
                },
                "new_address": {
                    "type": "string", 
                    "description": "The new shipping address to set for the order."
                }
            },
            "required": ["order_id", "new_address"]
        }

    },
    {
        "name": "cancel_order",
        "description": "Cancel an existing order if eligible.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "The unique ID of the order to cancel."
                }
            },
            "required": ["order_id"]
        }
    }
]