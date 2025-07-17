
def main():

    import os
    import json
    import requests
    # import openai

    import pandas as pd
    import streamlit as st

    from openai import OpenAI

    from amadeus import Client, ResponseError
    from flight_search import main as flight_search_main
    from attractions_search import main as attractions_search_main
    from trip_location_planning import get_place_images, get_image_url
    from hotels_search  import main as hotels_search_main
    from cafe_search  import main as cafe_search_main

    # from gemini import Gemini
    # from google.generativeai import Client
    # import google.generativeai as genai

    # Google Maps API key
    API_KEY = 'KEY'

    # Initialize Amadeus client
    amadeus = Client(
        client_id='',
        client_secret=''
    )

    def get_lat_lon(place_name):
        
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={API_KEY}'
        
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'OK':
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']
            return str(lat) + "," + str(lon)
        else:
            return None

    def get_directions(origin, destination, waypoints_list):
        waypoints_str = '|'.join(waypoints_list)
        # url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"
        # url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&key={API_KEY}"
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&waypoints={waypoints_str}&alternatives=true&key={API_KEY}"
        response = requests.get(url)
        directions = response.json()
        return directions

    def generate_trip_plan(user_budget, departure_date, return_date, locations_routes, location_attraction_dict, flights_dict, hotels_offers_search_offers_dict, cafes_offers_search_offers_dict):

        # prompt = f"""Create a travel itinerary using the following
        #     source location and destination location direction routes: {json.dumps(locations_routes)}
        #     attactions: {json.dumps(location_attraction_dict)}
        #     """
        
        # client = OpenAI(
        #     api_key="",
        # )

        # return "Hi Random one: " + prompt

        # import openai
        # openai.api_base = 'https://api.openai.com/v1'

        # client = OpenAI(
        #     api_key=""
        # )

        # completion = client.chat.completions.create(
        #     # model="gpt-4o",
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        # )

        # return completion.choices[0].message.content

        # Initialize the Gemini client with your API key
        # genai.configure(api_key='')

        # trip_days = departure_date - return_date
        from datetime import datetime

        # Define the target date
        # target_date = datetime.strptime(return_date, '%Y/%m/%d')
        target_date = return_date

        # Get today's date
        # source_date = datetime.strptime(departure_date, '%Y/%m/%d')
        source_date = departure_date

        # Calculate the difference in days
        trip_days = (target_date - source_date).days

        # Define your custom knowledge base prompt
        custom_knowledge_base_prompt = f"""
        You are a travel agent. Sharing Important Considerations Before Booking, Important Notes and like other considered as you are not doing your job

        Create a travel itinerary ensuring following keypoinrs to include
        1. Trip Overview
        2. Recommended Flight Transportation (with price and date)
        3. Day Wise Planning according to the number of Days
        4. Budget

        Utilize
        0. User Budget: {user_budget}
        1. Departure Date: {departure_date}
        2. Arrival Date {return_date}
        3. source location and destination location direction routes: {json.dumps(locations_routes)}
        4. The attractions: {json.dumps(location_attraction_dict)}
        5. The available flights: {json.dumps(flights_dict)}
        6. Number of Days: {trip_days}
        7. Hotel Offers: {hotels_offers_search_offers_dict}
        8. Cafe and/or Restaurants Offers: {cafes_offers_search_offers_dict}

        """

        from google import genai

        # client = genai.Client(api_key="")
        client = genai.Client(api_key="")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[custom_knowledge_base_prompt]
        )
        # print(response.text)

        return response.text

    def fetch_attractions(location, radius=5000, type='tourist_attraction'):
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={type}&key={API_KEY}"
        response = requests.get(url)
        places = response.json()
        return places
        
    def compute_flight_tab():
            
        # st.header("Flight")

        origin = st.text_input("Enter Origin Airport Code (e.g., LAX):", "DEL")
        destination = st.text_input("Enter Destination Airport Code (e.g., JFK):", "BOM")
        adults=1
        # adults = st.number_input("Number of Adults:", min_value=1, value=1)

        if st.button("Search Flights"):
            if origin and destination and departure_date:
                print("departure_date: ", departure_date)
                print("return_date: ", return_date)
                try:
                    # Search for flights
                    response = amadeus.shopping.flight_offers_search.get(
                        originLocationCode=origin,
                        destinationLocationCode=destination,
                        departureDate=departure_date.strftime('%Y-%m-%d'),
                        returnDate=return_date.strftime('%Y-%m-%d') if return_date else None,
                        adults=adults
                    )
                    offers = response.data

                    # Display flight offers
                    if offers:
                        st.write("Available Flights:")
                        for offer in offers:
                            st.write(f"Price: {offer['price']['total']} {offer['price']['currency']}")
                            st.write(f"Departure: {offer['itineraries'][0]['segments'][0]['departure']['at']}")
                            st.write(f"Arrival: {offer['itineraries'][0]['segments'][0]['arrival']['at']}")
                            st.write("---")
                    else:
                        st.write("No flights found.")
                except ResponseError as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Please fill in all required fields.")
                
    def compute_hotel_tab():

        hotels_origin = st.text_input("Enter Hotel Name")
        # destination = st.text_input("Enter Destination Airport Code (e.g., JFK):")
        hotels_departure_date = st.date_input("Hotel Departure Date:")
        hotels_return_date = st.date_input("Hotel Checkout Date (optional):")
        hotels_adults=1
        # adults = st.number_input("Number of Adults:", min_value=1, value=1)

        if st.button("Search Hotels"):
            if hotels_origin and hotels_departure_date:

                import requests

                # Define the URL
                url = 'https://api.makcorps.com/mapping'

                # Define the parameters
                params = {
                    'api_key': '',
                    'name': hotels_origin,
                    'coords': " 28.679079,77.069710"
                }

                # Make the GET request
                response = requests.get(url, params=params)

                # Check the response status code
                if response.status_code == 200:
                    # Parse the JSON response (if applicable)
                    data = response.json()

                    st.write("Available Hotels:")
                    for offer in data:
                        st.write(offer)
                        # st.write(f"Price: {offer['price']['total']} {offer['price']['currency']}")
                        # st.write(f"Departure: {offer['itineraries'][0]['segments'][0]['departure']['at']}")
                        # st.write(f"Arrival: {offer['itineraries'][0]['segments'][0]['arrival']['at']}")
                        st.write("---")
                    # else:
                        # st.write("No flights found.")
                        # print(data)
                else:
                    print(f"Error: {response.status_code}")

        return ""

    # Streamlit UI
    st.title("AI-Powered Trip Planner")

    # User Input
    st.sidebar.header("Trip Planning")
    start_journey_location_name = st.sidebar.text_input("Source Location", st.session_state.start_journey_location_name)
    connected_journey_location_name = st.sidebar.text_input("Connected Location", "")
    connected_journey_location_name_list = connected_journey_location_name.split(',')
    end_journey_location_name = st.sidebar.text_input("Destination Location", st.session_state.end_journey_location_name)
    departure_date = st.sidebar.date_input("Departure Date:", st.session_state.departure_date)
    return_date = st.sidebar.date_input("Return Date (optional):", st.session_state.return_date)
    journey_budget = st.sidebar.text_input("Journey Budget", st.session_state.trip_budget)

    st.sidebar.subheader("Show Directions")

    if st.sidebar.button("Show Directions"):
        
        if start_journey_location_name and end_journey_location_name:

            directions = get_directions(start_journey_location_name, end_journey_location_name, waypoints_list=connected_journey_location_name_list)
            # directions_routes.append(directions)
            # print("directions_routes: ", directions_routes)

            if directions['status'] == 'OK':
                travel_time = directions['routes'][0]['legs'][0]['duration']['text']
                print(f"Travel time: {travel_time}")
                st.sidebar.write(f"Travel time: {travel_time}")

                st.sidebar.write("Directions:")
                for step in directions['routes'][0]['legs'][0]['steps']:
                    st.sidebar.write(step['html_instructions'])
            else:
                st.sidebar.write("Error fetching directions:", directions['status'])
        else:
            st.sidebar.write("Please enter both origin and destination.")

    # Fetch Attractions Section
    st.subheader("Find Attractions")

    destination_location_lat_lon = get_lat_lon(end_journey_location_name)
    if destination_location_lat_lon is None:
        destination_location_lat_lon = "37.7749,-122.4194"

    if len(connected_journey_location_name_list) > 0:

        for row in connected_journey_location_name_list:
            if len(row.strip()) > 0:
                _ = get_lat_lon(row)
                if _ is not None:
                    destination_location_lat_lon = destination_location_lat_lon + ";" + get_lat_lon(_)

    location_input = st.text_input("Location (latitude,longitude)", destination_location_lat_lon)
    if st.button("Get Attractions"):
        if location_input:
            payload = []
            payload = attractions_search_main(end_journey_location_name)
            # with st.expander("Nearby Attractions", expanded=False):
            #     for row in location_input.split(";"):
            #         attractions = fetch_attractions(row.strip())
            #         if attractions['status'] == 'OK':

            #             for place in attractions['results']:
            #                 st.write(f"**Name:** {place['name']}")
            #                 st.write(f"**Address:** {place.get('vicinity', 'N/A')}")
            #                 st.write(f"**Rating:** {place.get('rating', 'N/A')}")
            #                 st.write("---")
            #                 payload.append({
            #                     'Name': place['name'],
            #                     'Address': place.get('vicinity', 'N/A'),
            #                     'Rating': place.get('rating', 'N/A')
            #                 })
            #         else:
            #             st.write("Error fetching attractions:", attractions['status'])
            
            # Search for flights
            # flight_offers_search_response = amadeus.shopping.flight_offers_search.get(
            #     originLocationCode="DEL",
            #     destinationLocationCode="BOM",
            #     departureDate=departure_date.strftime('%Y-%m-%d'),
            #     returnDate=return_date.strftime('%Y-%m-%d') if return_date else None,
            #     adults=1
            # )
            # flight_offers_search_offers = flight_offers_search_response.data
            # flight_offers_search_offers_list = []
            # for offer in flight_offers_search_offers:
            #     _ = {}
            #     _['Departure Airport'] = start_journey_location_name
            #     _['Arrival Airport'] = end_journey_location_name
            #     _["Price"] = offer['price']['total'] + ' '+ offer['price']['currency']
            #     _["Departure"] = offer['itineraries'][0]['segments'][0]['departure']['at']
            #     _["Arrival"] = offer['itineraries'][0]['segments'][0]['arrival']['at']
            #     flight_offers_search_offers_list.append(_)

            flight_offers_search_offers_list = flight_search_main(start_journey_location_name, end_journey_location_name, st.session_state.trip_budget)
            # print("flight_offers_search_offers_list: ", flight_offers_search_offers_list)

            hotels_offers_search_offers_list = hotels_search_main(end_journey_location_name, departure_date, return_date, st.session_state.trip_budget)
            cafe_offers_search_offers_list = cafe_search_main(end_journey_location_name, st.session_state.trip_budget)

            """
            directions_routes_list = []
            directions_routes = get_directions(start_journey_location_name, end_journey_location_name, waypoints_list=connected_journey_location_name_list)
            if directions_routes['status'] == 'OK':
                for step in directions_routes['routes'][0]['legs'][0]['steps']:
                    directions_routes_list.append(step['html_instructions'])

                trip_plan = generate_trip_plan(journey_budget, departure_date, return_date, directions_routes_list, {'attractions': payload}, {'flights': flight_offers_search_offers_list}, {'hotels': hotels_offers_search_offers_list}, {'cafe/restaurants': cafe_offers_search_offers_list})
                st.write("Smart Recommendations:")
                st.write(trip_plan)
            """

            # Attractions
            for row in payload:
                api_key = ''
                if st.session_state.end_journey_location_name and api_key:
                    images = get_place_images(api_key, row['Attraction'])
                    if images:
                        st.subheader(row['Attraction'])
                        for image in images:
                            photo_reference = image['photo_reference']
                            image_url = get_image_url(photo_reference, api_key)
                            st.image(image_url, use_container_width=True)
                    else:
                        st.write("No images found for this location.")
                else:
                    st.write("Please enter both a location and your API key.")
        else:
            st.write("Please enter a valid location.")

    # st.subheader("Local Events")

    # events = {
    #     "name": ["Art Festival", "Food Fair", "Music Concert"],
    #     "date": ["2023-10-15", "2023-10-20", "2023-10-25"],
    #     "location": ["Downtown", "City Center", "Uptown"],
    # }
    # event_df = pd.DataFrame(events)
    # st.write(event_df)

    # Booking & Transport Section
    st.subheader("Bookings")
    # st.write("Options for booking flights, hotels, and tours will be integrated here.")
    tabs = st.tabs(["Flight", "Hotel"])

    with tabs[0]:
        compute_flight_tab()

    with tabs[1]:
        compute_hotel_tab()

    # Customize Your Trip Section
    st.subheader("Local Attractions")

    if st.button("Search Local Attractions"):
        import requests
        from requests.structures import CaseInsensitiveDict

        url = "https://api.geoapify.com/v2/places?categories=commercial.supermarket&filter=rect%3A10.716463143326969%2C48.755151258420966%2C10.835314015356737%2C48.680903341613316&limit=20&apiKey="

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"

        response = requests.get(url, headers=headers)

        # print(response.status_code)
        if response.status_code == 200:
            # Parse the JSON response (if applicable)
            data = response.json()

            st.write(data)