import os
import json
import streamlit as st
import openai
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
                "properties": {"Transaction_ID": {"type": "number"}},
                "required": ["Transaction_ID"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_email",
            "description": "Update the email for a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"},
                    "new_email": {"type": "string"},
                },
                "required": ["Transaction_ID", "new_email"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_phone",
            "description": "Update the phone for a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"},
                    "new_phone": {"type": "string"},
                },
                "required": ["Transaction_ID", "new_phone"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_name",
            "description": "Update the name for a transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "Transaction_ID": {"type": "number"},
                    "new_name": {"type": "string"},
                },
                "required": ["Transaction_ID", "new_name"],
            },
        },
    },
]

def call_function(name, args):
    if name == "get_order":
        return get_order(normalize_id(args["Transaction_ID"]))
    elif name == "update_email":
        return update_email(normalize_id(args["Transaction_ID"]), args["new_email"])
    elif name == "update_phone":
        return update_phone(normalize_id(args["Transaction_ID"]), args["new_phone"])
    elif name == "update_name":
        return update_name(normalize_id(args["Transaction_ID"]), args["new_name"])
    else:
        return {"error": f"Unknown function {name}"}

st.set_page_config(page_title="AI Shipping Assistant", page_icon="📦")
st.title("📦 AI Shipping Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a shipping tracker assistant. Always answer clearly and politely."}
    ]

def to_dict(msg):
    """Convert ChatCompletionMessage or dict into plain dict"""
    if isinstance(msg, dict):
        return msg
    return {"role": msg.role, "content": msg.content}


for msg in st.session_state.messages:
    msg = to_dict(msg)
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

if user_input := st.chat_input("Ask me about your order..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=st.session_state.messages,
        tools=tools,
        tool_choice="auto",
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            result = call_function(fn_name, fn_args)

            st.session_state.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": fn_name,
                "content": json.dumps(result)
            })

        followup = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = followup.choices[0].message
        st.session_state.messages.append({"role": "assistant", "content": msg.content})
        st.chat_message("assistant").write(msg.content)

    else:
        msg = {"role": msg.role, "content": msg.content}
        st.session_state.messages.append(msg)
        ai_reply = msg["content"] if msg["content"] else "(No reply)"
        st.chat_message("assistant").write(ai_reply)
