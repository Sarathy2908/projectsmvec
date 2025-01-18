import os
import requests
import streamlit as st
import googlemaps
import folium
from streamlit_folium import folium_static
from datetime import datetime
import time

# API Key for Google Maps
API_KEY = 'AIzaSyCSb2z7EtzAMGB-IA3Bc7sqrRo99o1wM9k'  
gmaps = googlemaps.Client(key=API_KEY)

# Function to fetch current location
def get_current_location():
    try:
        geocode_result = gmaps.geolocate()
        location = geocode_result['location']
        return location['lat'], location['lng']
    except Exception as e:
        st.error(f"Error fetching location: {e}")
        return None, None

# Function to calculate route and emissions
def calculate_route(start, end, vehicle_type):
    now = datetime.now()
    try:
        directions_result = gmaps.directions(start, end, mode="driving", departure_time=now, traffic_model='best_guess')
        if directions_result:
            route = directions_result[0]
            leg = route['legs'][0]
            distance = leg['distance']['value']
            duration = leg['duration']['value']
            duration_in_traffic = leg.get('duration_in_traffic', leg['duration'])['value']
            emissions = calculate_emissions(distance, vehicle_type)
            return route, distance, duration, duration_in_traffic, emissions
        else:
            st.error("No route found.")
            return None, None, None, None, None
    except googlemaps.exceptions.ApiError as e:
        st.error(f"Google Maps API Error: {e}")
        return None, None, None, None, None
    except Exception as e:
        st.error(f"Error calculating route: {e}")
        return None, None, None, None, None

# Function to calculate CO2 emissions
def calculate_emissions(distance, vehicle_type):
    emissions_factor = {
        'Electric': 0,
        'Diesel': 2.68,
        'Gas': 2.31,
        'Hybrid': 1.5
    }
    return (distance / 1000) * emissions_factor.get(vehicle_type, 1.5)

# Function to create map with route details
def create_map(route):
    try:
        start_location = route['legs'][0]['start_location']
        end_location = route['legs'][0]['end_location']
        m = folium.Map(location=[start_location['lat'], start_location['lng']], zoom_start=13, tiles='CartoDB positron')

        folium.Marker([start_location['lat'], start_location['lng']], tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
        folium.Marker([end_location['lat'], end_location['lng']], tooltip="End", icon=folium.Icon(color='red')).add_to(m)

        route_coords = []
        for leg in route['legs']:
            for step in leg['steps']:
                if 'polyline' in step and 'points' in step['polyline']:
                    try:
                        points = googlemaps.convert.decode_polyline(step['polyline']['points'])
                        route_coords.extend(points)
                    except Exception as e:
                        st.warning(f"Error decoding polyline: {e}")
                        continue
                else:
                    st.warning("Polyline data missing in step.")

        if route_coords:
            folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(m)
        else:
            st.warning("No route coordinates available to draw the polyline.")
        return m
    except Exception as e:
        st.error(f"Error creating map: {e}")
        return None

# Function to fetch distance matrix
def get_distance_matrix(origins, destinations):
    try:
        matrix = gmaps.distance_matrix(origins, destinations, mode="driving")
        return matrix
    except Exception as e:
        st.error(f"Error fetching distance matrix: {e}")
        return None

# Streamlit Application
st.title("Dynamic Route Optimizer and Emission Estimator")

# Inputs
start_location = st.text_input("Enter Start Location:")
end_location = st.text_input("Enter End Location:")
vehicle_type = st.selectbox("Select Vehicle Type", ['Gas', 'Diesel', 'Hybrid', 'Electric'])

if st.button("Calculate Route"):
    try:
        # Handle "current location"
        if start_location.lower().strip() == "current location":
            start_lat, start_lon = get_current_location()
            if start_lat and start_lon:
                start_location = f"{start_lat},{start_lon}"
            else:
                st.error("Could not fetch current location. Please enter manually.")
                st.stop()

        # Geocode start and end locations
        start_coords = gmaps.geocode(start_location)[0]['geometry']['location'] if ',' not in start_location else {
            'lat': float(start_location.split(',')[0]),
            'lng': float(start_location.split(',')[1])
        }
        end_coords = gmaps.geocode(end_location)[0]['geometry']['location'] if ',' not in end_location else {
            'lat': float(end_location.split(',')[0]),
            'lng': float(end_location.split(',')[1])
        }

        # Calculate route and emissions
        route, distance, duration, duration_in_traffic, emissions = calculate_route(start_coords, end_coords, vehicle_type)

        if route:
            # Display the map
            map_obj = create_map(route)
            if map_obj:
                folium_static(map_obj)

            # Display route details
            st.markdown("### Route Details")
            st.write(f"**Distance:** {distance / 1000:.2f} km")
            st.write(f"**Estimated Time Without Traffic:** {duration // 60} min")
            st.write(f"**Estimated Time With Traffic:** {duration_in_traffic // 60} min")
            st.write(f"**Estimated CO2 Emissions:** {emissions:.2f} kg")

        else:
            st.error("Route calculation failed.")
    except ValueError as ve:
        st.error(str(ve))
    except Exception as e:
        import traceback
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error(f"Traceback:\n{traceback.format_exc()}")
