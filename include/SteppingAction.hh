#ifndef STEPPINGACTION_HH
#define STEPPINGACTION_HH

#include "G4UserSteppingAction.hh"

#include "G4Track.hh"
#include "G4Step.hh"
#include "G4OpticalPhoton.hh"
#include "G4ProcessType.hh"
#include "G4Scintillation.hh"
#include "G4SystemOfUnits.hh"
#include "G4MuonPlus.hh"
// temporary:
#include "G4AnalysisManager.hh"
#include "G4RunManager.hh"

class MySteppingAction : public G4UserSteppingAction
{
  public:
    MySteppingAction();
    ~MySteppingAction() override;

    // method from the base class
    virtual void UserSteppingAction(const G4Step*) override;

    void ResetTotalOpticalPhotonEnergy();
    G4double GetTotalOpticalPhotonEnergy() const;

    void ResetTotalLightYield();
    G4double GetTotalLightYield() const;

    void ResetTotalDepositedEnergy();
    G4double GetTotalDepositedEnergy() const;

  private:
  G4double totalOpticalPhotonEnergy; 
  G4double totalLightYield; 
  G4double totalDepositedEnergy;

};

#endif