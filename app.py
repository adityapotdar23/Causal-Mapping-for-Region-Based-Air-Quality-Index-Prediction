import streamlit as st
import re

import requests
from bs4 import BeautifulSoup

# Example function to calculate AQI for PM2.5
def calculate_aqi_pm25(pm25):
    # AQI breakpoints and corresponding index values for PM2.5
    breakpoints = [0, 12, 35.4, 55.4, 150.4, 250.4, 350.4, 500.4]
    index_values = [0, 50, 100, 150, 200, 300, 400, 500]

    # Find the AQI category based on the concentration
    for i in range(len(breakpoints) - 1):
        if breakpoints[i] <= pm25 <= breakpoints[i + 1]:
            aqi_low = index_values[i]
            aqi_high = index_values[i + 1]
            breakpoint_low = breakpoints[i]
            breakpoint_high = breakpoints[i + 1]
            break
    else:
        # Handle out-of-range cases
        if pm25 < breakpoints[0]:
            aqi_low = index_values[0]
            aqi_high = index_values[0]
            breakpoint_low = breakpoints[0]
            breakpoint_high = breakpoints[1]
        elif pm25 > breakpoints[-1]:
            aqi_low = index_values[-1]
            aqi_high = index_values[-1]
            breakpoint_low = breakpoints[-2]
            breakpoint_high = breakpoints[-1]

    # Calculate AQI
    aqi = ((aqi_high - aqi_low) / (breakpoint_high - breakpoint_low)) * (pm25 - breakpoint_low) + aqi_low

    return aqi


# URL = "https://www.iqair.com/in-en/india/delhi/new-delhi"
# r = requests.get(URL)

# soup = BeautifulSoup(r.content, 'html.parser')

# # Find the table with class 'aqi-overview-detail__other-pollution-table'
# table = soup.find('table', class_='aqi-overview-detail__other-pollution-table')

# if table:
#     # Find all <tr> tags within the table's body
#     tbody = table.find('tbody')
#     rows = tbody.find_all('tr')

#     pm25_concentration = None
#     pm10_concentration = None
#     o3_concentration = None
#     no2_concentration = None
#     so2_concentration = None
#     co_concentration = None
    
#     for row in rows:
#         # Find all <td> tags within the current <tr> tag
#         cells = row.find_all('td')
#         # Extract pollutant name and concentration value
#         pollutant = cells[0].text.strip()
#         concentration = cells[2].find('span', class_='pollutant-concentration-value').text.strip()
#         if pollutant == 'PM2.5':
#             pm25_concentration = float(concentration)
#         elif pollutant == 'PM10':
#             pm10_concentration = float(concentration)
#         elif pollutant == 'O3':
#             o3_concentration = float(concentration)
#         elif pollutant == 'NO2':
#             no2_concentration = float(concentration)
#         elif pollutant == 'SO2':
#             so2_concentration = float(concentration)
#         elif pollutant == 'CO':
#             co_concentration = float(concentration)/1000
# else:
#     print("Table not found.")

def scrape_air_quality(city, country="india"):
    """
    Scrapes air quality data for a given city from the IQAir website.

    Parameters:
    - city (str): The name of the city for which to fetch air quality data.
    - country (str, optional): The name of the country. Defaults to "india".

    Returns:
    - dict: A dictionary containing the concentrations of various pollutants.
    """
    # Format city and country strings to fit the URL structure
    city_formatted = city.lower().replace(" ", "-")

    if(city_formatted=='mumbai'):
        URL = f"https://www.iqair.com/india/maharashtra/mumbai"
    elif(city_formatted=='new-delhi'):
        URL = "https://www.iqair.com/india/delhi/new-delhi"
    
    # Send the GET request
    # print(URL)
    r = requests.get(URL)
    
    # Parse the HTML content
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Find the table with the specified class
    table = soup.find('table', class_='aqi-overview-detail__other-pollution-table')
    
    air_quality_data = {}
    
    if table:
        # Find all <tr> tags within the table's body
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
        so2_concentration = 9
        # Loop through each row to extract pollutant concentrations
        for row in rows:
            cells = row.find_all('td')
            pollutant = cells[0].text.strip()
            concentration = cells[2].find('span', class_='pollutant-concentration-value').text.strip()
            if pollutant == 'PM2.5':
                pm25_concentration = float(concentration)
            elif pollutant == 'PM10':
                pm10_concentration = float(concentration)
            elif pollutant == 'O3':
                o3_concentration = float(concentration)
            elif pollutant == 'NO2':
                no2_concentration = float(concentration)
            elif pollutant == 'SO2':
                so2_concentration = float(concentration)
            elif pollutant == 'CO':
                co_concentration = float(concentration)/1000
    else:
        print("Table not found.")
    
    return pm25_concentration, pm10_concentration, o3_concentration, no2_concentration, so2_concentration, co_concentration

# print(pm25_concentration)
# print(pm10_concentration)
# print(o3_concentration)
# print(no2_concentration)
# print(so2_concentration)
# print(co_concentration)
    
