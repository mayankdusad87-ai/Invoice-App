import streamlit as st
from supabase import create_client
import pandas as pd
import time

# =========================================================
# CONFIGURATION
# =========================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Invoice Management System",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f4f7fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #111827;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.6rem 1.5rem;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
}

.upload-box {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #dbeafe;
    margin-bottom: 20px;
}

.section-card {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    margin-bottom: 20px;
    border: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.title("📄 Invoice Management System")

st.markdown("""
Upload invoices, manage vendor details,
track approvals, and automate invoice processing.
""")

st.markdown("---")

# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="section-card">',
    unsafe_allow_html=True
)

st.subheader("📤 Upload Invoice")

upload_option = st.radio(
    "Choose Upload Method",
    [
        "Capture From Camera",
        "Upload File"
    ],
    horizontal=True
)

uploaded_file = None

# CAMERA OPTION
if upload_option == "Capture From Camera":

    uploaded_file = st.camera_input(
        "Take Invoice Photo"
    )

# FILE OPTION
else:

    uploaded_file = st.file_uploader(
        "Upload Invoice File",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg",
            "docx"
        ]
    )

# PREVIEW
if uploaded_file:

    st.success("File uploaded successfully")

    if hasattr(uploaded_file, "type"):

        # IMAGE PREVIEW
        if uploaded_file.type.startswith("image"):

            st.image(
                uploaded_file,
                width=350
            )

        # PDF
        elif uploaded_file.type == "application/pdf":

            st.info("PDF uploaded successfully")

        # DOCX
        else:

            st.info("Document uploaded successfully")

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# VENDOR DETAILS
# =========================================================

st.markdown(
    '<div class="section-card">',
    unsafe_allow_html=True
)

st.subheader("🏢 Vendor Details")

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
            "Professional Services",
            "Other"
        ]
    )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FINANCIAL DETAILS
# =========================================================

st.markdown(
    '<div class="section-card">',
    unsafe_allow_html=True
)

st.subheader("💰 Financial Details")

f1, f2 = st.columns(2)

with f1:

    invoice_amount = st.number_input(
        "Invoice Amount",
        min_value=0.0,
        step=1.0,
        format="%.2f"
    )

with f2:

    gst_amount = st.number_input(
        "GST Amount",
        min_value=0.0,
        step=1.0,
        format="%.2f"
    )

# AUTO CALCULATION

total_amount = invoice_amount + gst_amount

st.success(
    f"✅ Total Amount Including GST: ₹ {total_amount:,.2f}"
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SUBMIT BUTTON
# =========================================================

submit_col1, submit_col2, submit_col3 = st.columns([1, 1, 4])

with submit_col1:

    submit_button = st.button(
        "Submit Invoice"
    )

# =========================================================
# SAVE DATA
# =========================================================

if submit_button:

    try:

        file_url = ""

        # ---------------------------------------------
        # FILE UPLOAD TO SUPABASE STORAGE
        # ---------------------------------------------

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

        # ---------------------------------------------
        # DATABASE INSERT
        # ---------------------------------------------

        data = {

            "vendor_name":
                vendor_name,

            "invoice_number":
                invoice_number,

            "invoice_date":
                str(invoice_date),

            "category":
                category,

            "invoice_amount":
                invoice_amount,

            "gst_amount":
                gst_amount,

            "total_amount":
                total_amount,

            "status":
                "Pending",

            "file_url":
                file_url
        }

        supabase.table(
            "invoices"
        ).insert(
            data
        ).execute()

        st.success(
            "✅ Invoice submitted successfully"
        )

    except Exception as e:

        st.error(
            f"Submission Error: {e}"
        )

# =========================================================
# TRACKING TABLE
# =========================================================

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

                "Invoice Date":
                    row["invoice_date"],

                "Amount":
                    f"₹ {row['invoice_amount']:,.2f}",

                "GST":
                    f"₹ {row['gst_amount']:,.2f}",

                "Total":
                    f"₹ {row['total_amount']:,.2f}",

                "Status":
                    row["status"]

            })

        df = pd.DataFrame(
            table_data
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No invoices submitted yet"
        )

except Exception as e:

    st.error(
        f"Database Error: {e}"
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "AI Invoice Management MVP • Streamlit + Supabase"
)
