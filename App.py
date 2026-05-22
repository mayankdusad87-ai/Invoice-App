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
    page_title="RAGHAV RESERV - Invoice Portal",
    page_icon="🏢",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "landing"

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
MAIN APP
===================================================== */

.stApp {

    background: linear-gradient(
        135deg,
        #eef4ff,
        #dbeafe
    );
}

/* =====================================================
HIDE STREAMLIT DEFAULTS
===================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* =====================================================
MAIN CONTAINER
===================================================== */

.block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* =====================================================
HEADINGS
===================================================== */

h1, h2, h3 {

    color: #0f172a;

    font-family: sans-serif;

    font-weight: 700;
}

/* =====================================================
LABELS
===================================================== */

label {

    color: #111827 !important;

    font-weight: 700 !important;

    font-size: 15px !important;
}

/* =====================================================
HERO SECTION
===================================================== */

.hero {

    background: linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a
    );

    padding: 45px;

    border-radius: 28px;

    text-align: center;

    color: white;

    margin-bottom: 35px;

    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
}

.hero-title {

    font-size: 50px;

    font-weight: 800;

    margin-bottom: 12px;
}

.hero-subtitle {

    font-size: 20px;

    opacity: 0.92;
}

/* =====================================================
SECTION CARDS
===================================================== */

.card {

    background: white;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 24px;

    box-shadow: 0 8px 25px rgba(0,0,0,0.06);

    border: 1px solid #dbeafe;
}

/* =====================================================
PORTAL CARDS
===================================================== */

.portal-card {

    background: white;

    padding: 35px;

    border-radius: 24px;

    text-align: center;

    box-shadow: 0 8px 25px rgba(0,0,0,0.08);

    border: 1px solid #dbeafe;

    margin-bottom: 20px;
}

/* =====================================================
BUTTONS
===================================================== */

.stButton > button {

    background: linear-gradient(
        90deg,
        #2563eb,
        #0284c7
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 14px 28px;

    font-size: 16px;

    font-weight: 700;

    width: 100%;
}

.stButton > button:hover {

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #0369a1
    );

    color: white;
}

/* =====================================================
INPUTS
===================================================== */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {

    border-radius: 14px !important;

    border: 1px solid #cbd5e1 !important;

    background-color: #ffffff !important;

    color: #111827 !important;

    font-weight: 500 !important;
}

/* =====================================================
RADIO
===================================================== */

div[role="radiogroup"] {

    background: #f8fafc;

    padding: 12px;

    border-radius: 14px;

    border: 1px solid #dbeafe;
}

/* =====================================================
DATAFRAME
===================================================== */

div[data-testid="stDataFrame"] {

    background: white;

    border-radius: 18px;

    padding: 10px;

    border: 1px solid #dbeafe;
}

/* =====================================================
NOTE
===================================================== */

.note {

    color: #dc2626;

    font-size: 14px;

    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LANDING PAGE
# =========================================================

if st.session_state.page == "landing":

    st.markdown("""
    <div class="hero">

    <div class="hero-title">
    🏢 RAGHAV RESERV
    </div>

    <div class="hero-subtitle">
    Enterprise Invoice Submission & Approval Portal
    </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div class="portal-card">

        <h2>📤 Vendor Portal</h2>

        <p>
        Submit invoices and track approvals
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Vendor Portal"):

            st.session_state.page = "vendor"

            st.rerun()

    with c2:

        st.markdown("""
        <div class="portal-card">

        <h2>🛠 Admin Portal</h2>

        <p>
        Review and approve invoices
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Admin Portal"):

            st.session_state.page = "admin_login"

            st.rerun()

# =========================================================
# VENDOR PORTAL
# =========================================================

elif st.session_state.page == "vendor":

    if st.button("⬅ Back to Home"):

        st.session_state.page = "landing"

        st.rerun()

    st.markdown("""
    <div class="hero">

    <div class="hero-title">
    📤 Vendor Invoice Submission
    </div>

    <div class="hero-subtitle">
    Submit invoices and track approvals
    </div>

    </div>
    """, unsafe_allow_html=True)

    # =====================================================
    # EMAIL
    # =====================================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("👤 Vendor Access")

    vendor_email = st.text_input(
        "Vendor Email *"
    )

    st.markdown(
        '<div class="note">* Mandatory Fields</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # UPLOAD
    # =====================================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

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

            else:

                st.info(
                    "Document uploaded successfully"
                )

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # DETAILS
    # =====================================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🏢 Vendor Details")

    c1, c2 = st.columns(2)

    with c1:

        vendor_name = st.text_input(
            "Vendor Name *"
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

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # FINANCE
    # =====================================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # SUBMIT
    # =====================================================

    if st.button("🚀 Submit Invoice"):

        missing_fields = []

        if not vendor_email:

            missing_fields.append(
                "Vendor Email"
            )

        if not vendor_name:

            missing_fields.append(
                "Vendor Name"
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
    # MY INVOICES
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
                "No invoices found"
            )

    except Exception as e:

        st.error(
            f"Database Error: {e}"
        )

# =========================================================
# ADMIN LOGIN
# =========================================================

elif st.session_state.page == "admin_login":

    if st.button("⬅ Back to Home"):

        st.session_state.page = "landing"

        st.rerun()

    st.markdown("""
    <div class="hero">

    <div class="hero-title">
    🔐 Admin Portal
    </div>

    <div class="hero-subtitle">
    Invoice Review & Approval Dashboard
    </div>

    </div>
    """, unsafe_allow_html=True)

    admin_password = st.text_input(
        "Enter Admin Password",
        type="password"
    )

    if st.button("Login as Admin"):

        if admin_password == "admin123":

            st.session_state.page = "admin_dashboard"

            st.rerun()

        else:

            st.error(
                "Incorrect Password"
            )

# =========================================================
# ADMIN DASHBOARD
# =========================================================

elif st.session_state.page == "admin_dashboard":

    if st.button("⬅ Logout"):

        st.session_state.page = "landing"

        st.rerun()

    st.markdown("""
    <div class="hero">

    <div class="hero-title">
    🛠 Admin Dashboard
    </div>

    <div class="hero-subtitle">
    Manage Invoice Approvals
    </div>

    </div>
    """, unsafe_allow_html=True)

    try:

        rows = supabase.table(
            "invoices"
        ).select("*").order(
            "id",
            desc=True
        ).execute()

        if rows.data:

            for row in rows.data:

                st.markdown('<div class="card">', unsafe_allow_html=True)

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

                st.markdown('</div>', unsafe_allow_html=True)

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
    "RAGHAV RESERVE • Enterprise Invoice Submission Portal"
)
