import os
import openai
from pydantic import BaseModel
from db import get_order, update_email, update_name, update_phone, normalize_id

client = openai.OpenAI(api_key=os.getenv("GROQ_API_KEY"),  base_url="https://api.groq.com/openai/v1")

class Order(BaseModel):
    trx_id: str
    name: str
    email: str
    phone: str

# def run_agent(user_input: str) -> str:
#     words = user_input.lower().split()
#     trx_id = next((w for w in user_input.split() if w.replace(".", "").isdigit()), None)

#     if trx_id:
#         trx_id = normalize_id(trx_id)

#         if "status" in user_input:
#             order = get_order(trx_id)
#             if order:
#                 return f"✅ Transaction {trx_id}: Order status is {order['Order_Status']}."
#             else:
#                 return f"❌ No data found for Transaction ID {trx_id}."

#         if "email" in user_input:
#             parts = user_input.split(" to ")
#             if len(parts) == 2:
#                 new_email = parts[1].strip()
#                 order = get_order(trx_id)
#                 if order:
#                     update_email(trx_id, new_email)
#                     return f"✅ Email for Transaction {trx_id} updated to {new_email}."
#                 else:
#                     return f"❌ No data found for Transaction ID {trx_id}."

#         if "name" in user_input:
#             parts = user_input.split(" to ")
#             if len(parts) == 2:
#                 new_name = parts[1].strip()
#                 order = get_order(trx_id)
#                 if order:
#                     update_name(trx_id, new_name)
#                     return f"✅ Name for Transaction {trx_id} updated to {new_name}."
#                 else:
#                     return f"❌ No data found for Transaction ID {trx_id}."

#         if "phone" in user_input:
#             parts = user_input.split(" to ")
#             if len(parts) == 2:
#                 new_phone = parts[1].strip()
#                 order = get_order(trx_id)
#                 if order:
#                     update_phone(trx_id, new_phone)
#                     return f"✅ Phone for Transaction {trx_id} updated to {new_phone}."
#                 else:
#                     return f"❌ No data found for Transaction ID {trx_id}."

#     # --- fallback ke LLM kalau tidak dikenali ---
#     response = client.chat.completions.create(
#         model="openai/gpt-oss-20b",  # bisa diganti model lain
#         messages=[
#             {"role": "system", "content": "You are an assistant for shipping and order tracking."},
#             {"role": "user", "content": user_input},
#         ],
#     )

#     return response.choices[0].message.content