import streamlit as st
import mysql.connector
import pandas as pd
from datetime import time



def fetch_data(query):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="redbus_data"
    )
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    # Get column names
    column_names = [column[0] for column in cursor.description]
    con.close()
    return rows,column_names


with st.sidebar:
    state_transport_corp = st.selectbox('Select the State Transport Corporation:',
    ['Kerala (KSRTC)', 'Kadamba (KTCL)', 'Rajasthan (RSRTC)','Punjab (PEPSU)'])
    
    if state_transport_corp == 'Kerala (KSRTC)':
        route = ['Bangalore to Kozhikode', 'Kozhikode to Ernakulam', 'Kozhikode to Bangalore', 
                 'Ernakulam to Kozhikode', 'Kozhikode to Mysore', 'Kozhikode to Thiruvananthapuram', 
                 'Bangalore to Kalpetta (kerala)', 'Mysore to Kozhikode', 'Kalpetta (kerala) to Bangalore', 
                 'Kozhikode to Thrissur', 'Thiruvananthapuram to Kozhikode', 'Bangalore to Kannur', 
                 'Kozhikode to Kottayam', 'Kannur to Bangalore', 'Kottayam to Kozhikode', 
                 'Thrissur to Kozhikode', 'Kozhikode to Kalpetta (kerala)', 'Coimbatore to Ooty', 
                 'Kalpetta (kerala) to Kozhikode']
    elif state_transport_corp == 'Kadamba (KTCL)':
        route = ['Pune to Goa', 'Goa to Pune', 'Mumbai to Goa', 'Goa to Mumbai', 'Pandharpur to Goa', 
                 'Bangalore to Goa', 'Goa to Pandharpur', 'Belagavi to Goa', 'Goa to Bangalore', 
                 'Solapur to Goa', 'Goa to Kolhapur(Maharashtra)', 'Goa to Solapur', 'Goa to Sangola (Solapur)', 
                 'Sangola (Solapur) to Goa', 'Calangute (goa) to Goa Airport', 'Goa to Sangli', 'Calangute (goa) to Mopa Airport', 
                 'Mopa Airport to Calangute (goa)', 'Ponda to Belagavi', 'Goa to Miraj', 'Goa Airport to Calangute (goa)', 
                 'Marcel to Belagavi', 'Shivamogga to Goa', 'Goa to Mopa Airport', 'Goa to Satara', 'Belagavi to Marcel', 
                 'Mopa Airport to Goa', 'Shirdi to Goa', 'Goa to Shivamogga', 'Goa to Shirdi', 'Goa to Goa Airport', 
                 'Margao to Mopa Airport', 'Goa Airport to Goa', 'Mopa Airport to Margao', 'Belagavi to Saquelim', 
                 'Panaji to Mopa Airport', 'Saquelim to Belagavi', 'Calangute (goa) to Goa', 'Calangute (goa) to Panaji', 
                 'Goa Airport to Panaji']
    elif state_transport_corp == 'Rajasthan (RSRTC)':
        route = ['Jodhpur to Ajmer', 'Beawar (Rajasthan) to Jaipur (Rajasthan)', 'Udaipur to Jodhpur', 
                 'Jaipur (Rajasthan) to Jodhpur', 'Sikar to Jaipur (Rajasthan)', 'Kishangarh to Jaipur (Rajasthan)', 
                 'Aligarh (uttar pradesh) to Jaipur (Rajasthan)', 'Jodhpur to Beawar (Rajasthan)', 'Kota(Rajasthan) to Jaipur (Rajasthan)', 
                 'Jaipur (Rajasthan) to Aligarh (uttar pradesh)', 'Jaipur (Rajasthan) to Kota(Rajasthan)', 
                 'Pali (Rajasthan) to Udaipur', 'Udaipur to Pali (Rajasthan)', 'Sikar to Bikaner', 'Jaipur (Rajasthan) to Bharatpur', 
                 'Kishangarh to Jodhpur', 'Jaipur (Rajasthan) to Bhilwara', 'Kota(Rajasthan) to Udaipur', 'Jaipur (Rajasthan) to Pilani', 
                 'Jaipur (Rajasthan) to Mathura', 'Bikaner to Sikar']
    elif state_transport_corp == 'Punjab (PEPSU)':
         route = ['Ludhiana to Delhi', 'Delhi to Ludhiana', 'Phagwara to Delhi', 
                 'Jalandhar to Delhi', 'Delhi to Jalandhar', 'Jalandhar to Delhi Airport', 
                 'Ludhiana to Delhi Airport', 'Phagwara to Delhi Airport', 'Delhi Airport to Ludhiana', 'Delhi to Phagwara', 
                 'Delhi to Amritsar', 'Amritsar to Delhi', 'Delhi Airport to Patiala', 'Amritsar to Delhi Airport', 
                 'Kapurthala to Delhi', 'Delhi Airport to Jalandhar', 'Chandigarh to Bathinda', 'Chandigarh to Faridkot', 
                 'Chandigarh to Patiala']
    
    bus_route = st.selectbox('Select the route:',route)

    bus_type = st.selectbox('Select the bus type:',['Sleeper','Seater'])

    air_con = st.selectbox('Select A/C or Non A/C:',['A/C', 'Non A/C'])

    ratings = st.selectbox('Select the ratings:',['4 to 5','3 to 4','2 to 3','1 to 2','0 to 1','unrated'])

    

    price_option = ['upto ₹200','upto ₹400','upto ₹600','upto ₹800','upto ₹1000', 'upto ₹3500']
    price = st.select_slider('Select the bus fare:',price_option)
    

    click_button = st.button('search')

