import streamlit as st
import requests

st.set_page_config(page_title="Units Conversion", page_icon="convert2.png")

# Main Categories of Conversion
conversion_types = {
    "Angle": ["Degrees", "Gradians", "Radians"],
    "Area": ["Acres", "Hectares", "Square Kilometers (km²)", "Square Meters (m²)", "Square Miles (mi²)"],
    "Currency": ["AUD (Australia)", "CAD (Canada)", "CNY (China)", "EUR (European Union)", "GBP (United Kingdom)", "INR (India)", "JPY (Japan)", "USD (United States of America)"],
    "Data Storage": ["Bits", "Bytes", "Kilobytes (KB)", "Megabytes (MB)", "Gigabytes (GB)", "Terabytes (TB)"],
    "Energy": ["Calories", "Joules (J)", "Kilowatt Hours (kWh)"],
    "Frequency": ["Gigahertz (GHz)", "Hertz (Hz)", "Kilohertz (kHz)", "Megahertz (MHz)"],
    "Length": ["Centimeters (cm)", "Feet (ft)", "Inches (in)", "Kilometers (km)", "Meters (m)", "Miles (mi)", "Millimeters (mm)", "Yards (yd)"],
    "Pressure": ["Atmospheres (atm)", "Bar", "Kilopascals (kPa)", "Millimeters of Mercury (mmHg)", "Pascals (Pa)", "Pounds per Square Inch (psi)"],
    "Speed": ["Kilometers per Hour (km/h)", "Knots", "Meters per Second (m/s)", "Miles per Hour (mph)"],
    "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
    "Time": ["Days", "Hours (hr)", "Minutes (min)", "Months", "Seconds (s)", "Weeks", "Years"],
    "Weight": ["Grams (g)", "Kilograms (kg)", "Metric Tons", "Ounces (oz)", "Pounds (lb)", "Stones"],
    "Fuel Consumption": ["Kilometers per Liter (km/L)", "Liters per 100 km (L/100 km)", "Miles per Gallon (MPG)"],
    "Volume": ["Cubic Meters (m³)", "Gallons", "Liters (L)", "Milliliters (mL)"]
}

st.sidebar.title("Conversion Categories")
selected_category = st.sidebar.selectbox("Select a Conversion Type", list(conversion_types.keys()))

st.title(f"{selected_category} Conversions")

# Conversion Logic Definitions
def convert_length(value, unit_from, unit_to):
    length_factors = {
        "Millimeters (mm)": 0.001,
        "Centimeters (cm)": 0.01,
        "Meters (m)": 1,
        "Kilometers (km)": 1000,
        "Inches (in)": 0.0254,
        "Feet (ft)": 0.3048,
        "Yards (yd)": 0.9144,
        "Miles (mi)": 1609.34,
    }
    return value * length_factors[unit_from] / length_factors[unit_to]

def convert_weight(value, unit_from, unit_to):
    weight_factors = {
        "Grams (g)": 1,
        "Kilograms (kg)": 1000,
        "Metric Tons": 1e6,
        "Pounds (lb)": 453.592,
        "Ounces (oz)": 28.3495,
        "Stones": 6350.29,
    }
    return value * weight_factors[unit_from] / weight_factors[unit_to]

def convert_temperature(value, unit_from, unit_to):
    if unit_from == unit_to:
        return value
    if unit_from == "Celsius (\u00b0C)":
        if unit_to == "Fahrenheit (\u00b0F)":
            return (value * 9/5) + 32
        elif unit_to == "Kelvin (K)":
            return value + 273.15
    elif unit_from == "Fahrenheit (\u00b0F)":
        if unit_to == "Celsius (\u00b0C)":
            return (value - 32) * 5/9
        elif unit_to == "Kelvin (K)":
            return (value - 32) * 5/9 + 273.15
    elif unit_from == "Kelvin (K)":
        if unit_to == "Celsius (\u00b0C)":
            return value - 273.15
        elif unit_to == "Fahrenheit (\u00b0F)":
            return (value - 273.15) * 9/5 + 32

def convert_time(value, unit_from, unit_to):
    time_factors = {
        "Seconds (s)": 1,
        "Minutes (min)": 60,
        "Hours (hr)": 3600,
        "Days": 86400,
        "Weeks": 604800,
        "Months": 2.628e6,
        "Years": 3.154e7,
    }
    return value * time_factors[unit_from] / time_factors[unit_to]

def convert_area(value, unit_from, unit_to):
    area_factors = {
        "Square Meters (m\u00b2)": 1,
        "Hectares": 10000,
        "Acres": 4046.86,
        "Square Kilometers (km\u00b2)": 1e6,
        "Square Miles (mi\u00b2)": 2.59e6,
    }
    return value * area_factors[unit_from] / area_factors[unit_to]

def convert_volume(value, unit_from, unit_to):
    volume_factors = {
        "Milliliters (mL)": 0.001,
        "Liters (L)": 1,
        "Cubic Meters (m\u00b3)": 1000,
        "Gallons": 3.78541,
    }
    return value * volume_factors[unit_from] / volume_factors[unit_to]

def convert_data_storage(value, unit_from, unit_to):
    data_storage_factors = {
        "Bits": 1,
        "Bytes": 8,
        "Kilobytes (KB)": 8192,
        "Megabytes (MB)": 8.39e6,
        "Gigabytes (GB)": 8.59e9,
        "Terabytes (TB)": 8.8e12,
    }
    return value * data_storage_factors[unit_from] / data_storage_factors[unit_to]

