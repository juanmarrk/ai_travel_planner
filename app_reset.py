def main():

    import json
    management_json_file = "management.json"
    management_json = {
        'trip_category': '',
        'start_journey_location_name': '',
        'end_journey_location_name': '',
        'current_page_index': 0
    }
    json.dump(management_json, open(management_json_file,'w'))
