import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot maximum light yield per event within a specified time interval.")
parser.add_argument("csv_file", help="Path to the CSV file containing the data.")
parser.add_argument("output_csv", help="Path to the output CSV file to save histogram data.")
parser.add_argument("time_lower", type=float, help="Lower bound of the time interval.")
parser.add_argument("time_upper", type=float, help="Upper bound of the time interval.")
args = parser.parse_args()

# Read the CSV file, skip the first 8 header lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Rename columns for clarity
df.columns = ['eventId', 'copyNo', 'energy', 'fT']

# Filter for the time interval
df = df[(df['fT'] >= args.time_lower) & (df['fT'] <= args.time_upper)]

# Dictionary to store the photon hits per event per detector
photon_hits_per_event = {}

# Group by eventId and copyNo to count the number of hits per detector for each event
grouped = df.groupby(['eventId', 'copyNo']).size()

# Iterate through each event to find the max photon hits for each
for eventId, group in grouped.groupby(level=0):
    max_hits = group.max()
    photon_hits_per_event[eventId] = max_hits

# Create histogram data and set overflow bin for values above 500
max_photon_hits = list(photon_hits_per_event.values())
plt.hist(max_photon_hits, bins=list(range(0, 501, 10)) + [float('inf')], edgecolor='black')
plt.xlabel("Maximum Photon Hits (Light Yield) per Event for a Single SiPM (Highest bin contains overflow)")
plt.ylabel("Frequency")
plt.title("Max Photon Hits for SiPM with Highest Yield per Event")

# Save the histogram plot
plt.savefig("max_light_yield_histogram.png")

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["EventId", "MaxPhotonHits"])
    for eventId, max_hits in photon_hits_per_event.items():
        writer.writerow([eventId, max_hits])

plt.show()
