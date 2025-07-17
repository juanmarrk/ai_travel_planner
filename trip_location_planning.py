
# Function to get place details from Google Places API
def get_place_images(api_key, location):

    import requests

    # URL for Google Places API
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=photos&key={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('candidates', [])
        if results:
            return results[0].get('photos', [])
    return []

# Function to get the full image URL
def get_image_url(photo_reference, api_key):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"

def unique_db_locations():

    import csv

    db = {}
    for row in csv.DictReader(open('./db/Budget_Flights_India.csv')):
        try:
            db[row['From']] = db[row['From']] + 1
        except:
            db[row['From']] = 1

    for row in csv.DictReader(open('./db/Budget_Flights_India.csv')):
        try:
            db[row['To']] = db[row['To']] + 1
        except:
            db[row['To']] = 1
    for row in csv.DictReader(open('./db/Attractions_India.csv')):
        try:
            db[row['City']] = db[row['City']] + 1
        except:
            db[row['City']] = 1
    for row in csv.DictReader(open('./db/Hotels_India.csv')):
        try:
            db[row['City']] = db[row['City']] + 1
        except:
            db[row['City']] = 1

    for row in csv.DictReader(open('./db/Restaurants_and_Cafes_India.csv')):
        try:
            db[row['City']] = db[row['City']] + 1
        except:
            db[row['City']] = 1
    
    return db.keys()

def main():

    import os
    import json
    import streamlit as st

    management_json_file = "management.json"
    if os.path.exists(management_json_file):
        management_json = json.loads(open(management_json_file,"r").read())
    else:
        management_json = {}

    # start_journey_location_name = st.text_input("Source Location", "")
    # start_journey_location_name = st.text_input("Departure Location", 'New Delhi')
    # end_journey_location_name = st.text_input("Arrival Location", "Mumbai")

    # options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    options = unique_db_locations()
    # Create a select box for the user to choose from the predefined list
    start_journey_location_name = st.selectbox('Departure Location', options)
    end_journey_location_name = st.selectbox("Arrival Location", options)

    # if 'start_journey_location_name' not in st.session_state:
    # if start_journey_location_name:
    if 'start_journey_location_name' not in st.session_state:
        st.session_state.start_journey_location_name = start_journey_location_name
        # st.session_state.start_journey_location_name = ''
    
    if 'end_journey_location_name' not in st.session_state:
        st.session_state.end_journey_location_name = end_journey_location_name
        # st.session_state.end_journey_location_name = ''

    # st.write("Current journey location:", st.session_state.start_journey_location_name)

    st.session_state.start_journey_location_name = start_journey_location_name
    st.session_state.end_journey_location_name = end_journey_location_name

    # st.write("start_journey_location_name:", start_journey_location_name)
    api_key = 'AIzaSyBn87CCJXa5YR2NViFNP2J-E2rpJMjPkhs'
    if st.session_state.end_journey_location_name and api_key:
        images = get_place_images(api_key, st.session_state.end_journey_location_name)
        if images:
            st.subheader("Images:")
            for image in images:
                photo_reference = image['photo_reference']
                image_url = get_image_url(photo_reference, api_key)
                st.image(image_url, use_container_width=True)
        else:
            st.write("No images found for this location.")
    else:
        st.write("Please enter both a location and your API key.")

    fcol1, fcol2 = st.columns([1, 1])

    with fcol1:
        if st.button("Back", key='trip_location_back_button'):
            st.session_state.selected_page = 'Page 1'

    with fcol2:
        if st.button("Next", key='trip_location_next_button'):
            # management_json['trip_category'] = option1
            # json.dump(management_json, open(management_json_file,'w'))

            st.session_state.start_journey_location_name = start_journey_location_name
            st.session_state.end_journey_location_name = end_journey_location_name

            management_json['start_journey_location_name'] = start_journey_location_name
            management_json['end_journey_location_name'] = end_journey_location_name
            json.dump(management_json, open(management_json_file,'w'))

            st.session_state.selected_page = 'Page 3'