def get_weather_data(city):
    """
    Fetches weather data for a given city from the Weather API.

    Parameters:
    - city (str): The name of the city for which to fetch weather data.

    Returns:
    - dict: A dictionary containing the temperature, humidity, wind speed (m/s),
            pressure (mmHg), wind degree, and rainfall for the city.
    """
    base_url = f'http://api.weatherapi.com/v1/current.json?key=2de71ea793984beeb8593410241703&q={city}'
    response = requests.get(base_url)
    if response.status_code == 200:
        x = response.json()
        wind_degree = x['current']['wind_degree']
        rainfall_mm = x['current']['precip_mm']
    
    if city=="Andheri":
        url = "https://weather.com/en-IN/weather/today/l/f7a5f2ac49c03ba32a82602a0dcdb6873a765a56231488a7a78b094818a18df9"
    elif city=="Patancheru":
        url = "https://weather.com/en-IN/weather/today/l/cdef225745ade209081f8c6be43a1bb69d16994b42d162d8c82b2b2aea45d0df"
    elif city=="Perungudi":
        url = "https://weather.com/en-IN/weather/today/l/351a15f0115e371a267b3ac11b1cef0ab7d02b4016464768389086c45069df11"
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the span element with data-testid="TemperatureValue"
    temperature_span = soup.find("span", {"data-testid": "TemperatureValue"})

    if temperature_span:
        # Extract the temperature value
        temperature_text = temperature_span.text.strip().replace('°', '')
        # temperature_value = 
        temperature_c = float(temperature_text)
    
    # Find the span element containing the wind speed value
    wind_speed_span = soup.find("span", {"data-testid": "Wind"})

    if wind_speed_span:
        # Extract the wind speed value
        wind_speed_value = wind_speed_span.find_all("span")[1].text.strip()
        wind_speed_value = float(wind_speed_value)*5/18
        wind_speed_m_s = round(wind_speed_value, 2)
        # print(wind_speed_value)
    
    # Find the span element with data-testid="PercentageValue"
    percentage_span = soup.find("span", {"data-testid": "PercentageValue"})

    if percentage_span:
        # Extract the numerical value
        numerical_value = percentage_span.text.strip('%')
        humidity = float(numerical_value)
    
    # Find the span element with data-testid="PressureValue"
    pressure_span = soup.find("span", {"data-testid": "PressureValue"})

    if pressure_span:
        # Extracting numerical value using regular expression
        pressure_value = re.search(r'[\d.]+', pressure_span.text.strip())
        
        if pressure_value:
            p = float(pressure_value.group())
            p = p*0.750062
            pressure_mmHg = round(p, 2)

    return temperature_c, humidity, wind_speed_m_s, pressure_mmHg, wind_degree, rainfall_mm



st.title('Analysis of Causal Mapping for Region-Based Air Quality Index Prediction')
option = st.selectbox(
    'Region',
    ("Andheri East, Mumbai", "ICRISAT Patancheru, Hyderabad, Telangana", "Perungudi, Chennai", "None"))

