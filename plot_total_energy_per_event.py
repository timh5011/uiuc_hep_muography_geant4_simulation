import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot total energy per event for each detector.")
parser.add_argument("csv_file", help="Path to the CSV file containing the data.")
parser.add_argument("output_csv", help="Path to the output CSV file to save histogram data.")
args = parser.parse_args()

# Read the CSV file, skip the first 8 header lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Rename columns for clarity
df.columns = ['eventId', 'copyNo', 'energy', 'fT'] # ADDED TIME COLUMN ONLY HERE

# Create a dictionary to store the total energy per event for each detector
total_energy_per_event = {0: {}, 1: {}, 2: {}, 3: {}}

# Create a dictionary to store the total energy across all detectors for each event
total_energy_all_detectors = {}

# Iterate over the DataFrame rows
for index, row in df.iterrows():
    eventId = row['eventId']
    copyNo = row['copyNo']
    energy = row['energy']
    
    # Sum the energy for each event for the corresponding detector
    if eventId in total_energy_per_event[copyNo]:
        total_energy_per_event[copyNo][eventId] += energy
    else:
        total_energy_per_event[copyNo][eventId] = energy

    # Also sum the energy across all detectors for each event
    if eventId in total_energy_all_detectors:
        total_energy_all_detectors[eventId] += energy
    else:
        total_energy_all_detectors[eventId] = energy

# Plot the histograms for each detector and for all detectors combined
plt.figure(figsize=(12, 8))

# Plot individual detector histograms
for i in range(4):
    plt.subplot(2, 3, i + 1)  # Arrange plots in a 2x3 grid
    plt.hist(total_energy_per_event[i].values(), bins=30, edgecolor='black')
    plt.title(f'Total Energy for Detector {i}')
    plt.xlabel('Total Energy per Event (eV)')
    plt.ylabel('Frequency')

# Plot the histogram for total energy across all detectors
plt.subplot(2, 3, 5)
plt.hist(total_energy_all_detectors.values(), bins=30, edgecolor='black')
plt.title('Total Energy for All Detectors')
plt.xlabel('Total Energy per Event (eV)')
plt.ylabel('Frequency')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('total_energy_histograms.png')

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['EventId', 'Detector0', 'Detector1', 'Detector2', 'Detector3', 'TotalEnergyAllDetectors'])
    for eventId in total_energy_all_detectors:
        row = [
            eventId,
            total_energy_per_event[0].get(eventId, 0),
            total_energy_per_event[1].get(eventId, 0),
            total_energy_per_event[2].get(eventId, 0),
            total_energy_per_event[3].get(eventId, 0),
            total_energy_all_detectors[eventId]
        ]
        writer.writerow(row)

plt.show()