if bus_type == 'Sleeper' and air_con == 'A/C':
     bustype_query = """bustype LIKE '%Sleeper%'
                    AND (bustype LIKE '%A/C%' OR
                        bustype LIKE 'A/C%')
                    AND (bustype NOT LIKE '%Non%' OR
                        bustype NOT LIKE 'Non%' OR
                        bustype NOT LIKE 'NON%')"""
elif bus_type == 'Seater' and air_con == 'A/C':
     bustype_query = """bustype LIKE '%Seater%'
                    AND (bustype LIKE '%A/C%' OR
                        bustype LIKE 'A/C%')
                    AND bustype LIKE '%MULTI AXLE'
                    And (bustype NOT LIKE '%Non%' OR
                        bustype NOT LIKE 'Non%' OR
                        bustype NOT LIKE 'NON%')"""
elif bus_type == 'Sleeper' and air_con == 'Non A/C':
     bustype_query = """bustype LIKE '%Sleeper%'
                    AND (bustype LIKE '%Non%' OR
                        bustype LIKE 'Non%' OR
                        bustype LIKE 'NON%')"""  
elif bus_type == 'Seater' and air_con == 'Non A/C':
     bustype_query = """bustype LIKE '%Seater%'
                    AND (bustype LIKE '%Non%' OR
                        bustype LIKE 'Non%' OR
                        bustype LIKE 'NON%')"""         

if ratings == '4 to 5':
     rating_query = """star_rating >= 4 AND
                        star_rating <= 5"""
elif ratings == '3 to 4':
     rating_query = """star_rating >= 3 AND
                        star_rating <= 4"""
elif ratings == '2 to 3':
     rating_query = """star_rating >= 2 AND
                        star_rating <= 3"""
elif ratings == '1 to 2':
     rating_query = """star_rating >= 1 AND
                        star_rating <= 2"""
elif ratings == '0 to 1':
     rating_query = """star_rating > 0 AND
                        star_rating <= 1"""
elif ratings == 'unrated':
     rating_query = "star_rating = 0"




if price == 'upto ₹200':
     price_query = "price <= 200"
elif price == 'upto ₹400':
     price_query = "price <= 400"
elif price == 'upto ₹600':
     price_query = "price <= 600"
elif price == 'upto ₹800':
     price_query = "price <= 800"
elif price == 'upto ₹1000':
     price_query = "price <= 1000"
elif price == 'upto ₹3500':
     price_query = "price >= 3500"

st.title(':rainbow[RedBus information for the route]')

# query = f"""SELECT * FROM bus_routes WHERE
#             route_name = '{bus_route}' AND
#             {bustype_query} AND 
#             {rating_query} AND
#             {time_query};"""

query = f"""SELECT * FROM bus_routes WHERE
            route_name = '{bus_route}' AND 
            {bustype_query} AND
            {rating_query} AND
            {price_query};"""

if click_button:
        # Fetch data from the database
        data, columns = fetch_data(query)
        # Convert to a DataFrame
        df = pd.DataFrame(data, columns=columns)
   
        # Display the data
        st.write(df)
        