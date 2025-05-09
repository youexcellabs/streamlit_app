import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Analysis Dashboard")


st.title("E-commerce Sales Analysis Dashboard")




def load_data(file_path):
    data = pd.read_csv(file_path)
    data["Date"] = pd.to_datetime(data["Date"],errors="coerce")
    data=data.dropna(subset=["Date"]) #remove rows with invalid date
    return data

data_path = "./supermarket_sales.csv"

data = load_data(data_path)
#st.dataframe(data.head(3))

#sidebars for Filters
st.sidebar.header("Filters")

select_branch = st.sidebar.multiselect("Select Branch",options=data["Branch"].unique(),default=data["Branch"].unique())
select_product = st.sidebar.multiselect("Select product",options=data["Product line"].unique(),default=data["Product line"].unique())
select_customer = st.sidebar.multiselect("Select Customer Type",options=data["Customer type"].unique(),default=data["Customer type"].unique())

# dt=data["Date"].dtype
# st.write(dt)

min_date = data["Date"].min().date()
max_date = data["Date"].max().date()

select_date  = st.sidebar.date_input("Select Date Range", value=(min_date,max_date),min_value=min_date,max_value=max_date)

filtered_data = data[
    (data["Branch"].isin(select_branch)) & 
    (data["Product line"].isin(select_product)) & 
    (data["Customer type"].isin(select_customer)) &
    (data["Date"].isin(select_date))
    
    ]

st.dataframe(filtered_data)


filtered_data["Total"] = filtered_data["Total"].round(2)
filtered_data["gross income"] = filtered_data["gross income"].round(2)
filtered_data["Rating"] = filtered_data["Rating"].round(2)
filtered_data["Quantity"] = filtered_data["Quantity"].round(2)




#Streamlit key_Matrics

total_sales = filtered_data["Total"].sum().round(2)
gross_income = filtered_data["gross income"].sum().round(2)
total_quantity = filtered_data["Quantity"].sum().round(2)
avg_rating = filtered_data["Rating"].mean().round(2)


st.subheader("KPI / Key Matrics")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(label="Total Sales", value=f"{total_sales}")

with col2:
    st.metric(label="Gross Income", value=f"{gross_income}")
with col3:
    st.metric(label="Total Quantity", value=f"{total_quantity}")

with col4:
    st.metric(label="Rating", value=f"{avg_rating}")

sales_by_branch = filtered_data.groupby("Branch")["Total"].sum().reset_index()

st.subheader("Total sales by Branch")
fig_branch = px.bar(
    sales_by_branch,
    x="Branch",
    y="Total",
    title="Total Sales By Branch",
    text="Total",
    color="Branch",
    color_discrete_sequence = px.colors.sequential.Teal


)

st.plotly_chart(fig_branch)


#sales by Customer Type

#st.markdown("### sales by Customer Type")

st.subheader("Sales by Customer Type")

sales_by_customer_type = filtered_data.groupby("Customer type")["Total"].sum().reset_index()

fig_customer_sales = px.pie(
    sales_by_customer_type, names="Customer type", values="Total", title="Sales Distribution by Customer Type",
    color="Customer type", color_discrete_sequence = px.colors.sequential.Plasma

)

st.plotly_chart(fig_customer_sales)

##Sales by Payment Method

sales_by_Payment_type = filtered_data.groupby("Payment")["Total"].sum().reset_index()

fig_payment_sales = px.pie(

    sales_by_Payment_type, names="Payment",values="Total",title="Sales by Payment Method",
    color_discrete_sequence = px.colors.sequential.Purples
)

st.plotly_chart(fig_payment_sales)


#sales Trends

sales_trend = filtered_data.groupby("Date")["Total"].sum().reset_index()

fig_sales_trend = px.line(

    sales_trend, x="Date", y="Total", title="Daily Sales Trend",
    color_discrete_sequence = ["#2C3E50"] 
)

st.plotly_chart(fig_sales_trend)

