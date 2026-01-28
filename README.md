# Geant4 Simulation of Plastic Scintillator BC408 for HEP Muography Group at UIUC and Occidental College

We simulate the passage of a 100 GeV positive muon through a volume of BC408 and collect scintillation photon hits on wavelength shifting fibers (which channel the re-emitted photons into SiPMs), to be read out into a CSV file and a ROOT file for analysis. Analysis focuses on the spatial and temporal distribution of the scintillation light yield. Scintillation light yield has been validated against the expected theoretical quantity predicted by Bethe-Bloch and Birks' Law.

## Table of Contents
- [Installation and Use](#installation)
- [Outline](#outline)
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
3. Run Executable: ./sim_bc408_1
```
./sim_bc408_1
```
4. After running events, hits will be stored in a CSV file in the build directory: output_events_hist.csv. You can run python scripts to get plots of the light yields by running:
```
python plot_total_energy_per_event.py build/output_nt_Hits.csv data/output_events_hist.csv
python plot_average_max_yield.py build/output_nt_Hits.csv data/average_max_yield_entries.csv 2 12 
```

The hits are also stored in output.root file in build directory. To access these, run root output.root and open a new TBrowser.
```
root output.root
new TBrowser
```
## Outline

1. Action

2. Run Action 

3. Event Action

3. Stepping Action is called at every "step". A step is essentially increment of a particle trajectory.

4. Detector

5. Detector Construction

6. Physics defines the PhysicsList of the simulation. This is where we tell the simulation to include processes from G4EmStandardPhysics, G4OpticalPhysics, anf G4DecayPhysics.

7. Generator defines the particle gun. This is what shoots muons into the scintillating material. Here we specify the parameters of the incoming muons, such as position, energy, angle, etc.


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
-\frac{dE}{dx} = 6\cdot 0.025589\cdot\left[ \frac{1}{2}(30.237)-1\right] = 2.17 \text{ MeV cm}^{-2}.
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