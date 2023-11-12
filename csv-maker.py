import csv
import os
import ast  # Import the ast module for safely evaluating the string representation of a list

csv_lines = {}

csv_read = 'stats-all.csv'

with open(os.path.join(os.getcwd(), csv_read), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == "Pharmacy":
            # Use ast.literal_eval to safely convert the string representation of a list to an actual list
            populations_list = ast.literal_eval(row[1])

            average = (ast.literal_eval(row[2])[0] + (1 - ast.literal_eval(row[3])[0]) + ast.literal_eval(row[4])[0]) / 3

            csv_lines[row[0]] = [populations_list, ast.literal_eval(row[2])[0], 1 - ast.literal_eval(row[3])[0], ast.literal_eval(row[4])[0], average]

csv_read = 'counties.csv'
countiesdict = {}

# Open 'counties.csv' and read its contents into a list
with open(os.path.join(os.getcwd(), csv_read), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == 'GEOID':
            countiesdict[row[0]] = row[1]

# Iterate through csv_lines and counties_data to append values
for c, values_set in csv_lines.items():
    for cd in countiesdict.keys():
        if str(cd) in values_set[0][0][0]:
            csv_lines[c].append(countiesdict.get(cd))
            break

csv_read = 'census_summarized.csv'
census = {}

with open(os.path.join(os.getcwd(), csv_read), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0].__contains__('County'):
            for c, values_set in csv_lines.items():
                if row[0].__contains__(values_set[5]):
                    csv_lines[c].append(((1 - float(row[2])) + float(row[3]) + (1 - float(row[4]))) / 3)

# Rest of the code remains unchanged
output_csv = 'stats-all2.csv'

with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['Pharmacy', 'Populations', 'Insurance', 'Poverty', 'Work', 'Average', 'County', 'Target'])

    for pharmacy, values in csv_lines.items():
        if len(values) >= 5:
            populations_list, insurance, poverty, work, average, county, target = values
            csv_writer.writerow([pharmacy, populations_list, insurance, poverty, work, average, county, target])


csv_read = 'stats-all2.csv'
with open(os.path.join(os.getcwd(), csv_read), 'r') as file:
    csv_reader = csv.reader(file)

    for row in csv_reader:
        if not row[0] == 'Pharmacy':
            if float(row[5]) > float(row[7]):
                csv_lines[row[0]].append(False)
            else:
                csv_lines[row[0]].append(True)

output_csv = 'stats-all2.csv'

with open(output_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(['Pharmacy', 'Populations', 'Insurance', 'Poverty', 'Work', 'Average', 'County', 'Target', 'Result'])

    for pharmacy, values in csv_lines.items():
        if len(values) >= 5:
            populations_list, insurance, poverty, work, average, county, target, result = values
            csv_writer.writerow([pharmacy, populations_list, insurance, poverty, work, average, county, target, result])