from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Executive Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Executive Sales Dashboard")
st.caption(
    "Explore sales performance by date, region, product category, and customer segment. "
    "This demonstration uses synthetic educational data."
)

# -----------------------------
# Load the dataset
# -----------------------------
DATA_PATH = Path(__file__).parent / "data" / "retail_sales.csv"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["Order_Date"])
    # Basic validation and preparation
    data = data.drop_duplicates(subset=["Order_ID"])
    data = data.dropna(subset=["Order_Date", "Sales", "Profit", "Region", "Category"])
    data["Month"] = data["Order_Date"].dt.to_period("M").dt.to_timestamp()
    return data


df = load_data(DATA_PATH)

if df.empty:
    st.error("The dataset is empty. Check data/retail_sales.csv.")
    st.stop()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Dashboard filters")

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()
selected_dates = st.sidebar.date_input(
    "Order date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

regions = sorted(df["Region"].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Region", regions, default=regions
)

categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Product category", categories, default=categories
)

segments = sorted(df["Segment"].dropna().unique())
selected_segments = st.sidebar.multiselect(
    "Customer segment", segments, default=segments
)

channels = sorted(df["Sales_Channel"].dropna().unique())
selected_channels = st.sidebar.multiselect(
    "Sales channel", channels, default=channels
)

# Handle a date range that may be temporarily incomplete while selecting
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    date_start, date_end = selected_dates
else:
    date_start, date_end = min_date, max_date

filtered = df[
    df["Order_Date"].dt.date.between(date_start, date_end)
    & df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Segment"].isin(selected_segments)
    & df["Sales_Channel"].isin(selected_channels)
].copy()

if filtered.empty:
    st.warning("No records match these filters. Select more options in the sidebar.")
    st.stop()

# -----------------------------
# KPI calculations
# -----------------------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
order_count = filtered["Order_ID"].nunique()
units_sold = int(filtered["Quantity"].sum())
average_order_value = total_sales / order_count if order_count else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

st.subheader("Key performance indicators")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total sales", f"${total_sales:,.0f}")
k2.metric("Total profit", f"${total_profit:,.0f}")
k3.metric("Orders", f"{order_count:,}")
k4.metric("Units sold", f"{units_sold:,}")
k5.metric("Profit margin", f"{profit_margin:.1f}%")

st.caption(
    f"Average order value: ${average_order_value:,.2f}  •  "
    f"Showing {len(filtered):,} order records after filters"
)

# -----------------------------
# Charts: trends and comparisons
# -----------------------------
st.subheader("Sales trends")
monthly = (
    filtered.groupby("Month", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Month")
)
left, right = st.columns(2)

with left:
    fig_trend = px.line(
        monthly,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly sales",
        labels={"Month": "Month", "Sales": "Sales (USD)"},
        template="plotly_white",
    )
    fig_trend.update_layout(margin=dict(l=10, r=10, t=55, b=10), hovermode="x unified")
    fig_trend.update_yaxes(tickprefix="$", tickformat=",.0f", gridcolor="#E9EDF2")
    st.plotly_chart(fig_trend, use_container_width=True)

with right:
    fig_profit = px.line(
        monthly,
        x="Month",
        y="Profit",
        markers=True,
        title="Monthly profit",
        labels={"Month": "Month", "Profit": "Profit (USD)"},
        template="plotly_white",
    )
    fig_profit.update_layout(margin=dict(l=10, r=10, t=55, b=10), hovermode="x unified")
    fig_profit.update_yaxes(tickprefix="$", tickformat=",.0f", gridcolor="#E9EDF2")
    st.plotly_chart(fig_profit, use_container_width=True)

st.subheader("Performance breakdown")
left, right = st.columns(2)

category_summary = (
    filtered.groupby("Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order_ID", "nunique"))
    .sort_values("Sales", ascending=True)
)
region_summary = (
    filtered.groupby("Region", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order_ID", "nunique"))
    .sort_values("Sales", ascending=True)
)

with left:
    fig_category = px.bar(
        category_summary,
        x="Sales",
        y="Category",
        orientation="h",
        title="Sales by product category",
        labels={"Sales": "Sales (USD)", "Category": "Category"},
        text_auto=".2s",
        template="plotly_white",
    )
    fig_category.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    fig_category.update_xaxes(tickprefix="$", tickformat=",.0f", gridcolor="#E9EDF2")
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    fig_region = px.bar(
        region_summary,
        x="Sales",
        y="Region",
        orientation="h",
        title="Sales by region",
        labels={"Sales": "Sales (USD)", "Region": "Region"},
        text_auto=".2s",
        template="plotly_white",
    )
    fig_region.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    fig_region.update_xaxes(tickprefix="$", tickformat=",.0f", gridcolor="#E9EDF2")
    st.plotly_chart(fig_region, use_container_width=True)

# -----------------------------
# Detailed table and download
# -----------------------------
st.subheader("Filtered order details")
st.caption("Use the filters above to narrow this table, then download the matching records.")
display_columns = [
    "Order_ID", "Order_Date", "Region", "Category", "Product",
    "Segment", "Sales_Channel", "Quantity", "Sales", "Profit"
]
st.dataframe(
    filtered[display_columns].sort_values("Order_Date", ascending=False),
    use_container_width=True,
    hide_index=True,
)

csv_data = filtered[display_columns].to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_retail_sales.csv",
    mime="text/csv",
)

with st.expander("About this dashboard and its metrics"):
    st.markdown(
        """
        - **Sales:** unit price × quantity × (1 − discount), in USD.
        - **Profit:** simulated sales less simulated product cost.
        - **Orders:** unique order IDs in the filtered data.
        - **Profit margin:** total profit ÷ total sales.
        - **Average order value:** total sales ÷ unique orders.

        This is a synthetic dataset created for learning and portfolio demonstration.
        It does not represent actual transactions or a real company.
        """
    )

st.divider()
st.caption("Built with Python, Streamlit, Pandas, and Plotly • Educational portfolio project")