if(option=="Andheri East, Mumbai"):
    col1, col2 = st.columns(2)
    url = "https://weather.com/en-IN/forecast/air-quality/l/f7a5f2ac49c03ba32a82602a0dcdb6873a765a56231488a7a78b094818a18df9"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    o3_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="O3 (Ozone)")

    if o3_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = o3_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            o3_concentration = float(measurement_value.group())
            # print("Measurement of O3:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    co_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="CO (Carbon Monoxide)")

    if co_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = co_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            co_concentration = float(measurement_value.group())/1000
            # print("Measurement of CO:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    no2_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="NO2 (Nitrogen Dioxide)")

    if no2_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = no2_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            no2_concentration = float(measurement_value.group())
            # print("Measurement of NO2:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    pm10_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="PM10 (Particulate matter less than 10 microns)")

    if pm10_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = pm10_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip()) 
            pm10_concentration = float(measurement_value.group())
            # print("Measurement of PM10:", float(measurement_value.group()))
    
    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    pm25_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="PM2.5 (Particulate matter less than 2.5 microns)")

    if pm25_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = pm25_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            pm25_concentration = float(measurement_value.group())
            # print("Measurement of PM2.5:", float(measurement_value.group()))
    
    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    so2_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="SO2 (Sulphur Dioxide)")

    if so2_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = so2_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            so2_concentration = float(measurement_value.group())
            # print("Measurement of SO2:", float(measurement_value.group()))

    with col1:
        # pm25_concentration, pm10_concentration, o3_concentration, no2_concentration, so2_concentration, co_concentration = scrape_air_quality(option)
        # pm25_concentration = 65
        # pm10_concentration = 185
        # o3_concentration = 11
        # no2_concentration = 45
        # so2_concentration = 9
        # co_concentration = 983/1000
        st.text(f"PM2.5 Concentration: {pm25_concentration} ug/m3")
        st.text(f"PM10 Concentration: {pm10_concentration} ug/m3")
        st.text(f"Ozone Concentration: {o3_concentration} ug/m3")
        st.text(f"NO2 Concentration: {no2_concentration} ug/m3")
        st.text(f"SO2 Concentration: {so2_concentration} ug/m3")
        st.text(f"CO Concentration: {co_concentration/1000} mg/m3")
    with col2:
        temp, humidity, wind_speed, pressure, wind_degree, rainfall = get_weather_data('Andheri')
        st.text(f"Temperature: {temp} degree celcius")
        st.text(f"Humidity: {humidity} %")
        st.text(f"Wind Speed: {wind_speed} m/s")
        st.text(f"Pressure: {pressure} mmHg")
        st.text(f"Wind Degree: {wind_degree} degrees")
        st.text(f"Rainfall: {rainfall} mm")
    
    # short_codes = {'rainfall': 'RF', 'humidity': 'RH', 'wind_degree': 'WD', 'pressure': 'BP', 'temp': 'Temp', 'o3_concentration': 'Ozone', 'co_concentration': 'CO_mg', }

    relationship_strengths = {
    ("PM10", "PM2_5"): 0.49,
    ("SO2", "PM2_5"): -0.13,
    ("CO_mg", "PM2_5"): 3.15,
    ("Ozone", "PM2_5"): 0.13,
    ("Temp", "PM2_5"): -0.06,
    ("RH", "PM2_5"): 0.09,
    ("WS", "PM2_5"): 0.32,
    ("BP", "PM2_5"): 0.17,
    ("WD", "PM2_5"): -0.02,
    ("RF", "PM2_5"): -1.15,
    ("SO2", "PM10"): 1.11,
    ("CO_mg", "PM10"): 45.24,
    ("Ozone", "PM10"): 0.22,
    ("Temp", "PM10"): 1.41,
    ("RH", "PM10"): -1.05,
    ("WS", "PM10"): -1.60,
    ("BP", "PM10"): -0.65,
    ("WD", "PM10"): -0.11,
    ("RF", "PM10"): -23.36,
    ("PM10", "NO2"): 0.08,
    ("SO2", "NO2"): 0.27,
    ("CO_mg", "NO2"): 11.32,
    ("Temp", "NO2"): 0.28,
    ("RH", "NO2"): -0.15,
    ("WS", "NO2"): 0.65,
    ("BP", "NO2"): 0.48,
    ("CO_mg", "SO2"): 1.47,
    ("Temp", "SO2"): 0.05,
    ("WS", "SO2"): 0.48,
    ("BP", "SO2"): 0.06,
    ("WD", "SO2"): -0.00,
    ("RF", "SO2"): -1.21,
    ("Temp", "CO_mg"): 0.01,
    ("WS", "CO_mg"): 0.02,
    ("BP", "CO_mg"): 0.00,
    ("RF", "CO_mg"): -0.06,
    ("CO_mg", "Ozone"): -2.70,
    ("Temp", "Ozone"): 0.42,
    ("WS", "Ozone"): -0.21,
    ("BP", "Ozone"): 0.16,
    ("WS", "Temp"): 0.71,
    ("BP", "Temp"): 0.08,
    ("SO2", "RH"): -0.09,
    ("Ozone", "RH"): -0.26,
    ("Temp", "RH"): 0.53,
    ("WS", "RH"): -0.89,
    ("BP", "RH"): -0.22,
    ("WD", "RH"): 0.09,
    ("RF", "RH"): 5.56,
    ("WS", "BP"): -0.76,
    ("RF", "BP"): -4.24,
    ("CO_mg", "WD"): -4.43,
    ("Ozone", "WD"): 0.22,
    ("Temp", "WD"): 1.28,
    ("WS", "WD"): -2.41,
    ("BP", "WD"): 0.28,
    ("RF", "WD"): 8.36,
    ("PM2_5", "AQI"): 0.76,
    ("PM10", "AQI"): 0.16,
    ("SO2", "AQI"): 0.08,
    ("CO_mg", "AQI"): -1.83,
    ("Ozone", "AQI"): 0.03,
    ("Temp", "AQI"): -0.11,
    ("BP", "AQI"): 0.08,
    ("WD", "AQI"): -0.05,
    ("RF", "AQI"): -6.97
    }

    single_record = {'PM2_5': pm25_concentration, 'PM10': pm10_concentration, 'SO2': so2_concentration, 'NO2': no2_concentration, 'CO_mg': co_concentration, 'Ozone': o3_concentration, 'Temp': temp, 'BP': pressure, 'WD': wind_degree, 'RF': rainfall, 'RH': humidity, 'WS': wind_speed}

    causal_order = ['WS', 'RF', 'BP', 'Temp', 'CO_mg', 'Ozone', 'WD', 'SO2', 'RH', 'PM10', 'PM2_5', 'NO2', 'AQI']
    target_variable = "AQI"

    # Predict the value of the target variable using the causal order and strengths of relationships
    predicted_value = 0.0
    last_influencing_variable = None
    for i in range(1, len(causal_order)):
        influencing_variable = causal_order[i-1]
        influenced_variable = causal_order[i]
        if (influencing_variable, influenced_variable) in relationship_strengths:
          last_influencing_variable = influencing_variable
          print(influencing_variable, influenced_variable)
          weight = relationship_strengths[(influencing_variable, influenced_variable)]
          influencing_value = single_record[influencing_variable]
          predicted_value += weight * influencing_value
        else:
          if last_influencing_variable is not None:
            influencing_variable = last_influencing_variable
            influenced_variable = causal_order[i]
            if (influencing_variable, influenced_variable) in relationship_strengths:
              last_influencing_variable = influencing_variable
              print(influencing_variable, influenced_variable)
              weight = relationship_strengths[(influencing_variable, influenced_variable)]
              influencing_value = single_record[influencing_variable]
              predicted_value += weight * influencing_value
    # print("Predicted value of", target_variable, ":", predicted_value)

    caqi = calculate_aqi_pm25(pm25_concentration)

    st.info(f"Calcualted AQI: {caqi}")
    # st.success(f"Predicted AQI Using Causal Analysis: {predicted_value}")

