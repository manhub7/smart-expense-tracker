# new file app.py
import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="💸 Smart Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
def load_css():
    st.markdown("""
    <style>
        /* ==================== ANIMATIONS ==================== */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes glowPulse {
            0%, 100% { box-shadow: 0 0 5px rgba(0, 255, 200, 0.3); border-color: rgba(0, 255, 200, 0.3); }
            50% { box-shadow: 0 0 20px rgba(0, 255, 200, 0.6); border-color: #00ffcc; }
        }
        @keyframes buttonRipple {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(50px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes shimmer {
            0% { background-position: -100% 0; }
            100% { background-position: 100% 0; }
        }

        /* ==================== MAIN BACKGROUND ==================== */
        .stApp {
            background: linear-gradient(135deg, #0a0e1a 0%, #0f1420 50%, #0a0e1a 100%);
            animation: fadeInUp 0.6s ease-out;
        }

        /* ==================== HEADER ANIMATION ==================== */
        header {
            background: rgba(10, 14, 26, 0.95) !important;
            backdrop-filter: blur(10px) !important;
            border-bottom: 1px solid rgba(0, 255, 200, 0.3) !important;
            padding: 8px 20px !important;
            animation: slideInLeft 0.5s ease-out !important;
        }

        /* ==================== BUTTONS WITH ANIMATIONS ==================== */
        .stButton > button {
            background: linear-gradient(90deg, #00ccff, #00ffcc);
            color: #0a0e1a;
            border-radius: 10px;
            padding: 8px 20px !important;
            font-weight: bold;
            font-size: 0.9rem !important;
            transition: all 0.3s ease;
            border: none;
            min-height: 36px !important;
            position: relative;
            overflow: hidden;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0, 255, 200, 0.5);
            background: linear-gradient(90deg, #00ffcc, #00ccff);
            animation: buttonRipple 0.3s ease;
        }
        .stButton > button:active { transform: scale(0.98); }

        button:has(span:contains("Get Started")),
        button:has(span:contains("Start Tracking Now")) {
            padding: 14px 40px !important;
            font-size: 1.1rem !important;
            min-height: 52px !important;
            border-radius: 30px !important;
            animation: glowPulse 2s infinite !important;
            background: linear-gradient(90deg, #00ffcc, #00ccff, #00ffcc);
            background-size: 200% 200%;
        }
        button:has(span:contains("Get Started")):hover,
        button:has(span:contains("Start Tracking Now")):hover {
            animation: none !important;
            transform: scale(1.05);
        }

        /* ==================== INPUT FIELDS ==================== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div,
        .stDateInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 10px;
            border: 1px solid #2a2f3e;
            background: #1a1f2e;
            color: #ffffff;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #00ffcc;
            box-shadow: 0 0 15px rgba(0, 255, 200, 0.3);
            transform: scale(1.01);
        }
        .stTextInput label, .stNumberInput label, .stSelectbox label, .stDateInput label {
            color: #00ffcc !important;
            font-weight: 500;
        }

        /* ==================== TYPOGRAPHY ==================== */
        h1 {
            background: linear-gradient(135deg, #ffffff, #00ffcc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: slideInLeft 0.5s ease-out;
        }
        h2, h3, h4 { color: #ffffff !important; }
        .stMarkdown p { color: #cccccc; line-height: 1.6; }

        /* ==================== FEATURE CARDS ==================== */
        .feature-card {
            background: linear-gradient(135deg, #1a1f2e, #141925);
            border-radius: 15px;
            padding: 25px 15px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid rgba(0, 255, 200, 0.2);
            animation: fadeInUp 0.6s ease-out;
            height: 100%;
        }
        .feature-card:hover {
            transform: translateY(-8px);
            border-color: #00ffcc;
            box-shadow: 0 15px 35px rgba(0, 255, 200, 0.25);
        }
        .feature-icon { font-size: 2.5rem; margin-bottom: 10px; }
        .feature-title { color: #00ffcc; font-size: 1.1rem; font-weight: bold; margin: 10px 0; }
        .feature-desc { color: #aaaaaa; font-size: 0.85rem; line-height: 1.5; }

        /* ==================== PROFESSIONAL METRIC CARDS ==================== */
        .metric-card {
            background: linear-gradient(135deg, #1a1f2e, #141925);
            border-radius: 16px;
            padding: 22px 20px;
            border: 1px solid rgba(0, 255, 200, 0.15);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: fadeInUp 0.5s ease-out;
            position: relative;
            overflow: hidden;
            height: 100%;
        }
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00ffcc, #00ccff, #00ffcc);
            background-size: 200% 100%;
            animation: shimmer 3s infinite;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: rgba(0, 255, 200, 0.5);
            box-shadow: 0 12px 30px rgba(0, 255, 200, 0.2);
        }
        .metric-icon { font-size: 1.8rem; margin-bottom: 8px; opacity: 0.9; }
        .metric-label {
            color: #8a92a6;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        .metric-value {
            color: #ffffff;
            font-size: 1.6rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff, #00ffcc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* ==================== DASHBOARD HEADER ==================== */
        .dash-header {
            background: linear-gradient(135deg, rgba(26, 31, 46, 0.9), rgba(20, 25, 37, 0.9));
            border-radius: 16px;
            padding: 25px 30px;
            border: 1px solid rgba(0, 255, 200, 0.2);
            margin-bottom: 25px;
            animation: fadeInUp 0.5s ease-out;
        }
        .dash-header h1 {
            margin: 0;
            font-size: 1.8rem;
        }
        .dash-header p {
            margin: 5px 0 0 0;
            color: #8a92a6;
            font-size: 0.9rem;
        }

        /* ==================== SECTION TITLES ==================== */
        .section-title {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 25px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(0, 255, 200, 0.15);
        }
        .section-title h3 {
            margin: 0;
            color: #ffffff;
            font-size: 1.2rem;
            font-weight: 600;
        }

        /* ==================== RECENT EXPENSE ROW ==================== */
        .expense-row {
            background: linear-gradient(135deg, #1a1f2e, #141925);
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 8px;
            border: 1px solid rgba(0, 255, 200, 0.1);
            transition: all 0.25s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .expense-row:hover {
            border-color: rgba(0, 255, 200, 0.4);
            transform: translateX(4px);
            background: linear-gradient(135deg, #1f2433, #191e2c);
        }
        .expense-cat { color: #00ffcc; font-weight: 600; font-size: 0.9rem; }
        .expense-note { color: #8a92a6; font-size: 0.8rem; margin-top: 2px; }
        .expense-amt { color: #ffffff; font-weight: 700; font-size: 1rem; }
        .expense-date { color: #8a92a6; font-size: 0.75rem; }

        /* ==================== ALERTS ==================== */
        .stAlert {
            background: #1a1f2e;
            border-left: 4px solid #00ffcc;
            border-radius: 10px;
            animation: slideInRight 0.4s ease-out;
        }

        /* ==================== SIDEBAR ==================== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0e1a, #0f1420);
            border-right: 1px solid rgba(0, 255, 200, 0.2);
            animation: slideInLeft 0.5s ease-out;
        }

        /* ==================== DATA FRAME ==================== */
        .stDataFrame { border-radius: 12px; overflow: hidden; }
        .stDataFrame table { background: #1a1f2e; color: #ffffff; }
        .stDataFrame thead tr th {
            background: linear-gradient(135deg, #1a1f2e, #141925);
            color: #00ffcc;
            border-bottom: 2px solid #00ffcc;
        }
        .stDataFrame tbody tr { transition: all 0.2s ease; }
        .stDataFrame tbody tr:hover { background: rgba(0, 255, 200, 0.1); }

        /* ==================== TABS ==================== */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(26, 31, 46, 0.6);
            border-radius: 10px;
            padding: 5px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 8px 20px;
            color: #aaaaaa;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(0, 255, 200, 0.15);
            color: #00ffcc;
            transform: translateY(-2px);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00ccff, #00ffcc);
            color: #0a0e1a;
            font-weight: bold;
            transform: scale(1.02);
        }

        /* ==================== PROGRESS BAR ==================== */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #00ffcc, #00ccff, #00ffcc);
            background-size: 200% 100%;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }

        /* ==================== DIVIDERS ==================== */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00ffcc, #00ccff, #00ffcc, transparent);
            margin: 20px 0;
        }

        /* ==================== SCROLLBAR ==================== */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #1a1f2e; border-radius: 10px; }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00ffcc, #00ccff);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #00ccff, #00ffcc);
        }

        /* ==================== EXPANDER ==================== */
        .streamlit-expanderHeader {
            color: #00ffcc !important;
            background: linear-gradient(135deg, #1a1f2e, #141925);
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        .streamlit-expanderHeader:hover {
            transform: translateX(5px);
            background: linear-gradient(135deg, #1f2433, #191e2c);
        }
        .streamlit-expanderContent {
            background: #1a1f2e;
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 200, 0.1);
        }

        /* ==================== EDIT/DELETE BUTTONS ==================== */
        button:has(span:contains("✏️")),
        button:has(span:contains("🗑️")) {
            background: linear-gradient(90deg, #2a2f3e, #1a1f2e) !important;
            color: #00ffcc !important;
            padding: 4px 10px !important;
            font-size: 0.9rem !important;
            min-height: 32px !important;
            width: 40px !important;
            border: 1px solid rgba(0, 255, 200, 0.3) !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        button:has(span:contains("✏️")):hover,
        button:has(span:contains("🗑️")):hover {
            background: linear-gradient(90deg, #3a3f4e, #2a2f3e) !important;
            transform: scale(1.1) !important;
            border-color: #00ffcc !important;
            box-shadow: 0 0 10px rgba(0, 255, 200, 0.3) !important;
        }

        /* ==================== CHART CONTAINERS ==================== */
        .stPlotlyChart { animation: fadeInUp 0.6s ease-out; }
        .stSuccess, .stError, .stWarning, .stInfo {
            animation: slideInRight 0.4s ease-out;
        }

        /* ==================== HERO SECTION ==================== */
        .hero-image {
            animation: slideInRight 0.8s ease-out;
            text-align: center;
        }
        .hero-image svg {
            filter: drop-shadow(0 10px 30px rgba(0, 255, 200, 0.3));
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff, #00ffcc, #00ccff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: slideInLeft 0.6s ease-out;
            line-height: 1.15;
        }
        .hero-subtitle {
            font-size: 1.05rem;
            color: #8a92a6;
            margin-top: 18px;
            animation: fadeInUp 0.8s ease-out;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ==================== DATA FILES ====================
USERS_FILE = "users.json"
EXPENSES_FILE = "expenses.json"

def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "w") as f:
            json.dump({}, f)

init_files()

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_expenses():
    with open(EXPENSES_FILE, "r") as f:
        return json.load(f)

def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# ==================== SESSION STATE ====================
if "user" not in st.session_state:
    st.session_state.user = None
if "show_auth" not in st.session_state:
    st.session_state.show_auth = False
if "notification" not in st.session_state:
    st.session_state.notification = None
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
if "edit_data" not in st.session_state:
    st.session_state.edit_data = None
if "monthly_budget" not in st.session_state:
    st.session_state.monthly_budget = 1000.0

def show_notification(msg, type="success"):
    st.session_state.notification = {"msg": msg, "type": type}

# ==================== HEADER & FOOTER ====================
def show_header():
    if st.session_state.user is None:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write("💸 **Smart Expense Tracker**")
        with col2:
            if st.button("📖 About Us", key="about_btn", use_container_width=True):
                st.info("Smart Expense Tracker helps you manage your finances effortlessly with smart analytics and insights.")
        with col3:
            if st.button("🔐 Login", key="header_login", use_container_width=True):
                st.session_state.show_auth = True
                st.rerun()
        st.divider()

def show_footer():
    if st.session_state.user is None:
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("**💸 Smart Expense Tracker**")
            st.write("Take control of your finances.")
        with col2:
            st.write("**Quick Links**")
            st.write("• Home")
            st.write("• Features")
            st.write("• Support")
        with col3:
            st.write("**Legal**")
            st.write("• Privacy Policy")
            st.write("• Terms of Service")
        with col4:
            st.write("**Connect**")
            st.write("📧 support@smarttracker.com")
        st.divider()
        st.caption("© 2024 Smart Expense Tracker | Made with 💚")

# ==================== HERO SVG (from old code) ====================
def get_hero_svg():
    return '''
    <svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#00ffcc;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#00ccff;stop-opacity:1" />
            </linearGradient>
        </defs>
        <circle cx="200" cy="200" r="180" fill="none" stroke="url(#grad)" stroke-width="3" stroke-dasharray="10 5">
            <animate attributeName="stroke-dashoffset" values="0;1000" dur="20s" repeatCount="indefinite" />
        </circle>
        <path d="M200 80 L220 140 L280 150 L240 190 L260 260 L200 220 L140 260 L160 190 L120 150 L180 140 Z" fill="url(#grad)" opacity="0.8">
            <animate attributeName="opacity" values="0.5;0.9;0.5" dur="3s" repeatCount="indefinite" />
        </path>
        <text x="200" y="330" text-anchor="middle" fill="white" font-size="14">Track. Analyze. Save.</text>
        <circle cx="200" cy="200" r="60" fill="none" stroke="url(#grad)" stroke-width="2">
            <animate attributeName="r" values="60;70;60" dur="2s" repeatCount="indefinite" />
        </circle>
    </svg>
    '''

# ==================== AUTH FUNCTIONS ====================
def signup(username, password):
    users = load_users()
    if username in users:
        return False, "Username already exists!"
    users[username] = {
        "password": password,
        "created": str(datetime.now()),
        "total_expenses": 0,
        "monthly_budget": 1000.0
    }
    save_users(users)
    expenses = load_expenses()
    expenses[username] = []
    save_expenses(expenses)
    return True, "Signup successful! Please login."

def login(username, password):
    users = load_users()
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        st.session_state.show_auth = False
        st.session_state.monthly_budget = users[username].get("monthly_budget", 1000.0)
        return True, f"Welcome back, {username}!"
    return False, "Invalid credentials!"

# ==================== EXPENSE FUNCTIONS ====================
def add_expense(username, expense_data):
    expenses = load_expenses()
    if username not in expenses:
        expenses[username] = []
    expenses[username].append(expense_data)
    save_expenses(expenses)
    users = load_users()
    users[username]["total_expenses"] = len(expenses[username])
    save_users(users)

def delete_expense(username, index):
    expenses = load_expenses()
    if username in expenses and 0 <= index < len(expenses[username]):
        expenses[username].pop(index)
        save_expenses(expenses)
        users = load_users()
        users[username]["total_expenses"] = len(expenses[username])
        save_users(users)
        return True
    return False

def edit_expense(username, index, new_data):
    expenses = load_expenses()
    if username in expenses and 0 <= index < len(expenses[username]):
        expenses[username][index] = new_data
        save_expenses(expenses)
        return True
    return False

def get_user_expenses_df(username):
    expenses = load_expenses()
    data = expenses.get(username, [])
    if data:
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return pd.DataFrame()

# ==================== EXPORT FUNCTIONS ====================
def export_to_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="expenses.csv" style="color: #00ffcc;">📥 Download CSV</a>'

def export_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Expenses')
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="expenses.xlsx" style="color: #00ffcc;">📥 Download Excel</a>'

# ==================== ANALYTICS CHARTS ====================
def create_pie_chart(df):
    if not df.empty:
        category_sum = df.groupby('Category')['Amount'].sum()
        fig = px.pie(values=category_sum.values, names=category_sum.index,
                     title="Expense Distribution", hole=0.3)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white'), title_font=dict(color='#00ffcc'))
        return fig
    return None

def create_bar_chart(df):
    if not df.empty:
        category_sum = df.groupby('Category')['Amount'].sum().sort_values()
        fig = px.bar(x=category_sum.values, y=category_sum.index, orientation='h',
                     title="Category-wise Spending", color=category_sum.values,
                     color_continuous_scale='Tealgrn')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white'), title_font=dict(color='#00ffcc'))
        return fig
    return None

def create_line_chart(df):
    if not df.empty and len(df) > 1:
        daily = df.groupby(df['Date'].dt.date)['Amount'].sum().reset_index()
        fig = px.line(daily, x='Date', y='Amount', title="Spending Over Time", markers=True)
        fig.update_traces(line=dict(color='#00ffcc', width=3), marker=dict(size=8, color='#00ccff'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white'), title_font=dict(color='#00ffcc'))
        return fig
    return None

def create_monthly_chart(df):
    if not df.empty:
        df['Month'] = df['Date'].dt.strftime('%B %Y')
        monthly = df.groupby('Month')['Amount'].sum().reset_index()
        fig = px.bar(monthly, x='Month', y='Amount', title="Monthly Spending", color='Amount')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         font=dict(color='white'), title_font=dict(color='#00ffcc'),
                         xaxis=dict(tickangle=-45))
        return fig
    return None

# ==================== HOME PAGE ====================
def home_page():
    # ===== HERO SECTION with Animated SVG =====
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div style="padding-top: 60px;"><h1 class="hero-title">Take Control<br>of Your Money 💸</h1><p class="hero-subtitle">Track, analyze and manage your expenses effortlessly<br>with our premium expense tracker.</p></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 Get Started", key="get_started_btn"):
            st.session_state.show_auth = True
            st.rerun()

    with col2:
        st.markdown(f'<div class="hero-image">{get_hero_svg()}</div>', unsafe_allow_html=True)

    st.divider()

    # ===== FEATURES SECTION =====
    st.write("## ✨ Premium Features")
    st.caption("Everything you need to manage your finances")
    st.write("")

    col1, col2, col3, col4 = st.columns(4)
    features = [
        ("📊", "Smart Analytics", "Real-time insights and beautiful visualizations"),
        ("🔐", "Secure Data", "Your financial data is encrypted and private"),
        ("⚡", "Fast & Easy", "Add expenses in seconds with our intuitive interface"),
        ("📱", "Export Reports", "Download CSV/Excel reports for accounting")
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>', unsafe_allow_html=True)

    st.divider()

    # ===== STATS SECTION =====
    st.write("## Trusted by Users Worldwide")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card" style="text-align:center;"><div class="metric-icon">💰</div><div class="metric-value">Rs10M+</div><div class="metric-label">Expenses Tracked</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card" style="text-align:center;"><div class="metric-icon">👥</div><div class="metric-value">50K+</div><div class="metric-label">Happy Users</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card" style="text-align:center;"><div class="metric-icon">⭐</div><div class="metric-value">4.9/5</div><div class="metric-label">User Rating</div></div>', unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("## Ready to take control?")
        st.write("Join thousands of users managing their finances smarter.")
        if st.button("Start Tracking Now 🚀", use_container_width=True):
            st.session_state.show_auth = True
            st.rerun()

# ==================== AUTH PAGE ====================
def auth_page():
    st.write("# Welcome Back!")
    st.caption("Sign in to continue to your dashboard")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Signup"])

        with tab1:
            username = st.text_input("Username", placeholder="Enter your username", key="login_user")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")

            if st.button("Login", use_container_width=True):
                if username and password:
                    success, msg = login(username, password)
                    if success:
                        show_notification(msg, "success")
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter both username and password")

        with tab2:
            username = st.text_input("Username", placeholder="Choose a username", key="signup_user")
            password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_pass")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")

            if st.button("Create Account", use_container_width=True):
                if username and password and confirm:
                    if password != confirm:
                        st.error("Passwords do not match!")
                    else:
                        success, msg = signup(username, password)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                else:
                    st.warning("Please fill all fields")

    if st.button("← Back to Home"):
        st.session_state.show_auth = False
        st.rerun()

# ==================== PROFESSIONAL DASHBOARD PAGE ====================
def dashboard_page():
    # ===== DASHBOARD HEADER =====
    st.markdown(f'<div class="dash-header"><h1>📊 Dashboard</h1><p>Welcome back, <b style="color:#00ffcc;">{st.session_state.user}</b> — here\'s your financial overview</p></div>', unsafe_allow_html=True)

    df = get_user_expenses_df(st.session_state.user)

    if not df.empty:
        total_spending = df['Amount'].sum()
        monthly_spending = df[df['Date'].dt.month == datetime.now().month]['Amount'].sum()
        category_count = df['Category'].nunique()
        avg_expense = df['Amount'].mean()

        # ===== METRIC CARDS (Professional) =====
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">💰</div><div class="metric-label">Total Spending</div><div class="metric-value">Rs {total_spending:,.2f}</div></div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">📈</div><div class="metric-label">This Month</div><div class="metric-value">Rs {monthly_spending:,.2f}</div></div>', unsafe_allow_html=True)

        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">📊</div><div class="metric-label">Categories</div><div class="metric-value">{category_count}</div></div>', unsafe_allow_html=True)

        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-icon">📝</div><div class="metric-label">Total Entries</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)

        st.write("")

        # ===== BUDGET TRACKER =====
        st.markdown('<div class="section-title"><h3>💰 Budget Tracker</h3></div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            budget = st.number_input(
                "Set Monthly Budget (Rs)",
                min_value=0.0,
                value=st.session_state.monthly_budget,
                step=100.0,
                key="monthly_budget_input"
            )
            if budget != st.session_state.monthly_budget:
                st.session_state.monthly_budget = budget
                users = load_users()
                if st.session_state.user in users:
                    users[st.session_state.user]["monthly_budget"] = budget
                    save_users(users)

        with col2:
            current_month_total = df[df['Date'].dt.month == datetime.now().month]['Amount'].sum()
            progress = min(100, (current_month_total / budget * 100) if budget > 0 else 0)
            st.write("")
            st.progress(progress / 100)
            st.write(f"**Spent:** Rs{current_month_total:,.2f} / Rs{budget:,.2f} ({progress:.1f}%)")

            if current_month_total > budget:
                st.error("⚠️ You have exceeded your monthly budget!")
            elif current_month_total > budget * 0.8:
                st.warning("⚠️ You are close to your budget limit!")
            else:
                st.success("✅ You are within budget!")

        # ===== RECENT EXPENSES (Professional Rows) =====
        st.markdown('<div class="section-title"><h3>🕒 Recent Expenses</h3></div>', unsafe_allow_html=True)

        recent = df.sort_values('Date', ascending=False).head(5)
        for _, row in recent.iterrows():
            note = row.get('Note', '') or 'No note'
            st.markdown(f'<div class="expense-row"><div><div class="expense-cat">{row["Category"]}</div><div class="expense-note">{note[:50]}</div></div><div style="text-align:right;"><div class="expense-amt">Rs {row["Amount"]:,.2f}</div><div class="expense-date">{row["Date"].strftime("%b %d, %Y")}</div></div></div>', unsafe_allow_html=True)

    else:
        st.info("📝 No expenses yet. Start by adding your first expense!")
        st.markdown('<div class="metric-card" style="text-align:center; padding:40px;"><div style="font-size:3rem;">📊</div><div style="color:#8a92a6; margin-top:10px;">Your dashboard will appear here once you add expenses</div></div>', unsafe_allow_html=True)

# ==================== ADD EXPENSE PAGE ====================
def add_expense_page():
    st.write("# ➕ Add New Expense")

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("📅 Date", datetime.now())
        category = st.selectbox("📂 Category",
            ["🍔 Food", "🚗 Transport", "🛍️ Shopping", "💡 Bills", "🎮 Entertainment",
             "🏥 Health", "📚 Education", "✈️ Travel", "🏠 Rent", "💼 Other"])

    with col2:
        amount = st.number_input("💰 Amount (Rs)", min_value=0.01, step=0.01, format="%.2f")
        note = st.text_area("📝 Note (Optional)", placeholder="Add any additional details...")

    if st.button("💾 Save Expense", use_container_width=True):
        if amount > 0:
            new_expense = {
                "Date": str(date),
                "Category": category,
                "Amount": amount,
                "Note": note if note else ""
            }
            add_expense(st.session_state.user, new_expense)
            show_notification("Expense added successfully! 🎉", "success")
            st.balloons()
            st.rerun()
        else:
            st.error("Please enter a valid amount!")

# ==================== ANALYTICS PAGE ====================
def analytics_page():
    st.write("# 📈 Smart Analytics")

    df = get_user_expenses_df(st.session_state.user)

    if df.empty:
        st.warning("⚠️ No data available for analytics. Add some expenses first!")
        return

    st.write("**Select Date Range**")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", df['Date'].min().date(), key="analytics_start")
    with col2:
        end_date = st.date_input("End Date", df['Date'].max().date(), key="analytics_end")

    if end_date < start_date:
        st.error("⚠️ End date cannot be earlier than start date! Please select a valid date range.")
        return

    filtered_df = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Expense Distribution**")
        pie_chart = create_pie_chart(filtered_df)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.write("**Category-wise Spending**")
        bar_chart = create_bar_chart(filtered_df)
        if bar_chart:
            st.plotly_chart(bar_chart, use_container_width=True, config={'displayModeBar': False})

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Spending Over Time**")
        line_chart = create_line_chart(filtered_df)
        if line_chart:
            st.plotly_chart(line_chart, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.write("**Monthly Spending Comparison**")
        monthly_chart = create_monthly_chart(filtered_df)
        if monthly_chart:
            st.plotly_chart(monthly_chart, use_container_width=True, config={'displayModeBar': False})

    st.divider()
    st.write("## 🧠 Smart Insights")

    total_spent = filtered_df['Amount'].sum()
    avg_expense = filtered_df['Amount'].mean()
    highest = filtered_df.loc[filtered_df['Amount'].idxmax()]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"💰 **Total Spent:** Rs{total_spent:,.2f}")
    with col2:
        st.info(f"📊 **Average Expense:** Rs{avg_expense:,.2f}")
    with col3:
        st.info(f"🏆 **Highest Expense:** Rs{highest['Amount']:.2f} ({highest['Category']})")

    top_category = filtered_df.groupby('Category')['Amount'].sum().idxmax()
    top_amount = filtered_df.groupby('Category')['Amount'].sum().max()
    st.success(f"🎯 You spend the most on **{top_category}** (Rs{top_amount:,.2f})")

# ==================== PROFILE PAGE ====================
def profile_page():
    st.write("# 👤 My Profile")

    users = load_users()
    user_data = users.get(st.session_state.user, {})
    df = get_user_expenses_df(st.session_state.user)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("## 👤")
        st.write(f"### {st.session_state.user}")
        st.write(f"**Member since:** {user_data.get('created', 'N/A')[:10]}")
        st.write(f"**Total expenses:** {len(df)}")
        st.write(f"**Total spent:** Rs{df['Amount'].sum():,.2f}" if not df.empty else "**Total spent:** Rs0")

    with col2:
        st.write("## 📊 Spending Summary")
        if not df.empty:
            category_sum = df.groupby('Category')['Amount'].sum().reset_index()
            category_sum.columns = ['Category', 'Total Spent (Rs)']
            st.dataframe(category_sum, use_container_width=True)
        else:
            st.write("No expenses recorded yet.")

# ==================== EXPENSE MANAGEMENT PAGE ====================
def expense_management_page():
    st.write("# 📋 Manage Expenses")

    df = get_user_expenses_df(st.session_state.user)

    if df.empty:
        st.warning("No expenses to manage. Add some expenses first!")
        return

    st.write("**Filter Options**")
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Filter by Category", ["All"] + list(df['Category'].unique()), key="filter_category")
    with col2:
        date_range = st.selectbox("Filter by Date Range", ["All Time", "Last 7 Days", "Last 30 Days", "This Month"], key="filter_date")
    with col3:
        sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "Amount (Highest)", "Amount (Lowest)"], key="filter_sort")

    filtered_df = df.copy()
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]
    if date_range == "Last 7 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= datetime.now() - timedelta(days=7)]
    elif date_range == "Last 30 Days":
        filtered_df = filtered_df[filtered_df['Date'] >= datetime.now() - timedelta(days=30)]
    elif date_range == "This Month":
        filtered_df = filtered_df[filtered_df['Date'].dt.month == datetime.now().month]
    if sort_by == "Date (Newest)":
        filtered_df = filtered_df.sort_values('Date', ascending=False)
    elif sort_by == "Date (Oldest)":
        filtered_df = filtered_df.sort_values('Date', ascending=True)
    elif sort_by == "Amount (Highest)":
        filtered_df = filtered_df.sort_values('Amount', ascending=False)
    elif sort_by == "Amount (Lowest)":
        filtered_df = filtered_df.sort_values('Amount', ascending=True)

    st.divider()
    st.write(f"**📝 Expenses ({len(filtered_df)} records)**")

    if not filtered_df.empty:
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 1.5, 2, 1, 1])
        with col1: st.write("**Date**")
        with col2: st.write("**Category**")
        with col3: st.write("**Amount**")
        with col4: st.write("**Note**")
        with col5: st.write("**Edit**")
        with col6: st.write("**Delete**")

        st.divider()

        expenses = load_expenses()
        user_expenses = expenses.get(st.session_state.user, [])

        for idx, row in filtered_df.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([1.5, 2, 1.5, 2, 1, 1])

            with col1:
                st.write(row['Date'].strftime('%Y-%m-%d'))
            with col2:
                st.write(row['Category'])
            with col3:
                st.write(f"Rs {row['Amount']:.2f}")
            with col4:
                st.write(row.get('Note', '')[:25])

            actual_index = None
            row_date_str = str(row['Date'].date())

            for i, exp in enumerate(user_expenses):
                exp_date_str = exp['Date'][:10] if len(exp['Date']) >= 10 else exp['Date']
                if (exp_date_str == row_date_str and
                    abs(exp['Amount'] - row['Amount']) < 0.01 and
                    exp['Category'] == row['Category']):
                    actual_index = i
                    break

            with col5:
                if st.button("✏️ ", key=f"edit_btn_{idx}_{row['Date']}_{row['Amount']}"):
                    for i, exp in enumerate(user_expenses):
                        exp_date_str = exp['Date'][:10] if len(exp['Date']) >= 10 else exp['Date']
                        if (exp_date_str == str(row['Date'].date()) and
                            abs(exp['Amount'] - row['Amount']) < 0.01 and
                            exp['Category'] == row['Category']):
                            st.session_state.edit_mode = True
                            st.session_state.edit_index = i
                            st.session_state.edit_data = exp.copy()
                            st.rerun()
                            break

            with col6:
                if st.button("🗑️", key=f"delete_btn_{idx}_{row['Date']}_{row['Amount']}"):
                    for i, exp in enumerate(user_expenses):
                        exp_date_str = exp['Date'][:10] if len(exp['Date']) >= 10 else exp['Date']
                        if (exp_date_str == str(row['Date'].date()) and
                            abs(exp['Amount'] - row['Amount']) < 0.01 and
                            exp['Category'] == row['Category']):
                            if delete_expense(st.session_state.user, i):
                                show_notification("Expense deleted successfully!", "success")
                                st.rerun()
                            break

    st.divider()
    st.write("**📥 Export Data**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Export to CSV", use_container_width=True, key="export_csv"):
            csv_link = export_to_csv(filtered_df)
            st.markdown(csv_link, unsafe_allow_html=True)
    with col2:
        if st.button("📈 Export to Excel", use_container_width=True, key="export_excel"):
            excel_link = export_to_excel(filtered_df)
            st.markdown(excel_link, unsafe_allow_html=True)

    if st.session_state.edit_mode and st.session_state.edit_data:
        st.divider()
        st.write("## ✏️ Edit Expense")
        data = st.session_state.edit_data

        col1, col2 = st.columns(2)

        with col1:
            try:
                date_val = pd.to_datetime(data['Date'])
            except:
                date_val = datetime.now()
            new_date = st.date_input("Date", date_val, key="edit_date_field")

            categories = [
                "🍔 Food", "🚗 Transport", "🛍️ Shopping", "💡 Bills",
                "🎮 Entertainment", "🏥 Health", "📚 Education",
                "✈️ Travel", "🏠 Rent", "💼 Other"
            ]
            current_category = data.get('Category', '🍔 Food')
            cat_index = categories.index(current_category) if current_category in categories else 0
            new_category = st.selectbox("Category", categories, index=cat_index, key="edit_category_field")

        with col2:
            new_amount = st.number_input(
                "Amount (Rs)", min_value=0.01,
                value=float(data['Amount']), step=0.01,
                format="%.2f", key="edit_amount_field"
            )
            new_note = st.text_area("Note", data.get('Note', ''), height=100, key="edit_note_field")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Save Changes", use_container_width=True, key="save_changes_field"):
                updated_expense = {
                    "Date": str(new_date),
                    "Category": new_category,
                    "Amount": new_amount,
                    "Note": new_note
                }
                if edit_expense(st.session_state.user, st.session_state.edit_index, updated_expense):
                    show_notification("Expense updated successfully!", "success")
                    st.session_state.edit_mode = False
                    st.session_state.edit_index = None
                    st.session_state.edit_data = None
                    st.rerun()

        with col2:
            if st.button("❌ Cancel", use_container_width=True, key="cancel_edit_field"):
                st.session_state.edit_mode = False
                st.session_state.edit_index = None
                st.session_state.edit_data = None
                st.rerun()

# ==================== MAIN APP ====================
def main():
    if st.session_state.user is None:
        show_header()

    if st.session_state.notification:
        msg = st.session_state.notification['msg']
        if st.session_state.notification['type'] == "success":
            st.success(msg)
        else:
            st.error(msg)
        st.session_state.notification = None

    if st.session_state.user is None:
        if st.session_state.show_auth:
            auth_page()
        else:
            home_page()
    else:
        with st.sidebar:
            st.write("💸 **Smart Tracker**")
            st.write(f"Welcome, **{st.session_state.user}**")
            st.divider()

            page = st.radio("Navigation",
                ["📊 Dashboard", "➕ Add Expense", "📋 Manage Expenses", "📈 Analytics", "👤 Profile", "🚪 Logout"],
                label_visibility="collapsed")

            st.divider()
            df = get_user_expenses_df(st.session_state.user)
            if not df.empty:
                st.metric("💰 Total Spent", f"Rs{df['Amount'].sum():,.2f}")

        if page == "📊 Dashboard":
            dashboard_page()
        elif page == "➕ Add Expense":
            add_expense_page()
        elif page == "📋 Manage Expenses":
            expense_management_page()
        elif page == "📈 Analytics":
            analytics_page()
        elif page == "👤 Profile":
            profile_page()
        elif page == "🚪 Logout":
            st.session_state.user = None
            st.session_state.show_auth = False
            st.session_state.edit_mode = False
            st.session_state.edit_index = None
            st.session_state.edit_data = None
            show_notification("Logged out successfully!", "success")
            st.rerun()

    if st.session_state.user is None:
        show_footer()

if __name__ == "__main__":
    main()