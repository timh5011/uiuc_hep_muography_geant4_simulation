import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot total light yield per event for each detector.")
parser.add_argument("csv_file", help="Path to the CSV file containing the data.")
parser.add_argument("output_csv", help="Path to the output CSV file to save histogram data.")
args = parser.parse_args()

# Read the CSV file, skip the first 8 header lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Rename columns for clarity
df.columns = ['eventId', 'copyNo', 'light_yield', 'fT']  # Changed 'energy' to 'light_yield'

# Create a dictionary to store the total light yield (photon count) per event for each detector
total_light_yield_per_event = {0: {}, 1: {}, 2: {}, 3: {}}

# Create a dictionary to store photon hits over time for each detector
photon_hits_time = {0: [], 1: [], 2: [], 3: []}

# Iterate over the DataFrame rows
for index, row in df.iterrows():
    eventId = row['eventId']
    copyNo = row['copyNo']
    light_yield = row['light_yield']  # Using light yield (photon count)
    time = row['fT']
    
    # Sum the light yield for each event for the corresponding detector
    if eventId in total_light_yield_per_event[copyNo]:
        total_light_yield_per_event[copyNo][eventId] += light_yield
    else:
        total_light_yield_per_event[copyNo][eventId] = light_yield

    # Add the time to photon hits per detector
    photon_hits_time[copyNo].append(time)

# Plot the histograms for each detector
plt.figure(figsize=(12, 10))

# Plot individual detector histograms (Top row)
for i in range(4):
    plt.subplot(4, 2, i * 2 + 1)  # Adjusting the subplot index
    plt.hist(total_light_yield_per_event[i].values(), bins=30, edgecolor='black')
    plt.title(f'Total Light Yield for SiPM {i}')
    plt.xlabel('Total Light Yield per Event (Photon Count)')
    plt.ylabel('Frequency')

# Plot photon strikes over time for each detector (Bottom row)
'''
for i in range(4):
    plt.subplot(4, 2, i * 2 + 2)  # Adjusting the subplot index
    plt.hist(photon_hits_time[i], bins=50, edgecolor='black')  # Adjust bin size as needed
    plt.title(f'Photon Hits Over Time for single SiPM')
    plt.xlabel('Time (ns)')
    plt.ylabel('Number of Photon Hits')
'''

# Plot photon strikes over time for each detector (Bottom row)
for i in range(4):
    plt.subplot(4, 2, i * 2 + 2)  # Adjusting the subplot index
    plt.hist(photon_hits_time[i], bins=50, weights=[1/1000] * len(photon_hits_time[i]), edgecolor='black')  # Scale by 1/500
    plt.title(f'Average Photon Hits Over Time for single SiPM')
    plt.xlabel('Time (ns)')
    plt.ylabel('Photon Hits (scaled)')

plt.tight_layout()
plt.show()


# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('total_light_yield_histograms_with_time.png')

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['EventId', 'Detector0', 'Detector1', 'Detector2', 'Detector3'])
    for eventId in total_light_yield_per_event[0].keys():
        row = [
            eventId,
            total_light_yield_per_event[0].get(eventId, 0),
            total_light_yield_per_event[1].get(eventId, 0),
            total_light_yield_per_event[2].get(eventId, 0),
            total_light_yield_per_event[3].get(eventId, 0)
        ]
        writer.writerow(row)

plt.show()
