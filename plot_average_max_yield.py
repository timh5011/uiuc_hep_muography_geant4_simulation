import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np
from collections import defaultdict

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot photon yields per SiPM ranked by number of photon hits per event.")
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

# Dictionary to store photon hits per event per detector
photon_hits_per_event = defaultdict(lambda: [0, 0, 0, 0])  # Initialize with 0 for each of 4 SiPMs (0, 1, 2, 3)

# Group by eventId and copyNo, summing the photon counts for each detector
grouped = df.groupby(['eventId', 'copyNo']).size()

# Populate the dictionary
for (eventId, copyNo), count in grouped.items():
    photon_hits_per_event[eventId][copyNo] = count

# Prepare lists for the histograms
histogram_data = [[], [], [], []]  # For 1st, 2nd, 3rd, and 4th highest SiPM yields

# Process each event
for event_hits in photon_hits_per_event.values():
    # Ensure the data is in list format and sorted
    sorted_hits = sorted(event_hits, reverse=True)
    for i in range(4):  # Assign each rank's yield to the appropriate histogram
        histogram_data[i].append(sorted_hits[i])

# Create histograms for the 4 plots
fig, axs = plt.subplots(2, 2, figsize=(14, 12))
titles = [
    f"Photon Yield between {args.time_lower}ns and {args.time_upper}ns of SiPM with Maximum Photon Yield",
    f"Photon Yield between {args.time_lower}ns and {args.time_upper}ns of SiPM with 2nd Largest Photon Yield",
    f"Photon Yield between {args.time_lower}ns and {args.time_upper}ns of SiPM with 3rd Largest Photon Yield",
    f"Photon Yield between {args.time_lower}ns and {args.time_upper}ns of SiPM with Minimum Photon Yield)",
]

# Define custom bins with an overflow bin for values above 200
bins = list(range(0, 201, 5)) + [float('inf')]

# Loop over histograms
for i, ax in enumerate(axs.flat):
    # Calculate histogram and handle overflow explicitly
    counts, edges = np.histogram(histogram_data[i], bins=bins)
    ax.bar(edges[:-1], counts, width=5, align='edge', edgecolor='black')
    
    # Replace the last bin label with '200+'
    xticks_labels = list(range(0, 201, 25)) + ['200+']  # Tick marks every 25 units, label overflow
    xticks_positions = list(range(0, 201, 25)) + [200]
    ax.set_xticks(xticks_positions)
    ax.set_xticklabels(xticks_labels)

    # Plot aesthetics
    ax.set_title(titles[i])
    ax.set_xlabel("Light Yield (Highest bin contains overflow)")
    ax.set_ylabel("Frequency")

    # Calculate statistics
    mean_hits = np.mean(histogram_data[i])
    median_hits = np.median(histogram_data[i])
    overflow_count = counts[-1]

    # Add statistics as text box
    ax.text(
        0.98, 0.95,
        f"Mean: {mean_hits:.2f}\nMedian: {median_hits:.2f}\nOverflow: {overflow_count}",
        transform=ax.transAxes,
        fontsize=10,
        ha='right',
        va='top',
        bbox=dict(boxstyle="round", edgecolor="black", facecolor="white")
    )

# Adjust layout and save the figure
plt.tight_layout()
plt.subplots_adjust(hspace=0.3, wspace=0.2)  # Adjust spacing between plots
plt.savefig("photon_yield_ranked_histograms.png")

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["EventId", "1stLargest", "2ndLargest", "3rdLargest", "4thLargest"])
    for eventId, hits in photon_hits_per_event.items():
        sorted_hits = sorted(hits, reverse=True)
        writer.writerow([eventId] + sorted_hits)

plt.show()
