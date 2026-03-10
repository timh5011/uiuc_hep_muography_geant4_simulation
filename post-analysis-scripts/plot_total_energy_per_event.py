import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv
import numpy as np
import os

# python plot_total_energy_per_event.py ../build/10000EVENTS_FIBERS_HITS_output_nt_Hits\ copy.csv ../data/output_events_hist.csv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(SCRIPT_DIR, '..', 'plots')

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot total light yield per event for each detector.")
parser.add_argument("csv_file", help="Path to the CSV file containing the data.")
parser.add_argument("output_csv", help="Path to the output CSV file to save histogram data.")
args = parser.parse_args()

# Read the CSV file, skip the first 8 header lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Rename columns for clarity
df.columns = ['eventId', 'copyNo', 'light_yield', 'fT']  # Changed 'energy' to 'light_yield'

# Detect all unique detector IDs
detector_ids = sorted(df['copyNo'].unique())
num_detectors = len(detector_ids)

# Create a dictionary to store the total light yield (photon count) per event for each detector
total_light_yield_per_event = {d: {} for d in detector_ids}

# Create a dictionary to store photon hits over time for each detector
photon_hits_time = {d: [] for d in detector_ids}

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

# Determine the number of unique events for scaling
num_events = df['eventId'].nunique()

# Plot the histograms for each detector
nrows = num_detectors
ncols = 2
plt.figure(figsize=(12, 5 * nrows))

# Plot individual detector histograms (left column) and time distributions (right column)
overflow_threshold = 10100
for idx, d in enumerate(detector_ids):
    d_int = int(d)
    # Light yield histogram (left column)
    plt.subplot(nrows, ncols, idx * ncols + 1)
    values = list(total_light_yield_per_event[d].values())
    values_with_overflow = [v if v <= overflow_threshold else overflow_threshold for v in values]
    mean_value = np.mean(values)
    variance_value = np.var(values)
    plt.hist(values_with_overflow, bins=30, edgecolor='black', range=(min(values_with_overflow), overflow_threshold + 500))
    plt.axvline(x=overflow_threshold, color='red', linestyle='dashed', label='Overflow Bin')
    plt.axvline(x=mean_value, color='blue', linestyle='dashed', label=f'Mean: {mean_value:.2f}')
    plt.legend()
    plt.title(f'Total Light Yield for Fiber {d_int}\nMean: {mean_value:.2f}, Variance: {variance_value:.2f}')
    plt.xlabel('Total Light Yield per Event (Photon Count)')
    plt.ylabel('Frequency')

    # Photon hits over time (right column)
    plt.subplot(nrows, ncols, idx * ncols + 2)
    mean_time = np.mean(photon_hits_time[d])
    variance_time = np.var(photon_hits_time[d])
    plt.hist(photon_hits_time[d], bins=50, weights=[1/num_events] * len(photon_hits_time[d]), edgecolor='black')  # Scale by 1/(number of events)
    plt.axvline(x=mean_time, color='blue', linestyle='dashed', label=f'Mean: {mean_time:.2f}')
    plt.legend()
    plt.title(f'Average Photon Hits Over Time for Fiber {d_int}\nMean: {mean_time:.2f}, Variance: {variance_time:.2f}')
    plt.xlabel('Time (ns)')
    plt.ylabel('Photon Hits (scaled)')

plt.tight_layout()

# Save the plot
plt.savefig(os.path.join(PLOTS_DIR, 'total_light_yield_histograms_with_time.png'))
plt.show()

# Save histogram data to CSV
all_event_ids = sorted(set().union(*(total_light_yield_per_event[d].keys() for d in detector_ids)))
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['EventId'] + [f'Detector{int(d)}' for d in detector_ids])
    for eventId in all_event_ids:
        row = [eventId] + [total_light_yield_per_event[d].get(eventId, 0) for d in detector_ids]
        writer.writerow(row)
