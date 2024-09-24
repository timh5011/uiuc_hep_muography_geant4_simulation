import pandas as pd
import matplotlib.pyplot as plt
import argparse
import csv

# Step 1: Set up argument parsing
parser = argparse.ArgumentParser(description='Sum photon energies per event and create a histogram.')
parser.add_argument('csv_file', type=str, help='Path to the CSV file')
parser.add_argument('output_file', type=str, help='Path to the output CSV file for histogram data')

args = parser.parse_args()

# Step 2: Load the CSV file, skipping the first 8 lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Step 3: Sum the energies for each event (group by eventId)
event_energy_sums = df.groupby(0)[2].sum()

# Step 4: Create the histogram
plt.figure(figsize=(10, 6))  # Set figure size
plt.hist(event_energy_sums, bins=30, color='blue', alpha=0.7, edgecolor='black')

# Step 5: Add labels and title
plt.xlabel('Total Energy per Event (eV)')  # X-axis label
plt.ylabel('Frequency')  # Y-axis label
plt.title('Histogram of Total Energy Striking any of the Four SiPMs per Event (eV)')  # Title of the histogram
plt.grid(axis='y', alpha=0.75)

# Step 6: Show the plot
plt.show()

# Step 7: Save histogram data into CSV
# Save event id and corresponding total energy for each event
event_energy_sums.to_csv(args.output_file, header=['Total Energy'], index_label='Event ID')

print(f"Histogram data saved to {args.output_file}")
