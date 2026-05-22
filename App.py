import streamlit as st
from supabase import create_client
import pandas as pd
import time

# =========================================
# CONFIG
# =========================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================================
# PAGE
# =========================================

st.set_page_config(
    page_title="Invoice Management System",
    layout="wide"
)

st.title("📄 Invoice Management System")

st.markdown("---")

# =========================================
# FILE UPLOAD SECTION
# =========================================

st.subheader("📤 Upload Invoice")

uploaded_file = st.file_uploader(
    "Upload Invoice File",
    type=["pdf", "png", "jpg", "jpeg", "docx"]
)

if uploaded_file:

    st.success("File uploaded successfully")

# =========================================
# VENDOR DETAILS
# =========================================

st.markdown("## 🏢 Vendor Details")

col1, col2 = st.columns(2)

with col1:

    vendor_name = st.text_input(
        "Vendor Name"
    )

    invoice_number = st.text_input(
        "Invoice Number"
    )

with col2:

    invoice_date = st.date_input(
        "Invoice Date"
    )

    category = st.selectbox(
        "Category",
        [
            "Raw Material",
            "Transport",
            "Labour",
            "Equipment",
            "Other"
        ]
    )

# =========================================
# FINANCIAL DETAILS
# =========================================

st.markdown("## 💰 Financial Details")

f1, f2 = st.columns(2)

with f1:

    invoice_amount = st.number_input(
        "Invoice Amount",
        min_value=0.0,
        step=1.0
    )

with f2:

    gst_amount = st.number_input(
        "GST Amount",
        min_value=0.0,
        step=1.0
    )

# AUTO CALCULATION

total_amount = invoice_amount + gst_amount

st.info(
    f"### Total Amount Including GST: ₹ {total_amount:,.2f}"
)

# =========================================
# SUBMIT
# =========================================

if st.button("Submit Invoice"):

    try:

        file_url = ""

        # Upload file
        if uploaded_file:

            unique_name = (
                f"{int(time.time())}_"
                f"{uploaded_file.name}"
            )

            supabase.storage.from_(
                "invoice-files"
            ).upload(
                unique_name,
                uploaded_file.getvalue()
            )

            file_url = (
                f"{SUPABASE_URL}/storage/v1/object/public/"
                f"invoice-files/{unique_name}"
            )

        # Insert data
        data = {

            "vendor_name": vendor_name,

            "invoice_number": invoice_number,

            "invoice_date": str(invoice_date),

            "category": category,

            "invoice_amount": invoice_amount,

            "gst_amount": gst_amount,

            "total_amount": total_amount,

            "status": "Pending",

            "file_url": file_url
        }

        supabase.table(
            "invoices"
        ).insert(data).execute()

        st.success(
            "✅ Invoice Submitted Successfully"
        )

    except Exception as e:

        st.error(f"Error: {e}")

# =========================================
# TRACKING TABLE
# =========================================

st.markdown("---")

st.subheader("📋 Invoice Tracking")

try:

    rows = supabase.table(
        "invoices"
    ).select("*").order(
        "id",
        desc=True
    ).execute()

    if rows.data:

        table_data = []

        for row in rows.data:

            table_data.append({

                "Invoice Number":
                    row["invoice_number"],

                "Vendor":
                    row["vendor_name"],

                "Amount":
                    row["total_amount"],

                "Status":
                    row["status"]

            })

        df = pd.DataFrame(table_data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
            "No invoices submitted yet"
        )

except Exception as e:

    st.error(f"Database Error: {e}")
