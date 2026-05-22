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
    page_title="RAGHAV RESERV - Invoice Submission",
    page_icon="🏢",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(
        135deg,
        #f1f5f9,
        #e0f2fe
    );
}

/* MAIN CONTAINER */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADINGS */

h1, h2, h3 {
    color: #0f172a;
    font-family: sans-serif;
}

/* HERO SECTION */

.hero-section {

    background: linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a
    );

    padding: 40px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;

    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}

.hero-title {

    font-size: 42px;
    font-weight: 700;
}

.hero-subtitle {

    font-size: 18px;
    opacity: 0.9;
}

/* CARDS */

.section-card {

    background: white;

    padding: 24px;

    border-radius: 20px;

    margin-bottom: 24px;

    box-shadow: 0 8px 25px rgba(0,0,0,0.06);

    border: 1px solid #e2e8f0;
}

/* BUTTON */

.stButton > button {

    background: linear-gradient(
        90deg,
        #2563eb,
        #0ea5e9
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
        #0284c7
    );

    color: white;
}

/* INPUTS */

.stTextInput input,
.stNumberInput input,
.stDateInput input {

    border-radius: 10px !important;
}

/* METRIC CARDS */

.metric-card {

    background: linear-gradient(
        135deg,
        #2563eb,
        #0ea5e9
    );

    color: white;

    padding: 20px;

    border-radius: 20px;

    text-align: center;

    box-shadow: 0 8px 20px rgba(37,99,235,0.2);
}

/* DATAFRAME */

div[data-testid="stDataFrame"] {

    background: white;

    border-radius: 16px;

    padding: 10px;
}

/* MANDATORY NOTE */

.mandatory-note {

    color: red;

    font-size: 14px;

    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LANDING PAGE HEADER
# =========================================================

st.markdown("""
<div class="hero-section">

<div class="hero-title">
🏢 RAGHAV RESERV
</div>

<div class="hero-subtitle">
Enterprise Invoice Submission & Approval Portal
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# PORTAL SELECTION
# =========================================================

portal = st.selectbox(
    "Choose Portal",
    [
        "Vendor Portal",
        "Admin Portal"
    ]
)

# =========================================================
# ADMIN LOGIN
# =========================================================

is_admin = False

if portal == "Admin Portal":

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("🔐 Admin Login")

    admin_password = st.text_input(
        "Enter Admin Password",
        type="password"
    )

    if admin_password == "admin123":

        is_admin = True

        st.success(
            "Admin Access Granted"
        )

    else:

        st.warning(
            "Please enter admin password"
        )

        st.stop()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

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
# VENDOR PORTAL
# =========================================================

if portal == "Vendor Portal":

    # =====================================================
    # UPLOAD SECTION
    # =====================================================

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

    if upload_option == "📷 Capture From Camera":

        uploaded_file = st.camera_input(
            "Take Invoice Photo"
        )

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

    if uploaded_file:

        st.success(
            "File uploaded successfully"
        )

        if hasattr(uploaded_file, "type"):

            if uploaded_file.type.startswith(
                "image"
            ):

                st.image(
                    uploaded_file,
                    width=350
                )

            elif uploaded_file.type == (
                "application/pdf"
            ):

                st.info(
                    "PDF uploaded successfully"
                )

            else:

                st.info(
                    "Document uploaded successfully"
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # VENDOR DETAILS
    # =====================================================

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("🏢 Vendor Details")

    st.markdown(
        '<div class="mandatory-note">* Mandatory Fields</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        vendor_name = st.text_input(
            "Vendor Name *"
        )

        vendor_email = st.text_input(
            "Vendor Email *"
        )

        invoice_number = st.text_input(
            "Invoice Number *"
        )

    with c2:

        invoice_date = st.date_input(
            "Invoice Date *"
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

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # FINANCIAL DETAILS
    # =====================================================

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

    total_amount = (
        invoice_amount + gst_amount
    )

    st.success(
        f"✅ Total Amount Including GST: ₹ {total_amount:,.2f}"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # SUBMIT BUTTON
    # =====================================================

    submit_button = st.button(
        "🚀 Submit Invoice"
    )

    # =====================================================
    # VALIDATION + SAVE
    # =====================================================

    if submit_button:

        missing_fields = []

        if not vendor_name:

            missing_fields.append(
                "Vendor Name"
            )

        if not vendor_email:

            missing_fields.append(
                "Vendor Email"
            )

        if not invoice_number:

            missing_fields.append(
                "Invoice Number"
            )

        if not invoice_date:

            missing_fields.append(
                "Invoice Date"
            )

        if missing_fields:

            st.error(
                "Missing Mandatory Fields: "
                + ", ".join(missing_fields)
            )

        else:

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

                    "vendor_email":
                        vendor_email,

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

    # =====================================================
    # VENDOR TABLE
    # =====================================================

    st.markdown("---")

    st.subheader("📋 My Invoices")

    try:

        rows = supabase.table(
            "invoices"
        ).select("*").eq(
            "vendor_email",
            vendor_email
        ).order(
            "id",
            desc=True
        ).execute()

        if rows.data:

            table_data = []

            for row in rows.data:

                table_data.append({

                    "Invoice Number":
                        row["invoice_number"],

                    "Amount":
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
# ADMIN PORTAL
# =========================================================

if is_admin:

    st.subheader(
        "🛠 Admin Invoice Dashboard"
    )

    try:

        rows = supabase.table(
            "invoices"
        ).select("*").order(
            "id",
            desc=True
        ).execute()

        if rows.data:

            for row in rows.data:

                st.markdown(
                    '<div class="section-card">',
                    unsafe_allow_html=True
                )

                c1, c2, c3, c4 = st.columns(
                    [2, 2, 2, 2]
                )

                with c1:

                    st.write(
                        f"### {row['invoice_number']}"
                    )

                    st.write(
                        f"Vendor: {row['vendor_name']}"
                    )

                    st.write(
                        f"Email: {row['vendor_email']}"
                    )

                with c2:

                    st.write(
                        f"💰 Amount: ₹ {row['invoice_amount']:,.2f}"
                    )

                    st.write(
                        f"🧾 GST: ₹ {row['gst_amount']:,.2f}"
                    )

                    st.write(
                        f"💵 Total: ₹ {row['total_amount']:,.2f}"
                    )

                with c3:

                    st.write(
                        f"📌 Status: {row['status']}"
                    )

                    st.write(
                        f"📅 Date: {row['invoice_date']}"
                    )

                    st.write(
                        f"📂 Category: {row['category']}"
                    )

                with c4:

                    if row["file_url"]:

                        st.link_button(
                            "View Invoice",
                            row["file_url"]
                        )

                    status = st.selectbox(
                        "Change Status",
                        [
                            "Pending",
                            "Approved",
                            "Rejected"
                        ],
                        key=f"status_{row['id']}"
                    )

                    if st.button(
                        "Update Status",
                        key=f"update_{row['id']}"
                    ):

                        supabase.table(
                            "invoices"
                        ).update({

                            "status": status

                        }).eq(
                            "id",
                            row["id"]
                        ).execute()

                        st.success(
                            "Status Updated"
                        )

                        st.rerun()

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No invoices found"
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
    "RAGHAV RESERV • Enterprise Invoice Submission Portal"
)