def convert_currency(value, unit_from, unit_to):
    api_key = '9198e01f6837629feeb0e88a'
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{unit_from[:3]}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        rate = data['conversion_rates'].get(unit_to[:3])
        if rate:
            return value * rate
        else:
            print(f"Error: Unable to find conversion rate for {unit_to}.")
    else:
        print(f"Error fetching data: {data.get('error-type', 'Unknown error')}")
    return None

def convert_speed(value, unit_from, unit_to):
    speed_factors = {
        "Meters per Second (m/s)": 1,
        "Kilometers per Hour (km/h)": 3.6,
        "Miles per Hour (mph)": 2.23694,
        "Knots": 1.94384,
    }
    return value * speed_factors[unit_from] / speed_factors[unit_to]

def convert_energy(value, unit_from, unit_to):
    energy_factors = {
        "Joules (J)": 1,
        "Calories": 4.184,
        "Kilowatt Hours (kWh)": 3.6e6,
    }
    return value * energy_factors[unit_from] / energy_factors[unit_to]

# New conversion functions
def convert_pressure(value, unit_from, unit_to):
    pressure_factors = {
        "Pascals (Pa)": 1,
        "Bar": 1e5,
        "Atmospheres (atm)": 101325,
        "Pounds per Square Inch (psi)": 6894.76,
        "Kilopascals (kPa)": 1000,
        "Millimeters of Mercury (mmHg)": 133.322,
    }
    return value * pressure_factors[unit_from] / pressure_factors[unit_to]

def convert_angle(value, unit_from, unit_to):
    if unit_from == unit_to:
        return value
    if unit_from == "Radians":
        if unit_to == "Degrees":
            return value * 180 / 3.14159265359
        elif unit_to == "Gradians":
            return value * 200 / 3.14159265359
    elif unit_from == "Degrees":
        if unit_to == "Radians":
            return value * 3.14159265359 / 180
        elif unit_to == "Gradians":
            return value * 200 / 180
    elif unit_from == "Gradians":
        if unit_to == "Radians":
            return value * 3.14159265359 / 200
        elif unit_to == "Degrees":
            return value * 180 / 200

def convert_fuel_consumption(value, unit_from, unit_to):
    if unit_from == unit_to:
        return value
    if unit_from == "Liters per 100 km (L/100 km)":
        if unit_to == "Miles per Gallon (MPG)":
            return 235.214583 / value
        elif unit_to == "Kilometers per Liter (km/L)":
            return 100 / value
    elif unit_from == "Miles per Gallon (MPG)":
        if unit_to == "Liters per 100 km (L/100 km)":
            return 235.214583 / value
        elif unit_to == "Kilometers per Liter (km/L)":
            return value * 0.425144
    elif unit_from == "Kilometers per Liter (km/L)":
        if unit_to == "Liters per 100 km (L/100 km)":
            return 100 / value
        elif unit_to == "Miles per Gallon (MPG)":
            return value * 2.35215

def convert_frequency(value, unit_from, unit_to):
    frequency_factors = {
        "Hertz (Hz)": 1,
        "Kilohertz (kHz)": 1e3,
        "Megahertz (MHz)": 1e6,
        "Gigahertz (GHz)": 1e9,
    }
    return value * frequency_factors[unit_from] / frequency_factors[unit_to]

def convert_power(value, unit_from, unit_to):
    power_factors = {
        "Watts (W)": 1,
        "Kilowatts (kW)": 1000,
        "Horsepower (hp)": 745.7,
        "BTUs per hour (BTU/h)": 0.293071,
    }
    return value * power_factors[unit_from] / power_factors[unit_to]

if selected_category:
    st.subheader("Available Units:")
    for unit in conversion_types[selected_category]:
        st.write(f"- {unit}")

    unit_from = st.selectbox(f"Select Unit to Convert From ({selected_category})", conversion_types[selected_category])
    unit_to = st.selectbox(f"Select Unit to Convert To ({selected_category})", conversion_types[selected_category])
    value = st.number_input(f"Enter the Value in {unit_from}", format="%.2f")

    if st.button("Convert"):
        result = None
        if selected_category == "Length":
            result = convert_length(value, unit_from, unit_to)
        elif selected_category == "Weight":
            result = convert_weight(value, unit_from, unit_to)
        elif selected_category == "Temperature":
            result = convert_temperature(value, unit_from, unit_to)
        elif selected_category == "Time":
            result = convert_time(value, unit_from, unit_to)
        elif selected_category == "Area":
            result = convert_area(value, unit_from, unit_to)
        elif selected_category == "Volume":
            result = convert_volume(value, unit_from, unit_to)
        elif selected_category == "Data Storage":
            result = convert_data_storage(value, unit_from, unit_to)
        elif selected_category == "Currency":
            result = convert_currency(value, unit_from, unit_to)
        elif selected_category == "Speed":
            result = convert_speed(value, unit_from, unit_to)
        elif selected_category == "Energy":
            result = convert_energy(value, unit_from, unit_to)
        elif selected_category == "Pressure":
            result = convert_pressure(value, unit_from, unit_to)
        elif selected_category == "Angle":
            result = convert_angle(value, unit_from, unit_to)
        elif selected_category == "Fuel Consumption":
            result = convert_fuel_consumption(value, unit_from, unit_to)
        elif selected_category == "Frequency":
            result = convert_frequency(value, unit_from, unit_to)
        elif selected_category == "Power":
            result = convert_power(value, unit_from, unit_to)

        if result is not None:
            st.success(f"Result : {result:.2f} {unit_to}")
        else:
            st.error("Conversion failed. Please check the inputs or try again.")