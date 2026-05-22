import streamlit as st
from supabase import create_client
from openai import OpenAI
import base64
import json
import time

# =====================================
# CONFIG
# =====================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="AI Invoice Upload System",
    layout="wide"
)

st.title("📄 AI Invoice Upload System")

st.markdown("---")

# =====================================
# FORM
# =====================================

st.subheader("Upload Invoice")

vendor_name = st.text_input("Vendor Name")

uploaded_file = st.file_uploader(
    "Upload Invoice",
    type=["png", "jpg", "jpeg", "pdf"]
)

amount = st.text_input("Total Amount")

gst_amount = st.text_input("GST Amount")

# =====================================
# FILE PREVIEW
# =====================================

file_bytes = None

if uploaded_file:

    file_bytes = uploaded_file.read()

    st.success("File uploaded successfully")

    # IMAGE PREVIEW
    if uploaded_file.type.startswith("image"):

        st.image(file_bytes, width=300)

    # PDF PREVIEW
    elif uploaded_file.type == "application/pdf":

        st.info("PDF uploaded successfully")

# =====================================
# AI EXTRACTION
# =====================================

if uploaded_file and st.button("Extract Using AI"):

    try:

        with st.spinner("Extracting invoice data using AI..."):

            # Only allow images for AI extraction
            if uploaded_file.type.startswith("image"):

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

Return ONLY valid JSON.

Example:
{
  "amount": "50000",
  "gst_amount": "9000"
}
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
                    ],
                    max_tokens=300
                )

                ai_result = response.choices[0].message.content

                st.subheader("AI Extraction Result")

                st.code(ai_result)

                # Try auto parsing
                try:

                    cleaned = ai_result.replace("```json", "").replace("```", "")

                    data = json.loads(cleaned)

                    if "amount" in data:
                        amount = data["amount"]

                    if "gst_amount" in data:
                        gst_amount = data["gst_amount"]

                    st.success("AI data extracted successfully")

                except:
                    st.warning("AI response could not be auto-filled")

            else:

                st.warning("AI extraction currently supports image files only")

    except Exception as e:

        st.error(f"AI Extraction Error: {str(e)}")

# =====================================
# SUBMIT INVOICE
# =====================================

if st.button("Submit Invoice"):

    try:

        image_url = ""

        # Upload file to Supabase Storage
        if uploaded_file:

            uploaded_file.seek(0)

            unique_name = f"{int(time.time())}_{uploaded_file.name}"

            supabase.storage.from_("invoice-files").upload(
                unique_name,
                uploaded_file.getvalue()
            )

            image_url = (
                f"{SUPABASE_URL}/storage/v1/object/public/"
                f"invoice-files/{unique_name}"
            )

        # Save invoice data
        invoice_data = {
            "vendor_name": vendor_name,
            "amount": amount,
            "gst_amount": gst_amount,
            "status": "Pending",
            "image_url": image_url
        }

        supabase.table("invoices").insert(invoice_data).execute()

        st.success("✅ Invoice submitted successfully")

    except Exception as e:

        st.error(f"Submission Error: {str(e)}")

# =====================================
# VIEW INVOICES
# =====================================

st.markdown("---")

st.subheader("Submitted Invoices")

try:

    rows = supabase.table("invoices").select("*").order(
        "id",
        desc=True
    ).execute()

    if rows.data:

        for row in rows.data:

            with st.container():

                col1, col2 = st.columns([2, 1])

                with col1:

                    st.write(f"### {row['vendor_name']}")
                    st.write(f"💰 Amount: ₹{row['amount']}")
                    st.write(f"🧾 GST: ₹{row['gst_amount']}")
                    st.write(f"📌 Status: {row['status']}")

                with col2:

                    if row["image_url"]:

                        if (
                            row["image_url"].endswith(".png")
                            or row["image_url"].endswith(".jpg")
                            or row["image_url"].endswith(".jpeg")
                        ):

                            st.image(row["image_url"], width=200)

                        else:

                            st.link_button(
                                "View PDF",
                                row["image_url"]
                            )

                st.divider()

    else:

        st.info("No invoices submitted yet")

except Exception as e:

    st.error(f"Database Error: {str(e)}")
