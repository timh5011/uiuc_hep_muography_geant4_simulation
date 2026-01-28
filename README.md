# Geant4 Simulation of Plastic Scintillator BC408 for HEP Muography Group at UIUC and Occidental College

We simulate the passage of a 100 GeV positive muon through a volume of BC408 and collect scintillation photon hits on wavelength shifting fibers (which channel the re-emitted photons into SiPMs), to be read out into a CSV file and a ROOT file for analysis. Analysis focuses on the spatial and temporal distribution of the scintillation light yield. Scintillation light yield has been validated against the expected theoretical quantity predicted by Bethe-Bloch and Birks' Law.

## Table of Contents
- [Installation and Use](#installation)
- [Outline](#outline)

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


## 
# HEP Muography Update

**Author:** Tim Healy  
**Date:** 27 August 2024

## BC-408 Simulation

We fire a 100 GeV positive muon into a volume of the plastic scintillator BC-408 of dimensions $61\text{cm} \times 61\text{cm} \times 1.27\text{cm}$. The muon travels a distance of $1.27\text{cm}$ through the material. We are interested in learning the amount of scintillation light which is produced.

### BC408 Material construction in Geant4

BC408 is $91.512\%$ carbon and $8.488\%$ hydrogen **(2)**. We have also defined the following optical/scintillation properties:

For the photon energy spectrum we use wavelengths which are known to be common of scintillation photons emitted from BC-408 **(2)**: $\{470\text{nm}, 439\text{nm}, 425\text{nm}, 410\text{nm}\}$, giving energies: $\{2.640\text{eV}, 2.826\text{eV}, 2.919\text{eV}, 3.026\text{eV}\}$. These are in the blue-violet light range.

**Material Optical Properties:**

1. SCINTILLATIONCOMPONENT1 = $\{0.3, 0.739, 0.994, 0.378\}$ corresponding to the photon energies.
2. SCINTILLATIONCOMPONENT2 = $\{0.3, 0.739, 0.994, 0.378\}$ corresponding to the photon energies.
3. SCINTILLATIONCOMPONENT3 = $\{0.3, 0.739, 0.994, 0.378\}$ corresponding to the photon energies.
4. Refraction Index: RINDEX = 1.58
5. Absorption Length: ABSLENGTH = 380cm
6. SCINTILLATIONTIMECONSTANT1 = 2.1ns
7. SCINTILLATIONTIMECONSTANT2 = 2.1ns
8. SCINTILLATIONTIMECONSTANT3 = 2.1ns
9. SCINTILLATIONYIELD = 10,000 / MeV
10. SCINTILLATIONYIELD1 = 1.0
11. RESOLUTIONSCALE = 1.0
12. SCINTILLATIONRISETIME1 = 0.9ns

Implement SSGL4 and SimOp for accuracy improvement? These are scintillation material packages for Geant4.

## Theoretical Expectation Explanation

The Bethe-Bloch equation tells us the average stopping power, $\frac{dE}{dx}$, of the material when some particle incident to the material travels through it. That is, it tells us the average total energy loss per unit distance, due to electromagnetic interactions.

These interactions are ionization and excitation. We will use the Bethe-Bloch equation to calculate how much energy we expect a $100\text{GeV}$ positive muon to deposit into BC408, after travelling $1.27\text{cm}$ through the plastic. The Bethe-Bloch equation tells us nothing about what happens to that energy after it is deposited into the material.

This is what Birks' Law tells us. Birks law takes in the stopping power, $\frac{dE}{dx}$, of the material, as well as other constants of the material, and tells us the scintillation light yield per unit distance, $\frac{dL}{dx}$, which is defined to be the number of scintillation photons produced per unit distance.

That is, it takes in the energy which the muon deposited into the plastic, and tells us how many scintillation photons are produced. If we now want to know the total energy of the scintillation light, we can multiply the number of photons produced by the energy of a scintillation photon.

For BC408, we know that the most common wavelength of a scintillation photon is $425\text{nm}$, which will have energy $3\text{eV}$. This simple multiplication gives us an approximate answer of $73.9\text{keV}$. For a more accurate prediction, we can integrate over the distribution of scintillation energies.

### Bethe-Bloch Calculation

Since BC408 is $91.512\%$ carbon, I am approximating this calculation by treating it as only carbon, for simplicity.

$$
\begin{split}    
-\frac{dE}{dx} & = Kz^2\frac{Z}{A}\frac{1}{\beta^2}\left[ \frac{1}{2}\ln{\frac{2m_ec^2\beta^2\gamma^2T_{max}}{I^2}}-\beta^2-\frac{\delta}{2} \right] \\
& = K\frac{6}{A}\frac{1}{\beta^2}\left[ \frac{1}{2}\ln{\frac{2(0.511\text{MeV})\beta^2\gamma^2T_{max}}{I^2}}-\beta^2-\frac{\delta}{2} \right]
\end{split}
$$

A positive muon has charge $z=1$ in electron charge units. A positive muon's rest mass $m_0=105.7 \text{MeV}/c^2$. We have $100 \text{GeV}=\gamma m_0c^2$, thus $\gamma^2 = 946$ and $\beta^2\approx 1$.

Table 2.1 of "Intro to Experimental Particle Physics" by Richard Fernow tells us that the mean ionization potential for carbon is $78\text{eV}$. We approximate $T_{\text{max}}$ to be equal to $I$. This is supported by the form of Bethe-Bloch given in "Intro to Experimental Particle Physics" by Richard Fernow.

$$
\begin{split}
    -\frac{dE}{dx} & = \frac{K\cdot 6}{A}\left[ \frac{1}{2}\ln{\frac{2(0.511\text{MeV})(895,055)}{I}}-1-\frac{\delta}{2} \right]
\end{split}
$$

The logarithm evaluates to 23.185. Thus, 

$$
\begin{split}
    -\frac{dE}{dx} & = \frac{K\cdot 6}{A}\left[ \frac{1}{2}(23.185)-1-\frac{\delta}{2} \right]
\end{split}
$$

We have that $K=0.307075 \text{ MeV g}^{-1} \text{cm}^2$ for $A=1 \text{ g mol}^{-1}$. Since the atomic mass of carbon is $12.01 \text{ g mol}^{-1}$, we have $K/A=0.025589 \text{ MeV g}^{-1} \text{cm}^2$.

$$
\begin{split}
    -\frac{dE}{dx} & = 6\cdot 0.025589\cdot\left[ \frac{1}{2}(23.185)-1-\frac{\delta}{2} \right]
\end{split}
$$

We approximate this without the density effect correction, $\delta$, and get

$$-\frac{dE}{dx} = 6\cdot 0.025589\cdot\left[ \frac{1}{2}(23.185)-1\right] = 1.63 \text{ MeV cm}^{-2}.$$

### BC-408 Stopping Power

References **(4)** and **(5)** provide evidence that we can assume the stopping power of BC-408 for a 100 GeV positive muon is approximately $2 \text{ MeV/cm}$. Figure 27.3 of (PDG review of interaction of radiation and matter: [https://pdg.lbl.gov/2004/reviews/passagerpp.pdf](https://pdg.lbl.gov/2004/reviews/passagerpp.pdf)) gives evidence for this as well. That is, $\frac{dE}{dx}=2$.

Then $\int dE=\int 2dx$. Thus, we find that the energy deposited is expected to be $2\text{ MeV/cm}\cdot 1.27\text{ cm}=2.54 \text{ MeV}$.

### Birks' Law Prediction

The constant $k$ is probability of quenching. The constant $B$ is another constant of proportional which is specific to the material. Together, $kB$ is referred to as Birks' coefficient, and has units of distance per energy. Reference (3) gives that $kB=0.155 \text{ mm/MeV}$. This supports claim on wikipedia [https://en.wikipedia.org/wiki/Birks%27_law](https://en.wikipedia.org/wiki/Birks%27_law) that Polyvinyl toluenes have $0.126\leq kB\leq 0.207 \text{ g MeV / cm}^2$.

$S$ is the scintillation efficiency, which is generally define to be the number of scintillation photons produced per unit distance traversed by the incident particle. (In certain contexts, it is also sometimes defined as the percentage of deposited energy which is transformed into scintillation light, but not in the context of Birks' Law - we can see this by dimensional analysis of Birks' Law.)

$$
\begin{split}
\frac{dL}{dx} & = S\frac{\frac{dE}{dx}}{1+kB\frac{dE}{dx}} \\
& = S\frac{2}{1.031}  \\
& = 10,000\cdot1.94 \\
& = 19,398.
\end{split}
$$

Since $dx=1.27\text{cm}$, we have that, $dL=19,398\cdot 1.27\text{cm} = 27,636.3$ photons.

We can now multiply this by the most common energy of scintillation photons for BC408. A photon of wavelength $425\text{nm}$ has energy of about $3\text{eV}$. Thus, $27,636.3\cdot 3=73,908.8 \text{ eV}=73.9088 \text{ keV}$ is the expected total energy of the scintillation light.

### Dimensional Analysis of Birks' law

$$
\begin{split}
    \left[\frac{dL}{dx}\right] & = \left[S\frac{\frac{dE}{dx}}{1+kB\frac{dE}{dx}}\right] \\
    \frac{\text{number of photons produced}}{\text{unit distance traversed}} 
    & = [S]\left[\frac{\frac{\text{unit energy deposited}}{\text{unit distance traversed}}}{[1]+\left(\frac{\text{unit distance traversed}}{\text{unit energy deposited}}\right)\frac{\text{unit energy deposited}}{\text{unit distance traversed}}}\right] \\
    & = \frac{\text{number of photons produced}}{\text{unit energy deposited}}\left[\frac{\text{unit energy deposited}}{\text{unit distance traversed}}\right] \\
    & =  \frac{\text{number of photons produced}}{\text{unit distance traversed}}.
\end{split}
$$

## References

1. BC-408 Definition: [https://luxiumsolutions.com/radiation-detection-scintillators/plastic-scintillators/bc400-bc404-bc408-bc412-bc416](https://luxiumsolutions.com/radiation-detection-scintillators/plastic-scintillators/bc400-bc404-bc408-bc412-bc416)
2. BC-408 Definition: [https://neutrino.erciyes.edu.tr/SSLG4/](https://neutrino.erciyes.edu.tr/SSLG4/)
3. Birk's parameters for BC-408: [https://arxiv.org/pdf/2007.08366](https://arxiv.org/pdf/2007.08366)
4. BC-408 is a PVT (Polyvinyl toluene) based plastic: [https://iopscience.iop.org/article/10.1088/1757-899X/928/7/072134/pdf](https://iopscience.iop.org/article/10.1088/1757-899X/928/7/072134/pdf)
5. [https://www.physics.purdue.edu/~jones105/phys56400_Fall2018/lectures/Phys56400_Lecture6.pdf](https://www.physics.purdue.edu/~jones105/phys56400_Fall2018/lectures/Phys56400_Lecture6.pdf)
6. Birks' Law Parameters: [https://indico.cern.ch/event/316614/contributions/732033/attachments/608186/836893/birksdisc.pdf](https://indico.cern.ch/event/316614/contributions/732033/attachments/608186/836893/birksdisc.pdf)