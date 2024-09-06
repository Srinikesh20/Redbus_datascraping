import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/redbus_data')
query = "SELECT * FROM bus_routes"
data = pd.read_sql(query,engine)

st.title('Redbus KSRTC Routes Data Filtering and Analysis')
busroute_filter = st.multiselect('Select Route:', options= data['route_name'].unique())
bustype_filter = st.multiselect('Select Bus type:', options = data['bustype'].unique())
price_filter = st.slider('Select Price Range:', min_value=int(data['price'].min()), max_value=int(data['price'].max()), value=(int(data['price'].min()), int(data['price'].max())))
star_filter = st.slider('Select Star Rating Range:', min_value=float(data['star_rating'].min()), max_value=float(data['star_rating'].max()), value=(float(data['star_rating'].min()), float(data['star_rating'].max())))
availability_filter = st.slider('Select Seat Availability Range:', min_value=int(data['seats_available'].min()), max_value=int(data['seats_available'].max()), value=(int(data['seats_available'].min()), int(data['seats_available'].max())))
filtered_data = data

if bustype_filter:
    filtered_data = filtered_data[filtered_data['bustype'].isin(bustype_filter)]

if busroute_filter:
    filtered_data = filtered_data[filtered_data['route_name'].isin(busroute_filter)]

filtered_data = filtered_data[(filtered_data['price'] >= price_filter[0]) & (filtered_data['price'] <= price_filter[1])]
filtered_data = filtered_data[(filtered_data['star_rating'] >= star_filter[0]) & (filtered_data['star_rating'] <= star_filter[1])]
filtered_data = filtered_data[(filtered_data['seats_available'] >= availability_filter[0]) & (filtered_data['seats_available'] <= availability_filter[1])]
st.write('Filtered Data:')
st.dataframe(filtered_data)
if not filtered_data.empty:
    st.download_button(
        label="Download Filtered Data",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.warning("No data available with the selected filters.")
