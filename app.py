import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Try importing Plotly for rich charts, fallback to native charts if missing
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Streamlit Pro Starter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main container background & font tweaks */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Gradient Text */
    .hero-title {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.25rem;
        margin-bottom: 0.25rem;
    }
    
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Modern Card Layout */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        color: #F8FAFC;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0.35rem 0;
    }
    
    .metric-delta {
        font-size: 0.825rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    
    .delta-positive {
        color: #10B981;
    }
    
    .delta-negative {
        color: #EF4444;
    }

    /* Pill badge */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 9999px;
        background: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SESSION STATE & SAMPLE DATA GENERATOR
# -----------------------------------------------------------------------------
if "records" not in st.session_state:
    st.session_state.records = []

@st.cache_data
def load_sample_dataset():
    """Generates a realistic sample dataset for analytics & visualization."""
    np.random.seed(42)
    categories = ["SaaS Subscription", "Enterprise License", "Professional Services", "Hardware Add-on"]
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    statuses = ["Completed", "Pending", "Processing", "Refunded"]
    
    start_date = datetime.now() - timedelta(days=90)
    dates = [start_date + timedelta(days=int(x)) for x in np.linspace(0, 90, 200)]
    
    df = pd.DataFrame({
        "Transaction ID": [f"TRX-{1000 + i}" for i in range(200)],
        "Date": dates,
        "Customer": [f"Client {chr(65 + (i % 26))}{i % 10}" for i in range(200)],
        "Category": np.random.choice(categories, size=200, p=[0.45, 0.25, 0.20, 0.10]),
        "Region": np.random.choice(regions, size=200),
        "Revenue": np.random.exponential(scale=1200, size=200).round(2) + 150,
        "Units": np.random.randint(1, 15, size=200),
        "Rating": np.random.choice([3.5, 4.0, 4.5, 5.0], size=200, p=[0.1, 0.2, 0.4, 0.3]),
        "Status": np.random.choice(statuses, size=200, p=[0.75, 0.12, 0.08, 0.05])
    })
    return df

df_master = load_sample_dataset()

# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **App Control Panel**")
    st.markdown("<span class='badge'>v1.0.0 Starter Kit</span>", unsafe_allow_html=True)
    st.write("")
    
    page = st.radio(
        "Navigation",
        options=["📊 Dashboard", "📈 Analytics & Charts", "🔍 Data Explorer", "⚙️ Interactive Form"],
        index=0
    )
    
    st.divider()
    
    st.subheader("Global Filters")
    selected_categories = st.multiselect(
        "Filter by Category",
        options=df_master["Category"].unique(),
        default=df_master["Category"].unique()
    )
    
    selected_regions = st.multiselect(
        "Filter by Region",
        options=df_master["Region"].unique(),
        default=df_master["Region"].unique()
    )
    
    revenue_filter = st.slider(
        "Minimum Revenue ($)",
        min_value=float(df_master["Revenue"].min()),
        max_value=float(df_master["Revenue"].max()),
        value=float(df_master["Revenue"].min()),
        step=50.0
    )
    
    st.divider()
    st.caption("🚀 Built with Streamlit • Customize in `app.py`")

# Apply sidebar filters to dataset
df_filtered = df_master[
    (df_master["Category"].isin(selected_categories)) &
    (df_master["Region"].isin(selected_regions)) &
    (df_master["Revenue"] >= revenue_filter)
]

# -----------------------------------------------------------------------------
# 5. PAGE: DASHBOARD OVERVIEW
# -----------------------------------------------------------------------------
if page == "📊 Dashboard":
    st.markdown('<div class="hero-title">Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Real-time performance metrics and revenue analytics</div>', unsafe_allow_html=True)
    
    # KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = df_filtered["Revenue"].sum()
    total_orders = len(df_filtered)
    avg_order_value = df_filtered["Revenue"].mean() if total_orders > 0 else 0
    avg_rating = df_filtered["Rating"].mean() if total_orders > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Revenue</div>
            <div class="metric-value">${total_revenue:,.2f}</div>
            <div class="metric-delta delta-positive">▲ +14.2% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Transactions</div>
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-delta delta-positive">▲ +8.1% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg. Deal Size</div>
            <div class="metric-value">${avg_order_value:,.2f}</div>
            <div class="metric-delta delta-negative">▼ -2.4% vs last month</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Customer Satisfaction</div>
            <div class="metric-value">{avg_rating:.2f} / 5.0</div>
            <div class="metric-delta delta-positive">★ 94% positive</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Visualizations Row
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.subheader("Revenue Trend Over Time")
        daily_trend = df_filtered.sort_values("Date").groupby("Date")["Revenue"].sum().reset_index()
        
        if PLOTLY_AVAILABLE:
            fig_trend = px.line(
                daily_trend,
                x="Date",
                y="Revenue",
                template="plotly_dark",
                color_discrete_sequence=["#6366F1"]
            )
            fig_trend.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)")
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.line_chart(daily_trend.set_index("Date")["Revenue"])
            
    with chart_col2:
        st.subheader("Revenue by Category")
        cat_data = df_filtered.groupby("Category")["Revenue"].sum().reset_index()
        
        if PLOTLY_AVAILABLE:
            fig_pie = px.donut(
                cat_data,
                values="Revenue",
                names="Category",
                template="plotly_dark",
                hole=0.55,
                color_discrete_sequence=["#6366F1", "#A855F7", "#EC4899", "#3B82F6"]
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.bar_chart(cat_data.set_index("Category")["Revenue"])

    # Recent Transactions Table
    st.write("")
    st.subheader("Recent Transactions")
    st.dataframe(
        df_filtered.sort_values("Date", ascending=False).head(8),
        use_container_width=True,
        hide_index=True
    )

# -----------------------------------------------------------------------------
# 6. PAGE: ANALYTICS & CHARTS
# -----------------------------------------------------------------------------
elif page == "📈 Analytics & Charts":
    st.markdown('<div class="hero-title">Deep Dive Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Multi-dimensional exploration of metrics & distributions</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Regional Revenue Comparison")
        region_df = df_filtered.groupby("Region")["Revenue"].sum().reset_index()
        if PLOTLY_AVAILABLE:
            fig_bar = px.bar(
                region_df,
                x="Region",
                y="Revenue",
                color="Region",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.bar_chart(region_df.set_index("Region"))

    with col_b:
        st.subheader("Deal Size vs Units Sold")
        if PLOTLY_AVAILABLE:
            fig_scatter = px.scatter(
                df_filtered,
                x="Units",
                y="Revenue",
                color="Category",
                size="Rating",
                hover_data=["Customer", "Status"],
                template="plotly_dark"
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.scatter_chart(df_filtered, x="Units", y="Revenue")

    st.write("")
    st.subheader("Transaction Status Breakdown")
    status_df = df_filtered.groupby(["Category", "Status"]).size().reset_index(name="Count")
    if PLOTLY_AVAILABLE:
        fig_status = px.bar(
            status_df,
            x="Category",
            y="Count",
            color="Status",
            barmode="stack",
            template="plotly_dark"
        )
        fig_status.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.dataframe(status_df, use_container_width=True)

# -----------------------------------------------------------------------------
# 7. PAGE: DATA EXPLORER & CSV EXPORT
# -----------------------------------------------------------------------------
elif page == "🔍 Data Explorer":
    st.markdown('<div class="hero-title">Data Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Search, filter, inspect, and export your data</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Filtered Data", "📤 Upload Custom Data"])
    
    with tab1:
        search_query = st.text_input("🔍 Search by Customer Name or ID", "")
        
        display_df = df_filtered.copy()
        if search_query:
            display_df = display_df[
                display_df["Customer"].str.contains(search_query, case=False, na=False) |
                display_df["Transaction ID"].str.contains(search_query, case=False, na=False)
            ]
            
        st.write(f"Showing **{len(display_df)}** records matching active filters.")
        st.dataframe(display_df, use_container_width=True)
        
        # Download buttons
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered Data as CSV",
            data=csv_data,
            file_name=f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    with tab2:
        st.subheader("Analyze Your Own CSV")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            user_df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(user_df)} rows and {len(user_df.columns)} columns!")
            st.dataframe(user_df.head(20), use_container_width=True)
            
            st.write("### Quick Statistics")
            st.write(user_df.describe())

# -----------------------------------------------------------------------------
# 8. PAGE: INTERACTIVE FORM & STATE MANAGEMENT
# -----------------------------------------------------------------------------
elif page == "⚙️ Interactive Form":
    st.markdown('<div class="hero-title">Interactive Input & Submission</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Test forms, validation, and session state persistence</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Add New Transaction")
        with st.form("new_transaction_form", clear_on_submit=True):
            f_customer = st.text_input("Customer Name", placeholder="e.g. Acme Corp")
            f_category = st.selectbox("Product Category", ["SaaS Subscription", "Enterprise License", "Professional Services", "Hardware Add-on"])
            f_region = st.selectbox("Region", ["North America", "Europe", "Asia-Pacific", "Latin America"])
            f_revenue = st.number_input("Revenue ($)", min_value=10.0, max_value=100000.0, value=1500.0, step=100.0)
            f_units = st.slider("Units", min_value=1, max_value=50, value=1)
            f_status = st.selectbox("Status", ["Completed", "Pending", "Processing"])
            
            submitted = st.form_submit_button("Submit Transaction", use_container_width=True)
            
            if submitted:
                if not f_customer.strip():
                    st.error("Please provide a valid customer name.")
                else:
                    new_entry = {
                        "Transaction ID": f"TRX-{2000 + len(st.session_state.records)}",
                        "Date": datetime.now(),
                        "Customer": f_customer,
                        "Category": f_category,
                        "Region": f_region,
                        "Revenue": f_revenue,
                        "Units": f_units,
                        "Rating": 5.0,
                        "Status": f_status
                    }
                    st.session_state.records.append(new_entry)
                    st.toast(f"Transaction for {f_customer} recorded!", icon="✅")
                    st.success(f"Added new record: **{f_customer}** - ${f_revenue:,.2f}")
    
    with col2:
        st.subheader("Live Session Submissions")
        if st.session_state.records:
            recent_sub_df = pd.DataFrame(st.session_state.records)
            st.dataframe(recent_sub_df, use_container_width=True)
            if st.button("🗑️ Clear Session Submissions"):
                st.session_state.records = []
                st.rerun()
        else:
            st.info("No new transactions submitted in this session yet. Use the form on the left to add entries.")
