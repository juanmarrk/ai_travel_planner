def main():

    import os
    import json
    import streamlit as st
    from datetime import datetime

    management_json_file = "management.json"
    if os.path.exists(management_json_file):
        management_json = json.loads(open(management_json_file,"r").read())
    else:
        management_json = {}

    # Set the title of the app
    st.title("Trip ("+ st.session_state.start_journey_location_name +" -> "+ st.session_state.end_journey_location_name+")")

    # Create a date input widget
    selected_date = st.date_input("Start date", datetime.today())
    end_date = st.date_input("End date", datetime.today())

    if 'departure_date' not in st.session_state:
        st.session_state.departure_date = selected_date
    
    if 'return_date' not in st.session_state:
        st.session_state.return_date = end_date

    st.session_state.departure_date = selected_date
    st.session_state.return_date = end_date

    # Display the selected date
    st.write("You selected:", selected_date)
    st.write("You selected:", end_date)

    fcol1, fcol2 = st.columns([1, 1])

    with fcol1:
        if st.button("Back", key='trip_date_planning_back_button'):
            st.session_state.selected_page = 'Page 2'

    with fcol2:
        if st.button("Next", key='trip_date_planning_next_button'):
            # management_json['trip_category'] = option1
            # json.dump(management_json, open(management_json_file,'w'))
            st.session_state.selected_page = 'Page 4'