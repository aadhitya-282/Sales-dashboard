import streamlit as st
import pandas as pd
import plotly.express as px
from database import initialize_database,load_sales


st.set_page_config(page_title="Sales Dashboard",page_icon="📊",layout="wide")
initialize_database()
df=load_sales()
st.title("📊 Sales Analysis Dashboard")
st.caption("Monitor sales, products, customers and profitability")
st.sidebar.header("Filters")
categories=st.sidebar.multiselect("Select categories", options=sorted(df["category"].unique()),default=sorted(df["category"].unique()))
regions=st.sidebar.multiselect("Select regions",options=sorted(df["region"].unique()),default=sorted(df["region"].unique()))
date_range=st.sidebar.date_input("Select date range",value=(df["order_date"].min().date(),df["order_date"].max().date()))
filtered=df[df["category"].isin(categories) & df["region"].isin(regions)].copy()
if isinstance(date_range, (tuple,list)) and len(date_range)==2:
    start,end=date_range
    filtered=filtered[filtered["order_date"].dt.date.between(start,end)]
if filtered.empty:
    st.warning("No sales match the selected filters.")
    st.stop()
revenue=filtered["revenue"].sum()
profit=filtered["profit"].sum()
orders=filtered["order_id"].sum()
avg_order=revenue/orders if orders else 0
c1,c2,c3,c4=st.columns(4)
c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Total Profit", f"₹{profit:,.0f}")
c3.metric("Total Orders", f"{orders:,}")
c4.metric("Average Order Value", f"₹{avg_order:,.0f}")
st.divider()
filtered["month"]=(filtered["order_date"].dt.to_period("M").astype(str))
monthly=(filtered.groupby("month",as_index=False)["revenue"].sum().sort_values("month"))
st.subheader("Monthly Sales Trend")
fig=px.line(monthly,x="month",y="revenue",markers=True,title="Revenue by Month")
st.plotly_chart(fig,use_container_width=True)
st.subheader("Revenue by Category")
category_sales=(filtered.groupby("category",as_index=False)["revenue"].sum().sort_values("revenue",ascending=False))
fig=px.bar(category_sales,x="category",y="revenue",color="category",title="Category Performance")
st.plotly_chart(fig,use_container_width=True)
st.subheader("Top 5 products")
top_products=(filtered.groupby("product_name",as_index=False)["revenue"].sum().nlargest(5,"revenue"))
st.dataframe(top_products,use_container_width=True)
st.subheader("Top 5 Customers")
top_customers=(filtered.groupby("customer_name",as_index=False)["revenue"].sum().nlargest(5,"revenue"))
st.dataframe(top_customers,use_container_width=True)
st.subheader("Profit by Category")
profit_data=(filtered.groupby("category",as_index=False)["profit"].sum().sort_values("profit",ascending=False))
fig=px.bar(profit_data,x="category",y="profit",title="Profit Analysis",color="profit")
st.plotly_chart(fig,use_container_width=True)
st.subheader("Sales Records")
st.dataframe(filtered,use_container_width=True)
st.download_button("Download Sales CSV",data=filtered.to_csv(index=False).encode("utf-8"),file_name="sales_report.csv",mime="text/csv")