# Geant4 Simulation of Plastic Scintillator BC408 for HEP Muography Group at UIUC and Occidental College

We simulate the passage of a 100 GeV positive muon through a volume of BC408 and collect scintillation photon hits on wavelength shifting fibers (which channel the re-emitted photons into SiPMs), to be read out into a CSV file and a ROOT file for analysis. Analysis focuses on the spatial and temporal distribution of the scintillation light yield. Scintillation light yield has been validated against the expected theoretical quantity predicted by Bethe-Bloch and Birks' Law.

## Table of Contents
- [Installation and Use](#installation-and-use)
- [Post-Analysis Scripts](#post-analysis-scripts)
- [Simulation Architecture](#simulation-architecture)
- [Directory Structure](#directory-structure)
- [Theoretical Validation of Simulation Results](#theoretical-validation-of-simulation-results)

## Installation and Use

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
4. Run Executable: ./sim_bc408_1
```
./sim_bc408_1
```
5. After running events, hits will be stored in a CSV file in the build directory: `output_nt_Hits.csv`. You can then use the post-analysis scripts to generate plots (see below).

The hits are also stored in `output.root` in the build directory. To access these, run root and open a TBrowser:
```
root output.root
new TBrowser
```

## Post-Analysis Scripts

All analysis scripts live in `post-analysis-scripts/` and save their output plots to `plots/`.

### plot_total_energy_per_event.py

Generates histograms of total light yield per event for each fiber detector, plus temporal distributions of photon hits.

```
cd post-analysis-scripts
python plot_total_energy_per_event.py <csv_file> <output_csv>
```

**Arguments:**
- `csv_file` — Path to the hits CSV (e.g. `../build/output_nt_Hits.csv`)
- `output_csv` — Path to save per-event yield data (e.g. `../data/output_events_hist.csv`)

**Example:**
```
python plot_total_energy_per_event.py ../build/output_nt_Hits.csv ../data/output_events_hist.csv
```

**Output:** `plots/total_light_yield_histograms_with_time.png`

### plot_average_max_yield.py

Ranks SiPM photon yields by magnitude for each event and creates comparative histograms (1st, 2nd, 3rd, 4th highest yield).

```
cd post-analysis-scripts
python plot_average_max_yield.py <csv_file> <output_csv> <time_lower> <time_upper>
```

**Arguments:**
- `csv_file` — Path to the hits CSV (e.g. `../build/output_nt_Hits.csv`)
- `output_csv` — Path to save ranked yield data (e.g. `../data/average_max_yield_entries.csv`)
- `time_lower` — Lower bound of the time window (ns)
- `time_upper` — Upper bound of the time window (ns)

**Example:**
```
python plot_average_max_yield.py ../build/output_nt_Hits.csv ../data/average_max_yield_entries.csv 2 12
```

**Output:** `plots/photon_yield_ranked_histograms.png`

### plot_reflectivity_yield.py

Generates a bar chart of mirror reflectivity vs. median light yield from a summary CSV.

```
cd post-analysis-scripts
python plot_reflectivity_yield.py <csv_file>
```

**Arguments:**
- `csv_file` — Path to a CSV with `Reflectivity` and `YieldMedian` columns (e.g. `../data/reflectivity_yield_median.csv`)

**Example:**
```
python plot_reflectivity_yield.py ../data/reflectivity_yield_median.csv
```

**Output:** Displayed interactively (no file saved).

## Simulation Architecture

### Data Flow

```
MyPrimaryGenerator (100 GeV mu+)
        |
        v
MyDetectorConstruction (BC408 scintillator bar + WLS fibers)
        |
        v  (muon traverses scintillator, producing optical photons)
MySteppingAction (accumulates scintillation photon count & muon dE/dx)
        |
        v
MySensitiveDetector (processes photon hits on fibers, writes per-hit data to CSV)
        |
        v
MyEventAction (resets counters at event start, aggregates & prints per-event stats)
        |
        v
MyRunAction (manages CSV/ROOT file I/O)
        |
        v
Post-analysis Python scripts (read CSV, generate plots)
```

### Components

| Component | Files | Description |
|---|---|---|
| **Action** | `Action.hh/cc` | Orchestrates initialization of all user action classes. Instantiates and registers the generator, stepping action, detector, event action, and run action. |
| **Generator** | `Generator.hh/cc` | Defines the particle gun. Shoots 100 GeV positive muons at random (x, y) positions within the scintillator volume, directed along +Z. |
| **Physics** | `Physics.hh/cc` | Defines the physics list (FTFP_BERT base). Registers `G4EmStandardPhysics`, `G4OpticalPhysics`, and `G4DecayPhysics`. |
| **Detector Construction** | `DetectorConstruction.hh/cc` | Builds the geometry: world volume (3m air cube), BC408 scintillator bar (1.857m x 5cm x 1cm), two wavelength-shifting fibers (0.5mm radius), and a mirror optical surface (95% reflectivity). Defines BC408 material properties (refractive index, absorption length, scintillation yield of 10,000 photons/MeV). |
| **Stepping Action** | `SteppingAction.hh/cc` | Called at every simulation step. Identifies scintillation photons among secondaries and accumulates photon energy, photon count, and muon energy deposition. |
| **Sensitive Detector** | `Detector.hh/cc` | Attached to the fiber logical volumes. Processes photon hits crossing into the fibers and writes per-hit data (event ID, detector copy number, light yield, time) to the CSV output. |
| **Event Action** | `EventAction.hh/cc` | Resets all counters at the beginning of each event. At event end, retrieves accumulated statistics from SteppingAction and the sensitive detector and prints a per-event summary. |
| **Run Action** | `RunAction.hh/cc` | Opens the CSV output file at run start (via `G4AnalysisManager`) and writes/closes it at run end. Defines the ntuple columns: `fEvent`, `copyNo`, `light_yield`, `fT`. |

## Directory Structure

```
.
├── CMakeLists.txt              # Build configuration
├── sim_bc408_1.cc              # Main entry point
├── include/                    # Header files (.hh)
├── src/                        # Source files (.cc)
├── build/                      # Build directory (generated)
├── data/                       # Output CSV data and reference figures
├── plots/                      # Generated plot images
└── post-analysis-scripts/      # Python analysis scripts
```

## Theoretical Validation of Simulation Results

### 1. Scintillation Light Yield of BC-408

#### 1.1 BC-408 Stopping Power from Bethe-Bloch Formula

The Bethe-Bloch equation tells us the average stopping power, $\frac{dE}{dx}$, of the material when some charged particle incident to the material travels through it. That is, it tells us the average total energy loss per unit distance, due to electromagnetic interactions.

These interactions are ionization and excitation. We use the Bethe-Bloch equation to calculate how much energy we expect a $100$ GeV positive muon to deposit into BC-408, after traveling $1.27$ cm through the plastic. Since BC-408 is 91.512% carbon, we approximate the calculation by treating it as only carbon, for simplicity. This is a reliable approximation because the stopping power of a material combines linearly in the atomic composition of the material.

$$
\begin{aligned}
-\frac{dE}{dx} & = Kz^2\frac{Z}{A}\frac{1}{\beta^2}\left[ \frac{1}{2}\ln{\frac{2m_ec^2\beta^2\gamma^2T_{max}}{I^2}}-\beta^2-\frac{\delta}{2} \right] \\
& = K\frac{6}{A}\frac{1}{\beta^2}\left[ \frac{1}{2}\ln{\frac{2(0.511\text{MeV})\beta^2\gamma^2T_{max}}{I^2}}-\beta^2-\frac{\delta}{2} \right]
\end{aligned}
$$

A positive muon has charge $z=1$ in electron charge units. A positive muon's rest mass $m_0=105.7$ MeV/$c^2$. Since we have 100 GeV muons, it follows that $\gamma^2 = 946$ and $\beta^2\approx 1$.

The mean ionization potential for carbon is $78$ eV. $T_{\text{max}}$ is the maximum kinetic energy transferred by the muon to a single free electron.

Using relativistic kinematics, we can find that this is:

$$
\frac{2m_e\beta^2\gamma^2}{1 + 2 \frac{m_e}{m_\mu} + \frac{m_e^2}{m_\mu^2}} = 90137.4 \text{ MeV}
$$

Finally, we have that $K=0.307075$ MeV g$^{-1}$ cm$^2$ for $A=1$ g mol$^{-1}$. Since the atomic mass of carbon is $12.01$ g mol$^{-1}$, we have $K/A=0.025589$ MeV g$^{-1}$ cm$^2$.

Thus,

$$
-\frac{dE}{dx} = \frac{K\cdot 6}{A}\left[ \frac{1}{2}\ln{\frac{2(0.511\text{MeV})(895,055)}{I}}-1-\frac{\delta}{2} \right]
$$

$$
-\frac{dE}{dx} = \frac{K\cdot 6}{A}\left[ \frac{1}{2}(23.185)-1-\frac{\delta}{2} \right]
$$

$$
-\frac{dE}{dx} = 6\cdot 0.025589\cdot\left[ \frac{1}{2}(30.237)-1-\frac{\delta}{2} \right]
$$

We then approximate this without the density effect correction, $\delta$, which is a good approximation at the energy levels we are concerned with, and get:

$$
-\frac{dE}{dx} = 6\cdot 0.025589\cdot\left[ \frac{1}{2}(30.237)-1\right] = 2.17 \text{ MeV cm}^{-1}.
$$

#### 1.2 Scintillation Yield from Birks' Law

The Bethe-Bloch equation tells us nothing about what happens to that energy after it is deposited into the material. This is what Birks' Law tells us.

Birks' law is an empirical equation for calculating the number of scintillation photons produced per unit length as a function of the energy loss per unit length. It is usually expressed as:

$$
\frac{dL}{dx} = S\frac{\frac{dE}{dx}}{1+kB\frac{dE}{dx}}
$$

* The constant $k$ is the probability of quenching.
* The constant $B$ is another constant of proportionality specific to the material.
* Together, $kB$ is referred to as Birks' coefficient, and has units of distance per energy.

Reference (3) gives that $kB=0.155$ mm/MeV, consistent with the fact that Polyvinyl toluenes have $0.126\leq kB\leq 0.207$ g MeV / cm$^2$.

$S$ is the scintillation efficiency, which is generally defined to be the number of scintillation photons produced per unit distance traversed by the incident particle. (In certain contexts, it is also sometimes defined as the percentage of deposited energy which is transformed into scintillation light, but not in the context of Birks' Law — we can see this by dimensional analysis of Birks' Law).

Using the result obtained from the Bethe-Bloch equation, we have an estimate for the total light yield through Birks' Law as follows:

$$
\begin{aligned}
\frac{dL}{dx} & = S\frac{\frac{dE}{dx}}{1+kB\frac{dE}{dx}} \\
& = S\frac{2}{1.031}  \\
& = 10,000\cdot1.94 \\
& = 19,398 \text{ photons cm}^{-1}.
\end{aligned}
$$
