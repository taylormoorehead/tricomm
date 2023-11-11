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