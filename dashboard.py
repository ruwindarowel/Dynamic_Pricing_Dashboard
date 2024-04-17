import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import warnings
import altair as alt




st.set_page_config(page_title="Dynamic Pricing", page_icon=":chart_with_upwards_trend:",layout="wide")
st.title(":chart_with_upwards_trend: Dynamic Pricing")
st.markdown("<style>div.block-container{padding-top:1rem}</style>",unsafe_allow_html=True)

df = pd.read_csv("dynamic.csv")

average_values = df[["Expected_Ride_Duration","adjusted_ride_cost","profit_percentage","Number_of_Riders","Number_of_Drivers"]].mean()
print(average_values)


col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(label= "Avg No.of Drivers :taxi:", value= "28", delta=3)
col2.metric(label= "Avg No.of Riders 	:raising_hand:", value= "61", delta="-2")
col3.metric(label= "Avg Expected Ride Duration :clock330:", value= "1 Hour 40 Min", delta="5")
col4.metric(label= "Avg Profit Percentage :moneybag:", value= "83%", delta="3")
col5.metric(label= "Avg Adjusted Cost :heavy_dollar_sign:", value= "$ 681", delta="-2")

# Expected_Ride_Duration,adjusted_ride_cost,profit_percentage
#st.line_chart(data=df, x="Expected_Ride_Duration", y="adjusted_ride_cost")

# Column names:  Location_Category,Customer_Loyalty_Status,Time_of_Booking,Vehicle_Type


st.sidebar.header("Choose Your Filter: ")

#vehicle type
vehicle_type = st.sidebar.multiselect("Vehicle Type: ", df["Vehicle_Type"].unique())
if not vehicle_type:
    df2 = df.copy()
else:
    df2 = df[df["Vehicle_Type"].isin(vehicle_type)]

#Time of booking
time = st.sidebar.selectbox("Time of Booking: ", df2["Time_of_Booking"].unique())
if not time:
    df3 = df2.copy()
else:
    df3 = df2[df2["Time_of_Booking"].isin([time])] 

#location
location = st.sidebar.selectbox("Location Category: ",df3["Location_Category"].unique())




# filter the data based on vehicle type, time & location
if not vehicle_type and not time and not location:
    filtered_df = df
elif not time and not location:
    filtered_df = df[df["Vehicle_Type"].isin(vehicle_type)]
elif not vehicle_type and not location:
    filtered_df = df[df["Time_of_Booking"].isin([time])]
elif time and location:
    filtered_df = df3[df["Time_of_Booking"].isin([time]) & df3["Location_Category"].isin([location])]
elif vehicle_type and location:
    filtered_df = df3[df["Vehicle_Type"].isin(vehicle_type) & df3["Location_Category"].isin([location])]
elif vehicle_type and time:
    filtered_df = df3[df["Vehicle_Type"].isin(vehicle_type) & df3["Time_of_Booking"].isin([time])]
elif location:
    filtered_df = df3[df3["Location_Category"].isin([location])]
else:
    filtered_df = df3[df3["Vehicle_Type"].isin(vehicle_type) & df3["Time_of_Booking"].isin(time) & df3["Location_Category"].isin(location)]





#Expected ride duration vs adjusted cost & profit% with vehicle type 

col1, col2 = st.columns(2)

chart1 = alt.Chart(filtered_df).mark_circle().encode(
    x="Expected_Ride_Duration",
    y="adjusted_ride_cost",
    color="Vehicle_Type", 
).interactive()

chart2 = alt.Chart(filtered_df).mark_circle().encode(
    x="Expected_Ride_Duration",
    y="profit_percentage",
    color="Vehicle_Type", 
    
).interactive()



with col1:
    st.subheader("Adjusted Cost")
    st.altair_chart(chart1, theme=None, use_container_width=True )


with col2:
    st.subheader("Profit Percentage")
    st.altair_chart(chart2, theme=None, use_container_width=True )


# No.of drivers Vs adjusted cost & profit%   ||||  No.of Riders Vs adjusted cost & profit%  


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### Adjusted cost & Profit percentage with No.of Drivers")
    st.line_chart(
        data=filtered_df,
        x="Number_of_Drivers",
        y=["profit_percentage", "adjusted_ride_cost"],
        color= ["#f25a2c","#2ccbf2"]
    )


    
with col2:
    st.markdown(" <h5 style='text-align: center;'> Loyalty Status wise Profit percentage </h5>", unsafe_allow_html=True)
    fig = px.pie(filtered_df, values = "profit_percentage", names = "Customer_Loyalty_Status", hole = 0.5)
    fig.update_traces(text = filtered_df["Customer_Loyalty_Status"], textposition = "outside")
    fig.update_layout(height=350, width=350)
    st.plotly_chart(fig, use_container_width=True)


with col3:
    st.markdown("##### Adjusted cost & Profit percentage with No.of Riders")
    st.line_chart(
        data=filtered_df,
        x="Number_of_Riders",
        y=["profit_percentage", "adjusted_ride_cost"],
        color= ["#f25a2c","#2ccbf2"]
    )


# """ with col3:
#     fig = go.Figure(data=[go.Pie(labels=filtered_df["Customer_Loyalty_Status"], values=filtered_df["profit_percentage"], hole=.5)])
#     st.plotly_chart(fig,use_container_width=True) """





# Use `hole` to create a donut-like pie chart

