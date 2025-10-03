import os
import openai
import json
import streamlit as st
from pydantic import BaseModel, Field
from db import get_order, update_email, update_name, update_phone, normalize_id

client = openai.OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get the order by Transaction ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"}
                },
                "required": ["Transaction_ID"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_email",
            "description": "Update the email address for a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"},
                    "new_email": {"type": "string"}
                },
                "required": ["Transaction_ID", "new_email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_name",
            "description": "Update the customer name for a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"},
                    "new_name": {"type": "string"}
                },
                "required": ["Transaction_ID", "new_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_phone",
            "description": "Update the phone number for a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"},
                    "new_phone": {"type": "string"}
                },
                "required": ["Transaction_ID", "new_phone"]
            }
        }
    }
]

System_prompt = """You are a shipping tracker assistant.
- Always answer clearly and politely in natural language.
- If a tool call is needed, call it with the required parameters.
"""

messages = [
    {"role": "system", "content": System_prompt},
    # {"role": "user", "content": "I want to check the shipping status with transaction ID 8691788"}, # check status
    {"role": "user", "content": "Change email for transaction ID 8691788 to hero@gmail.com"}, # change email
    # {"role": "user", "content": "I want to check the shipping status with transaction ID 0924951538"}, # check status (wrong ID)
]

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

def call_function(name, args):
    trx_id = normalize_id(args.get("Transaction_ID"))
    if name == "get_order":
        return get_order(trx_id)
    elif name == "update_email":
        return update_email(trx_id, args["new_email"])
    elif name == "update_name":
        return update_name(trx_id, args["new_name"])
    elif name == "update_phone":
        return update_phone(trx_id, args["new_phone"])
    return {"error": f"Unknown function {name}"}

for tool_call in response.choices[0].message.tool_calls or []:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(response.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
    )

st.set_page_config(page_title="📦 Shipping Tracker AI", page_icon="🚚")
st.title("📦 Shipping Tracker Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a polite shipping tracker assistant."}
    ]
    
class Order(BaseModel):
    transaction_id: float = Field(description="Transaction ID")
    response: str = Field(description="Natural language response to the user's question.")

completion = client.chat.completions.parse(
    model="openai/gpt-oss-20b",
    messages=messages,
    response_format=Order
)

parsed = completion.choices[0].message.parsed.response
print(parsed)