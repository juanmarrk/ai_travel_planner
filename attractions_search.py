def main(location):

    import json
    import os
    import csv

    fl = './db/Attractions_India.csv'

    db = []

    for row in csv.DictReader(open(fl)):
        # print("From: ", row['From'], source_location)
        # print("To: ", row['To'], destination_location)
        # print("Price (INR): ", row['Price (INR)'], budget)
        if row['City'] == location:
            db.append(row)
    
    return db

if __name__ == "__main__":
    pl = main('Delhi', "Mumbai", "10004")
    print("pl: ", pl)