elif(option=="ICRISAT Patancheru, Hyderabad, Telangana"):
    col1, col2 = st.columns(2)
    # URL = "https://www.iqair.com/in-en/india/telangana/patancheru"
    # r1 = requests.get(URL)
    # URL = "https://www.aqi.in/in/dashboard/india/telangana/hyderabad/icrisat-patancheru"
    # r2 = requests.get(URL)
    # time.sleep(5)
    # soup1 = BeautifulSoup(r1.content, 'html.parser')
    # soup2 = BeautifulSoup(r2.content, 'html.parser')
    # # Find the table with class 'aqi-overview-detail__other-pollution-table'
    # table = soup1.find('table', class_='aqi-overview-detail__other-pollution-table')

    # if table:
    #     # Find all <tr> tags within the table's body
    #     tbody = table.find('tbody')
    #     rows = tbody.find_all('tr')

    #     pm25_concentration = None
    #     pm10_concentration = None
    #     o3_concentration = None
    #     no2_concentration = None
    #     so2_concentration = None
    #     co_concentration = None

    # for row in rows:
    #     # Find all <td> tags within the current <tr> tag
    #     cells = row.find_all('td')
    #     # Extract pollutant name and concentration value
    #     pollutant = cells[0].text.strip()
    #     concentration = cells[2].find('span', class_='pollutant-concentration-value').text.strip()
    #     if pollutant == 'PM2.5':
    #         pm25_concentration = float(concentration)
    #     elif pollutant == 'PM10':
    #         pm10_concentration = float(concentration)
    #     elif pollutant == 'O3':
    #         o3_concentration = float(concentration)
    #     elif pollutant == 'NO2':
    #         no2_concentration = float(concentration)
    #     elif pollutant == 'SO2':
    #         so2_concentration = float(concentration)
    #     elif pollutant == 'CO':
    #         co_concentration = float(concentration)
    #     else:
    #         print("Table not found.")
    
    # if pm25_concentration is None:
    #     pm25_concentration = soup2.find(class_="Pollutants_sensor_text pm25").text
    # if pm10_concentration is None:
    #     pm10_concentration = soup2.find(class_="Pollutants_sensor_text pm10").text
    # if so2_concentration is None:
    #     for div in soup2.find_all("div", style="display: inline-block;"):
    # # Find the span tag with class "Pollutants_sensor_text_s" within the div
    #         pollutant_s = div.find("span", class_="Pollutants_sensor_text_s")
    #         if pollutant_s and "SO2" in pollutant_s.text:
    #         # If SO2 is found, find its parent div
    #             parent_div = pollutant_s.parent
    #             # Find the span tag with class "Pollutants_sensor_text" within the parent div
    #             so2_span = parent_div.find_previous_sibling("span", class_="Pollutants_sensor_text")
    #             if so2_span:
    #                 so2_concentration = so2_span.text
    #                 break
    #     so2_concentration = int(so2_concentration)
    # if co_concentration is None:
    #     # Find all divs with style "display: inline-block;"
    #     for div in soup2.find_all("div", style="display: inline-block;"):
    #         # Find the span tag with class "Pollutants_sensor_text_s" within the div
    #         pollutant_s = div.find("span", class_="Pollutants_sensor_text_s")
    #         if pollutant_s and "CO" in pollutant_s.text:
    #         # If co is found, find its parent div
    #             parent_div = pollutant_s.parent
    #             # Find the span tag with class "Pollutants_sensor_text" within the parent div
    #             co_span = parent_div.find_previous_sibling("span", class_="Pollutants_sensor_text")
    #             if co_span:
    #                 co_value = co_span.text
    #                 break
    #     co_concentration = float(co_value)
    
    # if o3_concentration is None:
    #     # Find all divs with style "display: inline-block;"
    #     for div in soup2.find_all("div", style="display: inline-block;"):
    #         # Find the span tag with class "Pollutants_sensor_text_s" within the div
    #         pollutant_s = div.find("span", class_="Pollutants_sensor_text_s")
    #         if pollutant_s and "Ozone" in pollutant_s.text:
    #         # If ozone is found, find its parent div
    #             parent_div = pollutant_s.parent
    #             # Find the span tag with class "Pollutants_sensor_text" within the parent div
    #             ozone_span = parent_div.find_previous_sibling("span", class_="Pollutants_sensor_text")
    #             if ozone_span:
    #                 o3_concentration = ozone_span.text
    #                 break
        
    #     o3_concentration = float(o3_concentration)
    
    # if no2_concentration is None:
    #     # Find all divs with style "display: inline-block;"
    #     for div in soup2.find_all("div", style="display: inline-block;"):
    #         # Find the span tag with class "Pollutants_sensor_text_s" within the div
    #         pollutant_s = div.find("span", class_="Pollutants_sensor_text_s")
    #         if pollutant_s and "NO2" in pollutant_s.text:
    #             # If no2 is found, find its parent div
    #             parent_div = pollutant_s.parent
    #             # Find the span tag with class "Pollutants_sensor_text" within the parent div
    #             no2_span = parent_div.find_previous_sibling("span", class_="Pollutants_sensor_text")
    #             if no2_span:
    #                 no2_concentration = no2_span.text
    #                 break
            
        # no2_concentration = float(no2_concentration)
    
    url = "https://weather.com/en-IN/forecast/air-quality/l/b76ca9bb0fafdb6ce4c0abf8fa762ba34f057d3e961705dee20508edfc546f4e"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    o3_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="O3 (Ozone)")

    if o3_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = o3_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            o3_concentration = float(measurement_value.group())
            # print("Measurement of O3:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    co_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="CO (Carbon Monoxide)")

    if co_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = co_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            co_concentration = float(measurement_value.group())/1000
            # print("Measurement of CO:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    no2_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="NO2 (Nitrogen Dioxide)")

    if no2_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = no2_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            no2_concentration = float(measurement_value.group())
            # print("Measurement of NO2:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    pm10_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="PM10 (Particulate matter less than 10 microns)")

    if pm10_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = pm10_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip()) 
            pm10_concentration = float(measurement_value.group())
            # print("Measurement of PM10:", float(measurement_value.group()))
    
    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    pm25_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="PM2.5 (Particulate matter less than 2.5 microns)")

    if pm25_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = pm25_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            pm25_concentration = float(measurement_value.group())
            # print("Measurement of PM2.5:", float(measurement_value.group()))
    
    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    so2_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="SO2 (Sulphur Dioxide)")

    if so2_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = so2_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            so2_concentration = float(measurement_value.group())
            # print("Measurement of SO2:", float(measurement_value.group()))

    with col1:
        # pm25_concentration, pm10_concentration, o3_concentration, no2_concentration, so2_concentration, co_concentration = scrape_air_quality(option)
        # pm25_concentration = 65
        # pm10_concentration = 185
        # o3_concentration = 11
        # no2_concentration = 45
        # so2_concentration = 9
        # co_concentration = 983/1000
        st.text(f"PM2.5 Concentration: {pm25_concentration} ug/m3")
        st.text(f"PM10 Concentration: {pm10_concentration} ug/m3")
        st.text(f"Ozone Concentration: {o3_concentration} ug/m3")
        st.text(f"NO2 Concentration: {no2_concentration} ug/m3")
        st.text(f"SO2 Concentration: {so2_concentration} ug/m3")
        st.text(f"CO Concentration: {co_concentration/1000} mg/m3")
    with col2:
        temp, humidity, wind_speed, pressure, wind_degree, rainfall = get_weather_data('Patancheru')
        st.text(f"Temperature: {temp} degree celcius")
        st.text(f"Humidity: {humidity} %")
        st.text(f"Wind Speed: {wind_speed} m/s")
        st.text(f"Pressure: {pressure} mmHg")
        st.text(f"Wind Degree: {wind_degree} degrees")
        st.text(f"Rainfall: {rainfall} mm")
    
    # short_codes = {'rainfall': 'RF', 'humidity': 'RH', 'wind_degree': 'WD', 'pressure': 'BP', 'temp': 'Temp', 'o3_concentration': 'Ozone', 'co_concentration': 'CO_mg', }

    relationship_strengths = {
    ("SO2", "PM2_5"): 1.23,
    ("Ozone", "PM2_5"): 0.07,
    ("Temp", "PM2_5"): 0.66,
    ("RH", "PM2_5"): -0.02,
    ("WS", "PM2_5"): -9.84,
    ("WD", "PM2_5"): -0.09,
    ("RF", "PM2_5"): -5.93,
    ("PM2_5", "PM10"): 1.89,
    ("SO2", "PM10"): 0.49,
    ("Ozone", "PM10"): -0.20,
    ("Temp", "PM10"): 0.83,
    ("RH", "PM10"): -0.77,
    ("WD", "PM10"): 0.04,
    ("RF", "PM10"): -2.78,
    ("PM2_5", "NO2"): 0.05,
    ("PM10", "NO2"): 0.15,
    ("SO2", "NO2"): 0.35,
    ("Ozone", "NO2"): -0.07,
    ("Temp", "NO2"): 0.13,
    ("RH", "NO2"): 0.07,
    ("WS", "NO2"): -1.13,
    ("WD", "NO2"): -0.02,
    ("Ozone", "SO2"): 0.09,
    ("Temp", "SO2"): 0.07,
    ("WD", "SO2"): -0.01,
    ("RF", "SO2"): -1.52,
    ("PM2_5", "CO_mg"): -0.00,
    ("PM10", "CO_mg"): 0.00,
    ("NO2", "CO_mg"): 0.01,
    ("SO2", "CO_mg"): -0.00,
    ("Ozone", "CO_mg"): 0.00,
    ("RH", "CO_mg"): 0.00,
    ("WS", "CO_mg"): -0.01,
    ("WD", "CO_mg"): 0.00,
    ("Temp", "Ozone"): 0.63,
    ("WS", "Ozone"): 5.67,
    ("WD", "Ozone"): -0.07,
    ("RF", "Ozone"): -3.60,
    ("WS", "Temp"): 0.88,
    ("SO2", "RH"): -0.20,
    ("Ozone", "RH"): -0.34,
    ("Temp", "RH"): 0.45,
    ("WS", "RH"): -0.34,
    ("WD", "RH"): 0.02,
    ("RF", "RH"): 9.80,
    ("RF", "WS"): 0.11,
    ("PM2_5", "BP"): 0.10,
    ("PM10", "BP"): -0.04,
    ("NO2", "BP"): 0.22,
    ("SO2", "BP"): -0.12,
    ("CO_mg", "BP"): -6.54,
    ("Ozone", "BP"): 0.11,
    ("Temp", "BP"): 0.29,
    ("RH", "BP"): 0.18,
    ("WS", "BP"): -3.00,
    ("WD", "BP"): -0.00,
    ("RF", "BP"): -1.14,
    ("Temp", "WD"): 1.54,
    ("WS", "WD"): 32.44,
    ("RF", "WD"): 39.27,
    ("PM2_5", "AQI"): 1.90,
    ("PM10", "AQI"): 0.01,
    ("SO2", "AQI"): -0.13,
    ("CO_mg", "AQI"): -2.61,
    ("Ozone", "AQI"): 0.07,
    ("Temp", "AQI"): 0.43,
    ("RH", "AQI"): -0.20,
    ("WS", "AQI"): -1.29,
    ("WD", "AQI"): -0.01,
    ("RF", "AQI"): 1.45
    }

    single_record = {'PM2_5': pm25_concentration, 'PM10': pm10_concentration, 'SO2': so2_concentration, 'NO2': no2_concentration, 'CO_mg': co_concentration, 'Ozone': o3_concentration, 'Temp': temp, 'BP': pressure, 'WD': wind_degree, 'RF': rainfall, 'RH': humidity, 'WS': wind_speed}

    causal_order = ['RF', 'WS', 'Temp', 'WD', 'Ozone', 'SO2', 'RH', 'PM2_5', 'PM10', 'NO2', 'CO_mg', 'BP', 'AQI']
    target_variable = "AQI"

    # Predict the value of the target variable using the causal order and strengths of relationships
    predicted_value = 0.0
    last_influencing_variable = None
    for i in range(1, len(causal_order)):
        influencing_variable = causal_order[i-1]
        influenced_variable = causal_order[i]
        if (influencing_variable, influenced_variable) in relationship_strengths:
          last_influencing_variable = influencing_variable
          print(influencing_variable, influenced_variable)
          weight = relationship_strengths[(influencing_variable, influenced_variable)]
          influencing_value = single_record[influencing_variable]
          predicted_value += weight * influencing_value
        else:
          if last_influencing_variable is not None:
            influencing_variable = last_influencing_variable
            influenced_variable = causal_order[i]
            if (influencing_variable, influenced_variable) in relationship_strengths:
              last_influencing_variable = influencing_variable
              print(influencing_variable, influenced_variable)
              weight = relationship_strengths[(influencing_variable, influenced_variable)]
              influencing_value = single_record[influencing_variable]
              predicted_value += weight * influencing_value
    # print("Predicted value of", target_variable, ":", predicted_value)

    caqi = calculate_aqi_pm25(pm25_concentration)

    st.info(f"Calcualted AQI: {caqi}")
    # st.success(f"Predicted AQI Using Causal Analysis: {predicted_value}")

