
import os
import json
import streamlit as st

from app_reset import main as reset_home
from home import main as show_home
from trip_planning import main as show_trip_planning
from trip_date_planning import main as show_trip_date_planning
from trip_location_planning import main as show_trip_location_planning
from trip_budget_planning import main as show_trip_budget_planning

management_json_file = "management.json"
if os.path.exists(management_json_file):
    management_json = json.loads(open(management_json_file,"r").read())
else:
    # management_json = {'trip_category': ''}
    # json.dump(management_json, open(management_json_file,'a'))
    reset_home()

# Define the pages
def home():
    show_home()

def page1():
    show_trip_planning()

def page2():
    show_trip_location_planning()

def page3():
    show_trip_date_planning()

def page4():
    show_trip_budget_planning()

# Create a dictionary to map page names to functions
pages = {
    "Page 1": page1,
    "Page 2": page2,
    "Page 3": page3,
    "Page 4": page4,
    "Home": home,
}

# # Create a selectbox for navigation
# selected_page = st.selectbox("Select a page:", list(pages.keys()))

# # Call the function corresponding to the selected page
# pages[selected_page]()

# Check if 'selected_page' is already in session state, if not set a default
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = list(pages.keys())[0]  # Default to the first page

if 'trip_category' not in st.session_state:
    st.session_state.trip_category = ''

# Functionality that uses the selected page
def display_page(page):
    pages[page]()  # Call the function associated with the selected page

# Call the function with the selected page
print("st.session_state.selected_page: ", st.session_state.selected_page)
print("st.session_state.trip_category: ", st.session_state.trip_category)

display_page(st.session_state.selected_page)

# Optionally, you can allow the user to change the page (if you want to show the selectbox)
# selected_page = st.selectbox("Select a page:", list(pages.keys()), index=list(pages.keys()).index(st.session_state.selected_page))
# st.session_state.selected_page = selected_page