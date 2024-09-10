#ifndef DETECTOR_HH
#define DETECTOR_HH

#include "G4VSensitiveDetector.hh"
#include "G4OpticalPhoton.hh"
#include "G4VProcess.hh"
#include "G4SystemOfUnits.hh"
#include "G4AnalysisManager.hh"
#include "G4RunManager.hh"



class MySensitiveDetector : public G4VSensitiveDetector {
    public:
        MySensitiveDetector(G4String);
        ~MySensitiveDetector();
        
        virtual G4bool ProcessHits(G4Step *, G4TouchableHistory *);

        void ResetTotalDepositedEnergyDetector();
        G4double GetTotalDepositedEnergyDetector() const;

        void ResetTotalDepositedLightYieldDetector();
        G4double GetTotalDepositedLightYieldDetector() const;
    private:
        G4double totalEnergyDepositDetector;
        G4double totalLightYieldDetector;
};

#endif