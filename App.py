import streamlit as st
from supabase import create_client
from openai import OpenAI
from PIL import Image
import tempfile
import base64

# -----------------------------
# CONFIG
# -----------------------------

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# -----------------------------
# PAGE TITLE
# -----------------------------

st.set_page_config(page_title="Invoice AI App")

st.title("📄 AI Invoice Upload System")

# -----------------------------
# FORM
# -----------------------------

vendor_name = st.text_input("Vendor Name")

uploaded_file = st.file_uploader(
    "Upload Invoice",
    type=["png", "jpg", "jpeg", "pdf"]
)

amount = st.text_input("Total Amount")

gst_amount = st.text_input("GST Amount")

# -----------------------------
# AI EXTRACTION
# -----------------------------

if uploaded_file:

    st.success("File Uploaded")

    file_bytes = uploaded_file.read()

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file_bytes)
        temp_path = tmp_file.name

    st.image(file_bytes, width=300)

    if st.button("Extract Using AI"):

        base64_image = base64.b64encode(file_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
Extract:
- total amount
- GST amount

Return only JSON.
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

        ai_result = response.choices[0].message.content

        st.subheader("AI Extraction Result")
        st.code(ai_result)

# -----------------------------
# SUBMIT BUTTON
# -----------------------------

if st.button("Submit Invoice"):

    image_url = ""

    if uploaded_file:

        uploaded_file.seek(0)

        file_name = uploaded_file.name

        supabase.storage.from_("invoice-files").upload(
            file_name,
            uploaded_file.getvalue()
        )

        image_url = f"{SUPABASE_URL}/storage/v1/object/public/invoice-files/{file_name}"

    data = {
        "vendor_name": vendor_name,
        "amount": amount,
        "gst_amount": gst_amount,
        "image_url": image_url,
        "status": "Pending"
    }

    supabase.table("invoices").insert(data).execute()

    st.success("Invoice Submitted Successfully")

# -----------------------------
# VIEW INVOICES
# -----------------------------

st.divider()

st.subheader("Submitted Invoices")

rows = supabase.table("invoices").select("*").execute()

for row in rows.data:

    st.write(f"Vendor: {row['vendor_name']}")
    st.write(f"Amount: ₹{row['amount']}")
    st.write(f"GST: ₹{row['gst_amount']}")
    st.write(f"Status: {row['status']}")

    if row["image_url"]:
        st.image(row["image_url"], width=200)

    st.divider()
