#include "SteppingAction.hh"

MySteppingAction::MySteppingAction()
    : totalOpticalPhotonEnergy(0.0), totalLightYield(0.0), totalDepositedEnergy(0.0)
{}

MySteppingAction::~MySteppingAction() {}

void MySteppingAction::UserSteppingAction(const G4Step* step) {
    // Get all secondaries generated during this step
    const std::vector<const G4Track*>* secondaries = step->GetSecondaryInCurrentStep();

    // Loop over all secondaries
    for (auto secondary : *secondaries)
    {
        // Check if the secondary is an optical photon
        if (secondary->GetDefinition() == G4OpticalPhoton::OpticalPhotonDefinition())
        {
            // Check the creator process of the optical photon
            const G4VProcess* creatorProcess = secondary->GetCreatorProcess();

            if (creatorProcess && creatorProcess->GetProcessName() == "Scintillation")
            {
                // Accumulate the energy of optical photons created by scintillation
                G4double photonEnergy = secondary->GetKineticEnergy();
                totalOpticalPhotonEnergy += photonEnergy / MeV; // This used to be * MeV --- check this is correct
                totalLightYield += 1;
                // G4cout << "Scintillation Photon Energy: " << photonEnergy / eV << " eV" << G4endl;
            }
        }
    }
    /*
    if (totalOpticalPhotonEnergy != 0) { // I think I should only return this at end of event. Or this is what I should store in root.
        G4cout << "Total Scintillation Photon Energy: " << totalOpticalPhotonEnergy / eV << " eV" << G4endl;
    }
    */

    // Get the energy deposited in the current step ::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    G4double edep = step->GetTotalEnergyDeposit();

    // Only accumulate energy if it's a positive muon
    const G4ParticleDefinition* particleType = step->GetTrack()->GetParticleDefinition();
    if (particleType == G4MuonPlus::MuonPlusDefinition()) {
        totalDepositedEnergy += edep;
    }
}

// Method to reset the total optical photon energy at the beginning of each event
void MySteppingAction::ResetTotalOpticalPhotonEnergy()
{
    totalOpticalPhotonEnergy = 0.0;  // Reset to zero
}
// Method to get the total optical photon energy after the event
G4double MySteppingAction::GetTotalOpticalPhotonEnergy() const
{
    return totalOpticalPhotonEnergy;  // Return the accumulated value
}

void MySteppingAction::ResetTotalLightYield()
{
    totalLightYield = 0.0; // Reset to zero
}

G4double MySteppingAction::GetTotalLightYield() const
{
    return totalLightYield;  // Return the accumulated value
}

void MySteppingAction::ResetTotalDepositedEnergy()
{
    totalDepositedEnergy = 0.0; // Reset to zero
}

G4double MySteppingAction::GetTotalDepositedEnergy() const
{
    return totalDepositedEnergy;  // Return the accumulated value
}
