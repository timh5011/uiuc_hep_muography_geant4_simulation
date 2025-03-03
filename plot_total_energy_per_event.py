import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np

# python plot_total_energy_per_event.py build/10000EVENTS_FIBERS_HITS_output_nt_Hits\ copy.csv data/output_events_hist.csv

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
total_light_yield_per_event = {0: {}, 1: {}}

# Create a dictionary to store photon hits over time for each detector
photon_hits_time = {0: [], 1: []}

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
overflow_threshold = 10100
for i in range(2):
    plt.subplot(2, 2, i * 2 + 1)  # Adjusting the subplot index
    values = list(total_light_yield_per_event[i].values())
    values_with_overflow = [v if v <= overflow_threshold else overflow_threshold for v in values]
    mean_value = np.mean(values)
    variance_value = np.var(values)
    plt.hist(values_with_overflow, bins=30, edgecolor='black', range=(min(values_with_overflow), overflow_threshold + 500))
    plt.axvline(x=overflow_threshold, color='red', linestyle='dashed', label='Overflow Bin')
    plt.axvline(x=mean_value, color='blue', linestyle='dashed', label=f'Mean: {mean_value:.2f}')
    plt.legend()
    plt.title(f'Total Light Yield for Fiber {i}\nMean: {mean_value:.2f}, Variance: {variance_value:.2f}')
    plt.xlabel('Total Light Yield per Event (Photon Count)')
    plt.ylabel('Frequency')

# Plot photon strikes over time for each detector (Bottom row)
for i in range(2):
    plt.subplot(2, 2, i * 2 + 2)  # Adjusting the subplot index
    mean_time = np.mean(photon_hits_time[i])
    variance_time = np.var(photon_hits_time[i])
    plt.hist(photon_hits_time[i], bins=50, weights=[1/10000] * len(photon_hits_time[i]), edgecolor='black')  # Scale by 1/(number of events)
    plt.axvline(x=mean_time, color='blue', linestyle='dashed', label=f'Mean: {mean_time:.2f}')
    plt.legend()
    plt.title(f'Average Photon Hits Over Time for Fiber {i}\nMean: {mean_time:.2f}, Variance: {variance_time:.2f}')
    plt.xlabel('Time (ns)')
    plt.ylabel('Photon Hits (scaled)')

plt.tight_layout()
plt.show()

# Save the plot
plt.savefig('total_light_yield_histograms_with_time.png')

# Save histogram data to CSV
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['EventId', 'Detector0', 'Detector1'])
    for eventId in total_light_yield_per_event[0].keys():
        row = [
            eventId,
            total_light_yield_per_event[0].get(eventId, 0),
            total_light_yield_per_event[1].get(eventId, 0)
        ]
        writer.writerow(row)

plt.show()
