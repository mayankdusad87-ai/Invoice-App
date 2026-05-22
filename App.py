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
    page_title="InvoiceFlow AI",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* BACKGROUND */

.stApp {
    background: linear-gradient(
        135deg,
        #eef2ff,
        #f8fafc
    );
}

/* MAIN CONTAINER */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADINGS */

h1, h2, h3 {
    color: #111827;
    font-family: sans-serif;
}

/* CARDS */

.section-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e5e7eb;
}

/* BUTTON */

.stButton > button {

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #6d28d9
    );

    color: white;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stDateInput input {

    border-radius: 10px !important;
}

/* SUCCESS BOX */

.stSuccess {

    border-radius: 12px;
}

/* TABLE */

div[data-testid="stDataFrame"] {

    background: white;
    border-radius: 14px;
    padding: 10px;
}

/* METRIC CARDS */

.metric-card {

    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );

    color: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
}

/* STATUS BADGES */

.pending {
    color: #b45309;
    font-weight: 700;
}

.approved {
    color: #15803d;
    font-weight: 700;
}

.rejected {
    color: #dc2626;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
# 📄 InvoiceFlow AI

### AI-Powered Invoice Processing & Tracking Platform
""")

st.markdown("---")

# =========================================================
# KPI CARDS
# =========================================================

try:

    rows = supabase.table(
        "invoices"
    ).select("*").execute()

    total_invoices = len(rows.data)

    total_amount = sum([
        row["total_amount"]
        for row in rows.data
        if row["total_amount"]
    ])

    pending_count = len([
        row for row in rows.data
        if row["status"] == "Pending"
    ])

except:

    total_invoices = 0
    total_amount = 0
    pending_count = 0

k1, k2, k3 = st.columns(3)

with k1:

    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Invoices</h3>
        <h1>{total_invoices}</h1>
    </div>
    """, unsafe_allow_html=True)

with k2:

    st.markdown(f"""
    <div class="metric-card">
        <h3>Total Amount</h3>
        <h1>₹ {total_amount:,.0f}</h1>
    </div>
    """, unsafe_allow_html=True)

with k3:

    st.markdown(f"""
    <div class="metric-card">
        <h3>Pending Approvals</h3>
        <h1>{pending_count}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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
        "📷 Capture From Camera",
        "📁 Upload File"
    ],
    horizontal=True
)

uploaded_file = None

# CAMERA OPTION

if upload_option == "📷 Capture From Camera":

    uploaded_file = st.camera_input(
        "Take Invoice Photo"
    )

# FILE OPTION

else:

    uploaded_file = st.file_uploader(
        "Upload Invoice",
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

        if uploaded_file.type.startswith("image"):

            st.image(
                uploaded_file,
                width=350
            )

        elif uploaded_file.type == "application/pdf":

            st.info("PDF uploaded successfully")

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

c1, c2 = st.columns(2)

with c1:

    vendor_name = st.text_input(
        "Vendor Name"
    )

    invoice_number = st.text_input(
        "Invoice Number"
    )

with c2:

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
        step=1.0
    )

with f2:

    gst_amount = st.number_input(
        "GST Amount",
        min_value=0.0,
        step=1.0
    )

# TOTAL

total_amount = invoice_amount + gst_amount

st.success(
    f"✅ Total Amount Including GST: ₹ {total_amount:,.2f}"
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SUBMIT BUTTON
# =========================================================

submit_button = st.button(
    "🚀 Submit Invoice"
)

# =========================================================
# SAVE DATA
# =========================================================

if submit_button:

    try:

        file_url = ""

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
            "✅ Invoice Submitted Successfully"
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

            status = row["status"]

            table_data.append({

                "Invoice Number":
                    row["invoice_number"],

                "Vendor":
                    row["vendor_name"],

                "Date":
                    row["invoice_date"],

                "Amount":
                    f"₹ {row['invoice_amount']:,.2f}",

                "GST":
                    f"₹ {row['gst_amount']:,.2f}",

                "Total":
                    f"₹ {row['total_amount']:,.2f}",

                "Status":
                    status

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
    "InvoiceFlow AI • Enterprise Invoice Automation Platform"
)