elif(option=="Perungudi, Chennai"):
    col1, col2 = st.columns(2)
    url = "https://weather.com/en-IN/forecast/air-quality/l/351a15f0115e371a267b3ac11b1cef0ab7d02b4016464768389086c45069df11"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    o3_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="O3 (Ozone)")

    if o3_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = o3_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            o3_concentration = float(measurement_value.group())
            # print("Measurement of O3:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    co_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="CO (Carbon Monoxide)")

    if co_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = co_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            co_concentration = float(measurement_value.group())/1000
            # print("Measurement of CO:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    no2_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="NO2 (Nitrogen Dioxide)")

    if no2_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = no2_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            no2_concentration = float(measurement_value.group())
            # print("Measurement of NO2:", float(measurement_value.group()))

    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    pm10_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="PM10 (Particulate matter less than 10 microns)")

    if pm10_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = pm10_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip()) 
            pm10_concentration = float(measurement_value.group())
            # print("Measurement of PM10:", float(measurement_value.group()))
    
    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    pm25_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="PM2.5 (Particulate matter less than 2.5 microns)")

    if pm25_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = pm25_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            pm25_concentration = float(measurement_value.group())
            # print("Measurement of PM2.5:", float(measurement_value.group()))
    
    # Find the span element with data-testid="AirQualityCategory" containing "CO"
    so2_span = soup.find("span", {"data-testid": "AirQualityCategory"}, string="SO2 (Sulphur Dioxide)")

    if so2_span:
        # Find the next subsequent span element with data-testid="AirQualityMeasurement"
        measurement_span = so2_span.find_next_sibling("span", {"data-testid": "AirQualityMeasurement"})
        
        if measurement_span:
            measurement_value = re.search(r'\d+(\.\d+)?', measurement_span.text.strip())
            so2_concentration = float(measurement_value.group())
            # print("Measurement of SO2:", float(measurement_value.group()))

    with col1:
        # pm25_concentration, pm10_concentration, o3_concentration, no2_concentration, so2_concentration, co_concentration = scrape_air_quality(option)
        # pm25_concentration = 65
        # pm10_concentration = 185
        # o3_concentration = 11
        # no2_concentration = 45
        # so2_concentration = 9
        # co_concentration = 983/1000
        st.text(f"PM2.5 Concentration: {pm25_concentration} ug/m3")
        st.text(f"PM10 Concentration: {pm10_concentration} ug/m3")
        st.text(f"Ozone Concentration: {o3_concentration} ug/m3")
        st.text(f"NO2 Concentration: {no2_concentration} ug/m3")
        st.text(f"SO2 Concentration: {so2_concentration} ug/m3")
        st.text(f"CO Concentration: {co_concentration/1000} mg/m3")
    with col2:
        temp, humidity, wind_speed, pressure, wind_degree, rainfall = get_weather_data('Perungudi')
        st.text(f"Temperature: {temp} degree celcius")
        st.text(f"Humidity: {humidity} %")
        st.text(f"Wind Speed: {wind_speed} m/s")
        st.text(f"Pressure: {pressure} mmHg")
        st.text(f"Wind Degree: {wind_degree} degrees")
        st.text(f"Rainfall: {rainfall} mm")
    
    # short_codes = {'rainfall': 'RF', 'humidity': 'RH', 'wind_degree': 'WD', 'pressure': 'BP', 'temp': 'Temp', 'o3_concentration': 'Ozone', 'co_concentration': 'CO_mg', }

    relationship_strengths = {
    ("PM10", "PM2_5"): 0.48,
    ("SO2", "PM2_5"): 0.95,
    ("CO_mg", "PM2_5"): 1.27,
    ("Temp", "PM2_5"): -0.10,
    ("RH", "PM2_5"): 0.78,
    ("WS", "PM2_5"): 1.98,
    ("BP", "PM2_5"): 0.12,
    ("WD", "PM2_5"): -0.02,
    ("RF", "PM2_5"): 0.91,
    ("SO2", "PM10"): 3.20,
    ("CO_mg", "PM10"): 3.41,
    ("Ozone", "PM10"): -0.36,
    ("Temp", "PM10"): 0.78,
    ("RH", "PM10"): -2.06,
    ("WS", "PM10"): -14.74,
    ("BP", "PM10"): -0.36,
    ("WD", "PM10"): -0.14,
    ("RF", "PM10"): -10.05,
    ("PM10", "NO2"): 0.04,
    ("SO2", "NO2"): 0.15,
    ("CO_mg", "NO2"): 0.36,
    ("Ozone", "NO2"): -0.05,
    ("RH", "NO2"): 0.04,
    ("WS", "NO2"): -2.68,
    ("BP", "NO2"): -0.16,
    ("WD", "NO2"): 0.00,
    ("RF", "NO2"): 0.82,
    ("Ozone", "SO2"): 0.00,
    ("Temp", "SO2"): -0.10,
    ("RH", "SO2"): -0.03,
    ("BP", "SO2"): 0.02,
    ("WD", "SO2"): -0.00,
    ("RF", "SO2"): -0.15,
    ("RF", "CO_mg"): -0.08,
    ("CO_mg", "Ozone"): -2.44,
    ("Temp", "Ozone"): -0.48,
    ("RH", "Ozone"): -0.74,
    ("BP", "Ozone"): -0.17,
    ("WD", "Ozone"): 0.02,
    ("RH", "Temp"): -0.11,
    ("BP", "Temp"): 0.12,
    ("WD", "Temp"): -0.01,
    ("CO_mg", "RH"): -1.62,
    ("WD", "RH"): -0.02,
    ("RF", "RH"): 5.26,
    ("SO2", "WS"): 0.02,
    ("CO_mg", "WS"): -0.04,
    ("Ozone", "WS"): 0.00,
    ("Temp", "WS"): -0.01,
    ("RH", "WS"): -0.04,
    ("BP", "WS"): -0.01,
    ("WD", "WS"): -0.00,
    ("RF", "WS"): 0.37,
    ("CO_mg", "BP"): 4.48,
    ("RH", "BP"): -0.18,
    ("WD", "BP"): -0.02,
    ("RF", "BP"): -0.64,
    ("CO_mg", "WD"): -7.67,
    ("RF", "WD"): -21.08,
    ("PM2_5", "AQI"): 1.19,
    ("PM10", "AQI"): 0.23,
    ("NO2", "AQI"): 0.81,
    ("CO_mg", "AQI"): 0.86,
    ("WS", "AQI"): 1.55,
    ("BP", "AQI"): 0.41,
    ("WD", "AQI"): -0.06
    }

    single_record = {'PM2_5': pm25_concentration, 'PM10': pm10_concentration, 'SO2': so2_concentration, 'NO2': no2_concentration, 'CO_mg': co_concentration, 'Ozone': o3_concentration, 'Temp': temp, 'BP': pressure, 'WD': wind_degree, 'RF': rainfall, 'RH': humidity, 'WS': wind_speed}

    causal_order = ['RF', 'CO_mg', 'WD', 'RH', 'BP', 'Temp', 'Ozone', 'SO2', 'WS', 'PM10', 'NO2', 'PM2_5', 'AQI']
    target_variable = "AQI"

    # Predict the value of the target variable using the causal order and strengths of relationships
    predicted_value = 0.0
    last_influencing_variable = None
    for i in range(1, len(causal_order)):
        influencing_variable = causal_order[i-1]
        influenced_variable = causal_order[i]
        if (influencing_variable, influenced_variable) in relationship_strengths:
          last_influencing_variable = influencing_variable
          print(influencing_variable, influenced_variable)
          weight = relationship_strengths[(influencing_variable, influenced_variable)]
          influencing_value = single_record[influencing_variable]
          predicted_value += weight * influencing_value
        else:
          if last_influencing_variable is not None:
            influencing_variable = last_influencing_variable
            influenced_variable = causal_order[i]
            if (influencing_variable, influenced_variable) in relationship_strengths:
              last_influencing_variable = influencing_variable
              print(influencing_variable, influenced_variable)
              weight = relationship_strengths[(influencing_variable, influenced_variable)]
              influencing_value = single_record[influencing_variable]
              predicted_value += weight * influencing_value
    # print("Predicted value of", target_variable, ":", predicted_value)

    if predicted_value<0:
        predicted_value = abs(predicted_value)
        
    caqi = calculate_aqi_pm25(pm25_concentration)

    st.info(f"Calcualted AQI: {caqi}")

