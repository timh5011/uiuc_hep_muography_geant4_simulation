'''
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np

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

# Create histogram data and set overflow bin for values above 200
max_photon_hits = list(photon_hits_per_event.values())
# Define custom bins with an overflow bin
bins = list(range(0, 201, 5)) + [float('inf')]  # Bins up to 200 with size 5, and one overflow bin

# Create the histogram
counts, edges = np.histogram(max_photon_hits, bins=bins)

# Adjust the last bin label for clarity
plt.bar(edges[:-1], counts, width=5, align='edge', edgecolor='black')

# Replace the last bin label with '200+'
xticks_labels = list(range(0, 201, 25)) + ['200+']  # Tick marks every 25 units, label overflow
xticks_positions = list(range(0, 201, 25)) + [200]

plt.xticks(ticks=xticks_positions, labels=xticks_labels)

plt.xlabel("Light Yield (Highest bin contains overflow)")
plt.ylabel("Frequency")
plt.title(f'Photon Hits from {args.time_lower} to {args.time_upper} for SiPM with Highest Yield per Muon')

# Calculate and display mean and median
mean_hits = np.mean(max_photon_hits)
median_hits = np.median(max_photon_hits)
plt.text(
    0.98, 0.95,
    f"Mean: {mean_hits:.2f}\nMedian: {median_hits:.2f}",
    transform=plt.gca().transAxes,
    fontsize=10,
    ha='right',
    va='top',
    bbox=dict(boxstyle="round", edgecolor="black", facecolor="white")
)

# Save the histogram plot
plt.savefig("max_light_yield_histogram.png")

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["EventId", "MaxPhotonHits"])
    for eventId, max_hits in photon_hits_per_event.items():
        writer.writerow([eventId, max_hits])
    writer.writerow([])  # Blank line
    writer.writerow(["Mean", mean_hits])
    writer.writerow(["Median", median_hits])

plt.show()
'''
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot photon yields per event for 1st, 2nd, 3rd, and lowest SiPM.")
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

# Iterate through each event to find the photon hits per detector
for eventId, group in grouped.groupby(level=0):
    # Create a list of hits for the SiPMs in this event (SiPMs are 1, 2, 3, 4)
    event_hits = [group.get(copyNo, 0) for copyNo in range(1, 5)]
    photon_hits_per_event[eventId] = event_hits

# Prepare lists for the highest, second highest, third highest, and lowest photon yields
highest_yields = []
second_highest_yields = []
third_highest_yields = []
lowest_yields = []

# Iterate over photon hits per event (each event has a list of SiPM yields)
for event_hits in photon_hits_per_event.values():
    # Ensure event_hits contains 4 values (pad with 0 if fewer than 4 SiPMs)
    while len(event_hits) < 4:
        event_hits.append(0)

    # Sort the yields in descending order
    event_hits_sorted = sorted(event_hits, reverse=True)

    # Append the corresponding photon yields to each list
    highest_yields.append(event_hits_sorted[0])
    second_highest_yields.append(event_hits_sorted[1])
    third_highest_yields.append(event_hits_sorted[2])
    lowest_yields.append(event_hits_sorted[3])  # This is now guaranteed to be the smallest (last) yield

# Create histograms for the photon yields of the 1st, 2nd, 3rd, and lowest SiPMs
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Define custom bins with an overflow bin for values above 200 and a bin size of 5
bins = list(range(0, 201, 5)) + [float('inf')]  # Bins up to 200 with size 5, and one overflow bin

# Plot for the highest yield (1st SiPM)
axs[0, 0].hist(highest_yields, bins=bins, edgecolor='black')
axs[0, 0].set_title('Highest Photon Yield per Event (SiPM 1st)')
axs[0, 0].set_xlabel('Light Yield (Highest bin contains overflow)')
axs[0, 0].set_ylabel('Frequency')
axs[0, 0].set_xticks(list(range(0, 201, 25)) + [200])
axs[0, 0].set_xticklabels(list(range(0, 201, 25)) + ['200+'])

# Plot for the second highest yield (2nd SiPM)
axs[0, 1].hist(second_highest_yields, bins=bins, edgecolor='black')
axs[0, 1].set_title('2nd Highest Photon Yield per Event (SiPM 2nd)')
axs[0, 1].set_xlabel('Light Yield (Highest bin contains overflow)')
axs[0, 1].set_ylabel('Frequency')
axs[0, 1].set_xticks(list(range(0, 201, 25)) + [200])
axs[0, 1].set_xticklabels(list(range(0, 201, 25)) + ['200+'])

# Plot for the third highest yield (3rd SiPM)
axs[1, 0].hist(third_highest_yields, bins=bins, edgecolor='black')
axs[1, 0].set_title('3rd Highest Photon Yield per Event (SiPM 3rd)')
axs[1, 0].set_xlabel('Light Yield (Highest bin contains overflow)')
axs[1, 0].set_ylabel('Frequency')
axs[1, 0].set_xticks(list(range(0, 201, 25)) + [200])
axs[1, 0].set_xticklabels(list(range(0, 201, 25)) + ['200+'])

# Plot for the lowest yield (4th SiPM)
axs[1, 1].hist(lowest_yields, bins=bins, edgecolor='black')
axs[1, 1].set_title('Lowest Photon Yield per Event (SiPM 4th)')
axs[1, 1].set_xlabel('Light Yield (Highest bin contains overflow)')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].set_xticks(list(range(0, 201, 25)) + [200])
axs[1, 1].set_xticklabels(list(range(0, 201, 25)) + ['200+'])

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("photon_yield_plots.png")

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["EventId", "HighestYield", "SecondHighestYield", "ThirdHighestYield", "LowestYield"])
    for eventId, hits in photon_hits_per_event.items():
        sorted_hits = sorted(hits, reverse=True)
        writer.writerow([eventId] + sorted_hits)

plt.show()
