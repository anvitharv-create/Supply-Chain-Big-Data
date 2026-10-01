import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 80% 0%, rgba(0,100,255,.18), transparent 28%),
        linear-gradient(135deg,#020817 0%,#03162e 55%,#020817 100%);
    color:#e8f2ff;
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#020a1b,#03152d);
    border-right:1px solid #12385f;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color:#9db8d5;
}

[data-testid="stSidebar"] .stButton button {
    width:100%;
    text-align:left;
    background:#061a34;
    border:1px solid #123b63;
    color:#cfe4fa;
    border-radius:8px;
    margin-bottom:5px;
    min-height:36px;
}

[data-testid="stSidebar"] .stButton button:hover {
    background:#075985;
    border-color:#1da1ff;
    color:white;
}

.brand {
    font-size:20px;
    font-weight:800;
    color:white;
}

.brand span {
    color:#2196ff;
}

.brand-sub {
    color:#3caaff;
    font-size:11px;
}

.header {
    background:
        radial-gradient(circle at 75% 10%,rgba(0,120,255,.25),transparent 30%),
        linear-gradient(110deg,#061b38,#020817);
    border:1px solid #164675;
    border-radius:14px;
    padding:18px 22px;
    margin-bottom:14px;
}

.header-title {
    font-size:29px;
    font-weight:800;
}

.header-title span {
    color:#249cff;
}

.header-sub {
    color:#62baff;
    font-size:14px;
    font-weight:600;
    margin-top:2px;
}

.header-info {
    color:#7895b5;
    font-size:10px;
    margin-top:4px;
}

.filter-status {
    display:inline-block;
    background:#082b4d;
    border:1px solid #12639a;
    color:#4db8ff;
    border-radius:20px;
    padding:5px 12px;
    font-size:11px;
    font-weight:700;
    margin-top:9px;
}

.kpi {
    background:linear-gradient(145deg,#082443,#041327);
    border:1px solid #164b7d;
    border-radius:12px;
    padding:14px 16px;
    min-height:105px;
    box-shadow:0 0 18px rgba(0,130,255,.07);
}

.kpi-title {
    color:#829ab5;
    font-size:10px;
    font-weight:700;
}

.kpi-value {
    color:#f5f9ff;
    font-size:22px;
    font-weight:800;
    margin-top:5px;
}

.kpi-info {
    color:#4f769b;
    font-size:9px;
    margin-top:5px;
}

.section {
    background:linear-gradient(145deg,#061b35,#041126);
    border:1px solid #123b64;
    border-radius:12px;
    padding:11px 15px;
    margin-top:15px;
    margin-bottom:8px;
}

.section-title {
    color:#eaf4ff;
    font-size:16px;
    font-weight:800;
}

.section-sub {
    color:#6482a4;
    font-size:10px;
    margin-top:2px;
}

[data-testid="stMetric"] {
    background:#061b35;
    border:1px solid #143e66;
    border-radius:10px;
    padding:10px;
}

[data-testid="stMetricLabel"] {
    color:#7995b3;
}

[data-testid="stMetricValue"] {
    color:#f4f8ff;
}

.footer {
    text-align:center;
    color:#466987;
    font-size:10px;
    padding:25px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    data = pd.read_parquet("data/processed/supply_chain_processed")
    data["Date"] = pd.to_datetime(data["Date"])
    return data


df = load_data()


def money(value):
    return f"₹{value:,.2f}"


def chart_layout(fig, title):
    fig.update_layout(
        title={
            "text": title,
            "font": {
                "size": 15,
                "color": "#edf6ff"
            }
        },
        paper_bgcolor="#061a32",
        plot_bgcolor="#061a32",
        font={
            "color": "#c5d8ec"
        },
        margin={
            "l":45,
            "r":20,
            "t":55,
            "b":45
        },
        legend={
            "bgcolor":"rgba(0,0,0,0)",
            "font":{
                "color":"#bcd1e7",
                "size":9
            }
        },
        xaxis={
            "gridcolor":"rgba(120,150,180,.12)",
            "zerolinecolor":"rgba(120,150,180,.15)"
        },
        yaxis={
            "gridcolor":"rgba(120,150,180,.12)",
            "zerolinecolor":"rgba(120,150,180,.15)"
        }
    )
    return fig


def section(title, subtitle):
    st.markdown(
        f'<div class="section"><div class="section-title">{title}</div><div class="section-sub">{subtitle}</div></div>',
        unsafe_allow_html=True
    )


def show_header(title, subtitle, filter_text, record_count):
    st.markdown(
        f'<div class="header"><div class="header-title">{title}</div><div class="header-sub">{subtitle}</div><div class="header-info">Actual processed supply chain data</div><div class="filter-status">Showing: {filter_text} • {record_count:,} records</div></div>',
        unsafe_allow_html=True
    )


def show_kpis(data, prefix="TOTAL"):
    total_units = data["Units_Sold"].sum()
    total_revenue = data["Revenue"].sum()
    total_profit = data["Profit"].sum()
    reorder_required = (
        data["Reorder_Status"] == "REORDER_REQUIRED"
    ).sum()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f'<div class="kpi"><div class="kpi-title">{prefix} UNITS SOLD</div><div class="kpi-value" style="color:#38bdf8">{total_units:,.0f}</div><div class="kpi-info">{len(data):,} filtered records</div></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'<div class="kpi"><div class="kpi-title">{prefix} REVENUE</div><div class="kpi-value" style="color:#c084fc">{money(total_revenue)}</div><div class="kpi-info">Actual calculated revenue</div></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f'<div class="kpi"><div class="kpi-title">{prefix} PROFIT</div><div class="kpi-value" style="color:#22d3a3">{money(total_profit)}</div><div class="kpi-info">Revenue minus total cost</div></div>',
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f'<div class="kpi"><div class="kpi-title">{prefix} REORDER</div><div class="kpi-value" style="color:#fb7185">{reorder_required:,.0f}</div><div class="kpi-info">Actual reorder records</div></div>',
            unsafe_allow_html=True
        )


def chart_title(title, active_filter_text):
    return f"{title} — {active_filter_text}"


if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "filter_reset" not in st.session_state:
    st.session_state.filter_reset = 0


period_options = [
    "All Periods",
    "Last 7 Days",
    "Last 20 Days",
    "Last 30 Days",
    "Last 60 Days",
    "Last 90 Days",
    "Custom Days"
]


with st.sidebar:

    st.markdown(
        '<div class="brand">📦 SUPPLY <span>CHAIN</span></div><div class="brand-sub">Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ANALYTICS")

    if st.button("🏠  Dashboard", width="stretch"):
        st.session_state.page = "Dashboard"
        st.rerun()

    if st.button("▥  Regional Analysis", width="stretch"):
        st.session_state.page = "Regional Analysis"
        st.rerun()

    if st.button("⬡  Product Analysis", width="stretch"):
        st.session_state.page = "Product Analysis"
        st.rerun()

    if st.button("⌂  Warehouse Analysis", width="stretch"):
        st.session_state.page = "Warehouse Analysis"
        st.rerun()

    if st.button("♟  Supplier Analysis", width="stretch"):
        st.session_state.page = "Supplier Analysis"
        st.rerun()

    if st.button("⚠  Reorder Analysis", width="stretch"):
        st.session_state.page = "Reorder Analysis"
        st.rerun()

    st.divider()

    st.markdown("### TOOLS")

    if st.button("▤  Data Explorer", width="stretch"):
        st.session_state.page = "Data Explorer"
        st.rerun()

    st.divider()

    st.markdown("### FILTERS")

    filter_key = st.session_state.filter_reset

    period = st.selectbox(
        "Time Period",
        period_options,
        index=0,
        key=f"period_filter_{filter_key}"
    )

    custom_days = 33

    if period == "Custom Days":
        custom_days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=3650,
            value=33,
            step=1,
            key=f"custom_days_{filter_key}"
        )

        st.caption(
            f"Showing actual last {custom_days} days from the dataset"
        )

    region_options = [
        "All Regions"
    ] + sorted(
        df["Region"].dropna().unique().tolist()
    )

    region = st.selectbox(
        "Region",
        region_options,
        index=0,
        key=f"region_filter_{filter_key}"
    )

    product_options = [
        "All Products"
    ] + sorted(
        df["SKU_ID"].dropna().unique().tolist()
    )

    product = st.selectbox(
        "Product / SKU",
        product_options,
        index=0,
        key=f"product_filter_{filter_key}"
    )

    warehouse_options = [
        "All Warehouses"
    ] + sorted(
        df["Warehouse_ID"].dropna().unique().tolist()
    )

    warehouse = st.selectbox(
        "Warehouse",
        warehouse_options,
        index=0,
        key=f"warehouse_filter_{filter_key}"
    )

    supplier_options = [
        "All Suppliers"
    ] + sorted(
        df["Supplier_ID"].dropna().unique().tolist()
    )

    supplier = st.selectbox(
        "Supplier",
        supplier_options,
        index=0,
        key=f"supplier_filter_{filter_key}"
    )

    if st.button("⟳  Clear Filters", width="stretch"):
        st.session_state.filter_reset += 1
        st.rerun()

    st.divider()

    st.info(
        "⚡ Powered by Apache Spark\n\nBig Data Analytics"
    )


data = df.copy()


if period == "All Periods":

    period_label = "All Periods"

elif period == "Custom Days":

    days = int(custom_days)

    latest_date = df["Date"].max()

    start_date = latest_date - timedelta(
        days=days - 1
    )

    data = data[
        data["Date"] >= start_date
    ]

    period_label = f"Last {days} Days"

elif period.startswith("Last"):

    days = int(
        period.split()[1]
    )

    latest_date = df["Date"].max()

    start_date = latest_date - timedelta(
        days=days - 1
    )

    data = data[
        data["Date"] >= start_date
    ]

    period_label = f"Last {days} Days"

else:

    selected_year = int(period)

    data = data[
        data["Date"].dt.year == selected_year
    ]

    period_label = f"Year {selected_year}"


if region != "All Regions":
    data = data[
        data["Region"] == region
    ]


if product != "All Products":
    data = data[
        data["SKU_ID"] == product
    ]


if warehouse != "All Warehouses":
    data = data[
        data["Warehouse_ID"] == warehouse
    ]


if supplier != "All Suppliers":
    data = data[
        data["Supplier_ID"] == supplier
    ]


if data.empty:
    st.error(
        "No records match the selected filters."
    )
    st.stop()


filter_parts = []


if period_label != "All Periods":
    filter_parts.append(period_label)


if region != "All Regions":
    filter_parts.append(region)


if product != "All Products":
    filter_parts.append(product)


if warehouse != "All Warehouses":
    filter_parts.append(warehouse)


if supplier != "All Suppliers":
    filter_parts.append(supplier)


if filter_parts:
    active_filter_text = " • ".join(
        filter_parts
    )
else:
    active_filter_text = "Complete Dataset"


if st.session_state.page == "Dashboard":

    show_header(
        "Supply Chain and <span>Inventory Analysis</span>",
        "Big Data Analytics Dashboard",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "OVERALL"
    )

    section(
        "🌍 Regional Performance",
        f"Actual regional performance • {active_filter_text}"
    )

    regional = data.groupby(
        "Region"
    ).agg(
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Units=("Units_Sold", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            regional,
            x="Region",
            y="Revenue",
            color="Region",
            color_discrete_sequence=[
                "#2196ff",
                "#00bcd4",
                "#22c55e",
                "#a855f7"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.2f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Revenue by Region",
                active_filter_text
            )
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        fig = px.pie(
            regional,
            names="Region",
            values="Profit",
            hole=.55,
            color_discrete_sequence=[
                "#22c55e",
                "#ef4444",
                "#38bdf8",
                "#a855f7"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Profit: ₹%{value:,.2f}<br>Share: %{percent}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Profit Distribution",
                active_filter_text
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


    section(
        "🏢 Warehouse Performance",
        f"Actual warehouse performance • {active_filter_text}"
    )

    warehouse_data = data.groupby(
        "Warehouse_ID"
    ).agg(
        Units=("Units_Sold", "sum"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            warehouse_data,
            x="Warehouse_ID",
            y="Units",
            color="Warehouse_ID",
            color_discrete_sequence=[
                "#06b6d4",
                "#3b82f6",
                "#8b5cf6",
                "#ec4899",
                "#f59e0b"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Units Sold: %{y:,.0f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Units Sold by Warehouse",
                active_filter_text
            )
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        fig = px.line(
            warehouse_data,
            x="Warehouse_ID",
            y="Revenue",
            markers=True
        )

        fig.update_traces(
            line=dict(
                color="#f59e0b",
                width=3
            ),
            marker=dict(
                size=9,
                color="#fbbf24"
            ),
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.2f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Revenue by Warehouse",
                active_filter_text
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


elif st.session_state.page == "Regional Analysis":

    show_header(
        "🌍 Regional <span>Analysis</span>",
        "Regional sales, revenue and profitability",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "REGIONAL"
    )

    regional = data.groupby(
        "Region"
    ).agg(
        Units=("Units_Sold", "sum"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Inventory=("Inventory_Level", "mean")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            regional,
            x="Region",
            y="Revenue",
            color="Region",
            color_discrete_sequence=[
                "#2196ff",
                "#00bcd4",
                "#22c55e",
                "#a855f7"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.2f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Revenue by Region",
                active_filter_text
            )
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        fig = px.pie(
            regional,
            names="Region",
            values="Profit",
            hole=.55,
            color_discrete_sequence=[
                "#22c55e",
                "#ef4444",
                "#38bdf8",
                "#a855f7"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Profit: ₹%{value:,.2f}<br>Percentage: %{percent}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Profit Distribution",
                active_filter_text
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.dataframe(
        regional,
        width="stretch",
        hide_index=True
    )


elif st.session_state.page == "Product Analysis":

    show_header(
        "📦 Product <span>Analysis</span>",
        "Actual product revenue, sales and inventory",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "PRODUCT"
    )

    products = data.groupby(
        "SKU_ID"
    ).agg(
        Units=("Units_Sold", "sum"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Inventory=("Inventory_Level", "mean"),
        Stockouts=("Stockout_Flag", "sum")
    ).reset_index()

    top_products = products.nlargest(
        10,
        "Revenue"
    ).sort_values(
        "Revenue"
    )

    fig = px.bar(
        top_products,
        x="Revenue",
        y="SKU_ID",
        orientation="h",
        color="SKU_ID",
        color_discrete_sequence=[
            "#2563eb",
            "#3b82f6",
            "#06b6d4",
            "#14b8a6",
            "#22c55e",
            "#84cc16",
            "#a3e635",
            "#facc15",
            "#f97316",
            "#ef4444"
        ]
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.2f}<br>Period: "
        + active_filter_text +
        "<extra></extra>"
    )

    fig = chart_layout(
        fig,
        chart_title(
            "Top 10 Products by Revenue",
            active_filter_text
        )
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.dataframe(
        products.sort_values(
            "Revenue",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )


elif st.session_state.page == "Warehouse Analysis":

    show_header(
        "🏢 Warehouse <span>Analysis</span>",
        "Actual warehouse sales, inventory and revenue",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "WAREHOUSE"
    )

    warehouse_data = data.groupby(
        "Warehouse_ID"
    ).agg(
        Units=("Units_Sold", "sum"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Inventory=("Inventory_Level", "mean"),
        Inventory_Value=("Inventory_Value", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            warehouse_data,
            x="Warehouse_ID",
            y="Units",
            color="Warehouse_ID",
            color_discrete_sequence=[
                "#06b6d4",
                "#3b82f6",
                "#8b5cf6",
                "#ec4899",
                "#f59e0b"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Units Sold: %{y:,.0f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Units Sold by Warehouse",
                active_filter_text
            )
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        fig = px.bar(
            warehouse_data,
            x="Warehouse_ID",
            y="Revenue",
            color="Warehouse_ID",
            color_discrete_sequence=[
                "#f59e0b",
                "#ef4444",
                "#ec4899",
                "#a855f7",
                "#3b82f6"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.2f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Revenue by Warehouse",
                active_filter_text
            )
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.dataframe(
        warehouse_data,
        width="stretch",
        hide_index=True
    )


elif st.session_state.page == "Supplier Analysis":

    show_header(
        "👥 Supplier <span>Analysis</span>",
        "Actual supplier lead time, orders and profit",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "SUPPLIER"
    )

    supplier_data = data.groupby(
        "Supplier_ID"
    ).agg(
        Lead_Time=("Supplier_Lead_Time_Days", "mean"),
        Orders=("Order_Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum")
    ).reset_index()

    c1, c2 = st.columns(2)

    with c1:

        fig = px.scatter(
            supplier_data,
            x="Lead_Time",
            y="Orders",
            size="Profit",
            color="Supplier_ID",
            color_discrete_sequence=[
                "#38bdf8",
                "#818cf8",
                "#c084fc",
                "#f472b6",
                "#fb7185",
                "#f59e0b",
                "#facc15",
                "#4ade80",
                "#2dd4bf",
                "#22d3ee"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{fullData.name}</b><br>Lead Time: %{x:.2f} days<br>Order Quantity: %{y:,.0f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Supplier Lead Time vs Order Quantity",
                active_filter_text
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        top_supplier = supplier_data.nlargest(
            7,
            "Profit"
        ).sort_values(
            "Profit"
        )

        fig = px.bar(
            top_supplier,
            x="Profit",
            y="Supplier_ID",
            orientation="h",
            color="Supplier_ID",
            color_discrete_sequence=[
                "#facc15",
                "#fb923c",
                "#f97316",
                "#ef4444",
                "#ec4899",
                "#c084fc",
                "#818cf8"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Profit: ₹%{x:,.2f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Top Suppliers by Profit",
                active_filter_text
            )
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.dataframe(
        supplier_data,
        width="stretch",
        hide_index=True
    )


elif st.session_state.page == "Reorder Analysis":

    show_header(
        "⚠️ Reorder <span>Analysis</span>",
        "Actual inventory status and reorder requirements",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "INVENTORY"
    )

    reorder_data = data[
        "Reorder_Status"
    ].value_counts().reset_index()

    reorder_data.columns = [
        "Status",
        "Count"
    ]

    reorder_data["Display"] = reorder_data[
        "Status"
    ].replace(
        {
            "REORDER_REQUIRED": "Reorder Required",
            "STOCK_SUFFICIENT": "Stock Sufficient"
        }
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = px.pie(
            reorder_data,
            names="Display",
            values="Count",
            hole=.58,
            color_discrete_sequence=[
                "#ef4444",
                "#22c55e"
            ]
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Records: %{value:,.0f}<br>Percentage: %{percent}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Reorder Status",
                active_filter_text
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with c2:

        fig = px.histogram(
            data,
            x="Inventory_Level",
            nbins=30
        )

        fig.update_traces(
            marker=dict(
                color="#38bdf8"
            ),
            hovertemplate="Inventory Level: %{x:,.0f}<br>Records: %{y:,.0f}<br>Period: "
            + active_filter_text +
            "<extra></extra>"
        )

        fig = chart_layout(
            fig,
            chart_title(
                "Inventory Level Distribution",
                active_filter_text
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    reorder_table = data.groupby(
        "Reorder_Status"
    ).agg(
        Records=("SKU_ID", "count"),
        Average_Inventory=("Inventory_Level", "mean"),
        Average_Demand_Forecast=("Demand_Forecast", "mean")
    ).reset_index()

    st.dataframe(
        reorder_table,
        width="stretch",
        hide_index=True
    )


elif st.session_state.page == "Data Explorer":

    show_header(
        "▤ Data <span>Explorer</span>",
        "Explore the actual processed supply chain dataset",
        active_filter_text,
        len(data)
    )

    show_kpis(
        data,
        "FILTERED"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Records",
            f"{len(data):,}"
        )

    with c2:
        st.metric(
            "Columns",
            f"{len(data.columns)}"
        )

    with c3:
        st.metric(
            "Products",
            f"{data['SKU_ID'].nunique():,}"
        )

    with c4:
        st.metric(
            "Warehouses",
            f"{data['Warehouse_ID'].nunique():,}"
        )

    st.dataframe(
        data,
        width="stretch",
        height=550,
        hide_index=True
    )

    csv = data.to_csv(
        index=False
    )

    st.download_button(
        "⬇ Download Filtered Dataset",
        csv,
        "supply_chain_filtered.csv",
        "text/csv",
        width="stretch"
    )


st.markdown(
    f'<div class="footer">Supply Chain and Inventory Analysis • Apache Spark • Python • Streamlit • {len(data):,} actual records • {active_filter_text}</div>',
    unsafe_allow_html=True
)