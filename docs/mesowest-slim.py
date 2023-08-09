import csv

mw_data_file = 'C:\\Users\\JOKN001\\Downloads\\HPN27.csv'
out_file = 'HPN27_slim_20230726.csv'

out_data = []

with open(mw_data_file, 'r') as file:
    mw_data_file_lines = file.readlines()
    # del the first six lines; headers are on the seventh line
    del(mw_data_file_lines[:6])
    # row below headers contains measurement units
    del(mw_data_file_lines[1])
    mw_data_rows = csv.reader(mw_data_file_lines)
    for row in mw_data_rows:
        # skip the header row
        if row[0] == 'Station_ID':
            next
        # we are only interested in the first 9 columns
        out_data.append(row[0:9])

with open(out_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(out_data)

print(f"wrote {out_file}")
