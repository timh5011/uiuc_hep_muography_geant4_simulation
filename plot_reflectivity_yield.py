import pandas as pd
import matplotlib.pyplot as plt
import sys

# Check if the CSV file was passed as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py <csv_file>")
    sys.exit(1)

# Get the CSV file from the arguments
csv_file = sys.argv[1]

# Read the CSV file
data = pd.read_csv(csv_file)

# Extract the columns
reflectivity = data['Reflectivity']
yield_median = data['YieldMedian']

# Create the histogram
plt.bar(reflectivity, yield_median, width=0.05, color='blue', edgecolor='black')

# Add labels and title
plt.xlabel('Reflectivity')
plt.ylabel('Yield Median')
plt.title('Reflectivity vs Yield Median')

# Show the plot
plt.show()
