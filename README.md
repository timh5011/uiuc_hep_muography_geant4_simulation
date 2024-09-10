# Geant 4 Simulation of Plastic Scintillator BC408 for HEP Muography Group at UIUC

We simulate the passage of a 100 GeV positive muon through a volume of BC408 and collect scintillation photon hits with four sensitive detectors, to be read out into ROOT histograms for analysis.

## Table of Contents
- [Installation](#installation)

## Installation

Must have Geant4 source code installed. 
*    1. Clone the repository
*    2. Navigate to build folder and run cmake ..
*    2. Run make from build folder
*    3. Run Executable: ./sim_bc408_1
*    4. After running events, hits will be stored in output.root file in base directory. To access these, run root output.root and open a new TBRowser