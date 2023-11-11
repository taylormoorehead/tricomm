import csv
import os

county_csv = 'county geoid - Sheet1.csv'
spatial_csv = 'spatial.csv'

geoid = []

with open(os.path.join(os.getcwd(), spatial_csv), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == 'GEOID':
            geoid.append(row[0])

counties = {}

with open(os.path.join(os.getcwd(), county_csv), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[3] == 'Geo Point':
            counties[row[8]] = row[9]

countydict = {}

for g in geoid:
    for c in counties.keys():
        if (g)[:5] == c:
            countydict[g] = counties.get(c)

output_csv = 'counties.csv'

with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the headers
    csv_writer.writerow(['Geo ID', 'County'])

    # Write the rows
    for geo_id, county in zip(countydict.keys(), countydict.values()):
        csv_writer.writerow([geo_id, county])

print("CSV file has been successfully created.")
