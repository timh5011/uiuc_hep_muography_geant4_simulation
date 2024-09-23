import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Step 1: Set up argument parsing
parser = argparse.ArgumentParser(description='Sum photon energies per event and create a histogram.')
parser.add_argument('csv_file', type=str, help='Path to the CSV file')

args = parser.parse_args()

# Step 2: Load the CSV file, skipping the first 8 lines
df = pd.read_csv(args.csv_file, header=None, skiprows=8)

# Step 3: Sum the energies for each event (group by eventId)
event_energy_sums = df.groupby(0)[2].sum()

# Step 4: Create the histogram
plt.figure(figsize=(10, 6))  # Set figure size
plt.hist(event_energy_sums, bins=30, color='blue', alpha=0.7, edgecolor='black')

# Step 5: Add labels and title
plt.xlabel('Total Energy on SiPM per Event (eV)')  # X-axis label
plt.ylabel('Frequency')  # Y-axis label
plt.title('Histogram of Total Energy per Event')  # Title of the histogram
plt.grid(axis='y', alpha=0.75)

# Step 6: Show the plot
plt.show()
