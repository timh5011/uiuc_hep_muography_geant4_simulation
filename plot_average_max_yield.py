import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv

# Parse command line arguments
parser = argparse.ArgumentParser(description="Plot maximum light yield for each event within a time interval.")
parser.add_argument("csv_file", help="Path to the CSV file containing the photon hit data.")
parser.add_argument("output_csv", help="Path to the output CSV file to save histogram data.")
parser.add_argument("lower_bound", type=float, help="Lower bound of the time interval (inclusive).")
parser.add_argument("upper_bound", type=float, help="Upper bound of the time interval (inclusive).")
args = parser.parse_args()

# Read the CSV file, skip the first 8 header lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Rename columns for clarity
df.columns = ['eventId', 'copyNo', 'light_yield', 'fT']  # Change 'energy' to 'light_yield' to represent photon hits

# Filter rows based on the time interval specified by the user
df_filtered = df[(df['fT'] >= args.lower_bound) & (df['fT'] <= args.upper_bound)]

# Initialize a dictionary to hold the maximum light yield per event
max_light_yield_per_event = {}

# Group by eventId and count hits per SiPM for each event within the time interval
for eventId, group in df_filtered.groupby('eventId'):
    # Count photon hits (light yield) per copyNo (SiPM) within the event
    light_yield_per_sipm = group['copyNo'].value_counts()
    
    # Find the maximum light yield (photon count) for this event
    max_light_yield = light_yield_per_sipm.max()
    
    # Store the maximum light yield for this event
    max_light_yield_per_event[eventId] = max_light_yield

# Plot the histogram of maximum light yields across events
plt.figure(figsize=(8, 6))
plt.hist(max_light_yield_per_event.values(), bins=30, edgecolor='black')
plt.title('Maximum Light Yield per Event in Time Interval')
plt.xlabel('Light Yield (Photon Hits)')
plt.ylabel('Frequency')
plt.tight_layout()

# Save and show the plot
plt.savefig('max_light_yield_histogram.png')
plt.show()

# Write the histogram data to a new CSV file
with open(args.output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['EventId', 'MaxLightYield'])
    for eventId, max_light_yield in max_light_yield_per_event.items():
        writer.writerow([eventId, max_light_yield])

print(f"Histogram data saved to {args.output_csv}")
