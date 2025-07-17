def main():

    import streamlit as st

    trip_budget = st.text_input("Trip Budget", "1000")

    if 'trip_budget' not in st.session_state:
        st.session_state.trip_budget = ''

    fcol1, fcol2 = st.columns([1, 1])

    with fcol1:
        if st.button("Back", key='trip_budget_planning_back_button'):
            st.session_state.selected_page = 'Page 3'

    with fcol2:
        if st.button("Next", key='trip_budget_planning_next_button'):
            st.session_state.trip_budget = trip_budget
            st.session_state.selected_page = 'Home'