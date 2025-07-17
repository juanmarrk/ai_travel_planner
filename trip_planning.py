def main():

    import os
    import json
    import streamlit as st

    from app_reset import main as reset_home
    
    management_json_file = "management.json"
    if os.path.exists(management_json_file):
        management_json = json.loads(open(management_json_file,"r").read())
    else:
        management_json = {}

    st.title("What kind of trip are you planning ?")
    # st.write("This is Page 1.")

    # import streamlit as st

    # Set the title of the app
    # st.title("Multiple Choice Questions in a Row")

    # Create columns for the multiple choice questions
    col1 = st.columns(1)

    # First multiple choice question in the first column
    with col1[0]:
        option1 = st.selectbox('Select one:', ['Solo Trip', 'Partner Trip', 'Friends Trip', 'Family Trip'])
        # option1 = st.multiselect(
        #     'Select one:',
        #     ['Solo Trip', 'Partner Trip', 'Friends Trip', 'Family Trip']
        # )

    # Display the selected options
    st.write("You selected:")
    st.write("Trip Category:", option1)

    if 'trip_members' not in st.session_state:
        st.session_state.trip_members = 1

    if option1 == 'Solo Trip':
        st.session_state.trip_members = 1

    if option1 == 'Friends Trip':
        st.session_state.trip_members = 5

    if option1 == 'Family Trip':
        st.session_state.trip_members = 3

    fcol1, fcol2 = st.columns([4, 1])  # Create two equal columns

    with fcol1:
        if st.button("Reset", key='trip_planning_reset_button'):
            reset_home()

    with fcol2:
        if st.button("Next", key='trip_planning_next_button'):

            if 'trip_category' not in st.session_state:
                st.session_state.trip_category = option1

            if 'selected_page' not in st.session_state:
                st.session_state.selected_page = 'Page 2'

            st.session_state.trip_category = option1
            management_json['trip_category'] = option1
            json.dump(management_json, open(management_json_file,'w'))
            st.session_state.selected_page = 'Page 2'