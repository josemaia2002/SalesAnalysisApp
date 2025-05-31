import streamlit as st
import pandas as pd

pd.set_option("display.float_format", "${:,.2f}".format)

sales_data = pd.read_csv('sales_data.csv',
     parse_dates=["order_date"],
     dayfirst=True,
).convert_dtypes(dtype_backend="pyarrow")

st.set_page_config(page_title="Sales Dashboard", layout="wide") 
st.title("📊 Sales Data Analysis Dashboard")
st.markdown("Explore sales performance across regions, product categories, and customer segments.")

st.sidebar.header("Filters")

# Date range selection
min_date = sales_data['order_date'].min().date()
max_date = sales_data['order_date'].max().date()
selected_dates = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region selection
regions = st.sidebar.multiselect(
    "Select Regions",
    options=sales_data['sales_region'].unique(),
    default=sales_data['sales_region'].unique()
)

# Filter data based on date and region
filtered_data = sales_data[
    (sales_data['order_date'].dt.date >= selected_dates[0]) &
    (sales_data['order_date'].dt.date <= selected_dates[1]) &
    (sales_data['sales_region'].isin(regions))

]

st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_data.to_csv(index=False).encode('utf-8'),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)  

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Total Sales by Region", 
    "Highest Sales by Category", 
    "Avg. Sales by Customer", 
    "Max Quantities by State", 
    "Total Sales by Product"
])

with tab1:
    st.subheader("Total sales by order type for each region table")
    pivot1 = filtered_data.pivot_table(values='sale_price', index='sales_region', 
                       columns='order_type', aggfunc='sum', 
                       margins=True, margins_name='Totals')
    st.dataframe(pivot1.style.format("${:,.2f}"))    

    # Total sales by region chart
    st.subheader("Total sales by order type for each region chart")
    sales_by_region = filtered_data.groupby(['sales_region', 'order_type'])['sale_price'].sum().unstack()
    st.bar_chart(sales_by_region, x_label='Sales region', y_label='Sales revenue', stack=False)

with tab2:
    st.subheader("Highest sale price by product category table")
    pivot2 = filtered_data.pivot_table(values='sale_price', index='product_category',
                           columns='sales_region', aggfunc='max')
    st.dataframe(pivot2.style.format("${:,.2f}"))

    # Highest sale price by product category
    st.subheader("Highest sale price by product category table chart")
    max_sale_by_category = filtered_data.groupby(['sales_region', 'product_category'])['sale_price'].max().unstack()
    st.bar_chart(max_sale_by_category, x_label='Sales region', y_label='Sales revenue', stack=False)

with tab3:
    st.subheader("Average sales of the different types of orders placed by each type of customer for each state table")
    pivot3 = filtered_data.pivot_table(values='sale_price', index='customer_state',
                       columns=['customer_type', 'order_type'] ,
                       aggfunc='mean')
    st.dataframe(pivot3.style.format("${:,.2f}"))

    # Average sales of the different types of orders placed by each type of customer for each state chart
    st.subheader("Average sales of the different types of orders placed by each type of customer for each state chart")

    # State selection
    state = st.selectbox(
        "Select a State",
        (sales_data['customer_state'].unique()),
        key="state_selectbox_tab3"
    )

    # Filter data based on state
    avg_sales = filtered_data[
        (filtered_data['customer_state'] == state)
    ]

    avg_sales = avg_sales.groupby(['customer_type', 'order_type'])['sale_price'].mean().unstack()

    st.bar_chart(avg_sales, x_label='Customer Type', y_label='Sales revenue', stack=False)

with tab4:
    st.subheader("Highest quantities of each product category within each type of customer for each state table:")
    pivot4 = filtered_data.pivot_table(values='sale_price', index='customer_state',
                        columns=['product_category', 'customer_type'] ,
                        aggfunc='max', fill_value=0,
                        margins=True, margins_name='Max Quantity')
    st.dataframe(pivot4.style.format("${:,.2f}"))
    
    # Average sales of the different types of orders placed by each type of customer for each state chart
    st.subheader("Highest quantities of each product category within each type of customer for each state chart")

    # State selection
    state = st.selectbox(
        "Select a State",
        (sales_data['customer_state'].unique()),
        key="state_selectbox_tab4"
    )

    # Filter data based on state
    max_sale_by_customer_type = filtered_data[
        (filtered_data['customer_state'] == state)
    ]

    max_sale_by_customer_type = max_sale_by_customer_type.groupby(['customer_type', 'product_category'])['sale_price'].max().unstack()

    st.bar_chart(max_sale_by_customer_type, x_label='Customer Type', y_label='Sales revenue', stack=False)

with tab5:
    st.subheader("Total sales of each different product categories, show details of the different types of orders placed by the different types of customers:")
    pivot5 = filtered_data.pivot_table(values='sale_price',
                        index=['customer_type', 'order_type'],
                        columns='product_category',
                        aggfunc='sum', fill_value=0,
                        margins=True, margins_name='Total')
    st.dataframe(pivot5.style.format("${:,.2f}"))

    # TODO chart