if predicted_value > 300:
    st.markdown(f'<span style="color: maroon;font-size: 20px;">Predicted AQI using Causal Analysis: {predicted_value}</span>', unsafe_allow_html=True)
    st.markdown('<span style="color: maroon;font-size: 20px;">Hazardous: Everyone may experience more serious health effects. Everyone should avoid all outdoor exertion.</span>', unsafe_allow_html=True)
elif predicted_value > 200:
    st.markdown(f'<span style="color: purple;font-size: 20px;">Predicted AQI using Causal Analysis: {predicted_value}</span>', unsafe_allow_html=True)
    st.markdown('<span style="color: purple;font-size: 20px;">Very Unhealthy: Health warnings of emergency conditions. The entire population is more likely to be affected. Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion.</span>', unsafe_allow_html=True)
elif predicted_value > 150:
    st.markdown(f'<span style="color: red;font-size: 20px;">Predicted AQI using Causal Analysis: {predicted_value}</span>', unsafe_allow_html=True)
    st.markdown('<span style="color: red;font-size: 20px;">Unhealthy: Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects. Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion</span>', unsafe_allow_html=True)
elif predicted_value > 100:
    st.markdown(f'<span style="color: orange;font-size: 20px;">Predicted AQI using Causal Analysis: {predicted_value}</span>', unsafe_allow_html=True)
    st.markdown('<span style="color: orange;font-size: 20px;">Unhealthy for Sensitive Groups: Members of sensitive groups may experience health effects. The general public is not likely to be affected. Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.</span>', unsafe_allow_html=True)
elif predicted_value > 50:
    st.markdown(f'<span style="color: yellow;font-size: 20px;">Predicted AQI using Causal Analysis: {predicted_value}</span>', unsafe_allow_html=True)
    st.markdown('<span style="color: yellow;font-size: 20px;">Moderate: Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution. Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.</span>', unsafe_allow_html=True)
else :
    st.markdown(f'<span style="color: green;font-size: 20px;">Predicted AQI using Causal Analysis: {predicted_value}</span>', unsafe_allow_html=True)
    st.markdown('<span style="color: green;font-size: 20px;">Good: Air quality is considered satisfactory, and air pollution poses little or no risk</span>', unsafe_allow_html=True)


