#include "EventAction.hh"

MyEventAction::MyEventAction(MySteppingAction* steppingAction, MySensitiveDetector* sensitiveDetector)
    : fSteppingAction(steppingAction), fSensitiveDetector(sensitiveDetector)
{}

MyEventAction::~MyEventAction() {}

// Called at the beginning of each event
void MyEventAction::BeginOfEventAction(const G4Event* event)
{
    // Reset the total optical photon energy at the beginning of each event
    fSteppingAction->ResetTotalOpticalPhotonEnergy();
    fSteppingAction->ResetTotalLightYield();
    fSteppingAction->ResetTotalDepositedEnergy();

    fSensitiveDetector->ResetTotalDepositedEnergyDetector();
}

// Called at the end of each event
void MyEventAction::EndOfEventAction(const G4Event* event)
{
    // ::::::::::::::::::::::: Values from Stepping Action :::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    // Get and print the total optical photon energy accumulated during the event
    G4double totalEnergy = fSteppingAction->GetTotalOpticalPhotonEnergy();
    // G4cout << "Total scintillation photon energy for this event: "
    //        << totalEnergy * MeV << " MeV" << G4endl; // divide or multiply by MeV?
     
    // Get and print the total light yield during the event
    G4double totalYield = fSteppingAction->GetTotalLightYield();
    // G4cout << "Total light yield for this event: "
    //        << totalYield << " scintillation photons were emitted." <<G4endl;
    
    // Check results with Birk's Law Prediction:
    G4double totalDeposited = fSteppingAction->GetTotalDepositedEnergy();

    // Convert the total light yield to the light yield per unit energy deposited:
    // G4cout << "Light yield per MeV for this event: "
    //        << totalYield/totalDeposited << G4endl;

    // Get and print total muon deposited energy
    // G4cout << "Total energy deposited by the muon for this event: " 
    //       << totalDeposited * MeV << "MeV" << G4endl;

    // ::::::::::::::::::::::: Values from Sensitive Detector :::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    G4double totalDepositedInDetector = fSensitiveDetector->GetTotalDepositedEnergyDetector();

    // ::::::::::::::::::::::: Store Deposited Energy in ROOT Ntuple :::::::::::::::::::::::::::::::::::::::::::::::::::

    G4int evt = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();

    G4AnalysisManager *manager = G4AnalysisManager::Instance();
    manager->FillNtupleIColumn(0, evt);
    manager->FillNtupleDColumn(1, totalDepositedInDetector);
    manager->AddNtupleRow(0);

}