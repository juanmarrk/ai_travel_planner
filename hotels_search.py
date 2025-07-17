def main(source_location, departure_date, return_date, budget):

    import json
    import os
    import csv

    fl = './db/Hotels_India.csv'

    db = []

    trip_days = (departure_date - return_date).days

    # print("source_location: ", source_location)
    # print("destination_location: ", destination_location)
    # print("budget: ", budget)

    for row in csv.DictReader(open(fl)):
        # print("From: ", row['From'], source_location)
        # print("To: ", row['To'], destination_location)
        # print("Price (INR): ", row['Price (INR)'], budget)
        if row['City'] == source_location and float(row['Price/Night (INR)']) * trip_days <= float(budget):
            db.append(row)
    
    return db

if __name__ == "__main__":
    pl = main('Delhi', "Mumbai", "10004")
    print("pl: ", pl)