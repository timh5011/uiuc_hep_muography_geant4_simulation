# Geant4 Simulation of Plastic Scintillator BC408 for HEP Muography Group at UIUC and Occidental College

We simulate the passage of a 100 GeV positive muon through a volume of BC408 and collect scintillation photon hits with four sensitive detectors, to be read out into ROOT histograms and csv files for analysis. Scintillation light yield has been validated against the expected theoretical quantity predicted by Bethe-Bloch and Birks' Law.

## Table of Contents
- [Installation](#installation)

## Installation

Must have Geant4 source code installed. 
1. Clone the repository locally into same root directory as Geant4 source code
2. Create a build directory and navigate to it. Run cmake ..
```
mkdir build
cd build
cmake ..
```
3. Run make from build directory
```
make
```
3. Run Executable: ./sim_bc408_1
```
./sim_bc408_1
```
4. After running events, hits will be stored in output.root file in build directory. To access these, run root output.root and open a new TBrowser.
```
root output.root
new TBrowser
```
The hits are also stored in a CSV file in the build directory: output_events_hist.csv. You can run python scripts to get plots of the light yields by running:
```
python plot_total_energy_per_event.py build/output_nt_Hits.csv data/output_events_hist.csv
python plot_average_max_yield.py build/output_nt_Hits.csv data/average_max_yield_entries.csv 2 6 
```