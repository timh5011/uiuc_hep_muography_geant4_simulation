#include "Detector.hh"

MySensitiveDetector::MySensitiveDetector(G4String name)
     : G4VSensitiveDetector(name), totalEnergyDepositDetector(0.0), totalLightYieldDetector(0.0) {}

MySensitiveDetector::~MySensitiveDetector() {}

G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist) {
    
    // Access information about the particle which enters the sensitive detector
    G4Track *track = aStep->GetTrack();

    // track->SetTrackStatus(fStopAndKill); // If we only want to detect photons from one side of the detector ?
    G4StepPoint *preStepPoint = aStep->GetPreStepPoint();
    G4StepPoint *postStepPoint = aStep->GetPostStepPoint();

    // ::::::::::::: Do I want to measure from aStep, preStepPoint, or postStepPoint? :::::::::::::::::::::::::

    G4double edep = aStep->GetTrack()->GetKineticEnergy();
    edep = edep / eV;
    // G4cout << "Photon Energy:" << edep * MeV << G4endl;

    G4ThreeVector momPhoton = aStep->GetTrack()->GetMomentum();
    // G4cout << "Photon Momentum:" << momPhoton << G4endl;
    // G4cout << "Photon Momentum Magnitude:" << momPhoton.mag() * MeV  << G4endl;

    G4ThreeVector posPhoton = preStepPoint->GetPosition();
    //G4cout << "Photon Position: " << posPhoton << G4endl;

    // Get Time of Hit
    G4double fTime = preStepPoint->GetGlobalTime() / ns;

    //variables for CSV ntuples
    G4int trackID{ track->GetTrackID() };
    G4int event{ G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID() };
    track->SetTrackStatus(fStopAndKill);
    // ::::::::::::::::::::::::: Identify Creation Process of Photon: :::::::::::::::::::::::::::::::::::::::::::::::::

/*
    if (aStep->GetTrack()->GetParticleDefinition() == G4OpticalPhoton::OpticalPhotonDefinition()) {
        G4String creatorProcess = aStep->GetTrack()->GetCreatorProcess()->GetProcessName();
        if (creatorProcess == "Scintillation") {
            G4cout << "Scintillation photon detected by SiPM ==================================" << G4endl;
            G4cout << "Kinetic energy of single photon (edep): " << edep / eV << G4endl;
            totalEnergyDepositDetector += edep / eV;
            G4cout << "totalEnergyDepositDetector: "<< totalEnergyDepositDetector / eV << G4endl;
            totalLightYieldDetector++;
            G4cout << "totalLightYieldDetector: " << totalLightYieldDetector << G4endl;
        }
    }
*/

    /*

    if (aStep->GetTrack()->GetParticleDefinition() == G4OpticalPhoton::OpticalPhotonDefinition()) {
        G4String creatorProcess = aStep->GetTrack()->GetCreatorProcess()->GetProcessName();
        if (creatorProcess == "Cerenkov") {
            G4cout << "Cerenkov photon detected by SiPM." << G4endl;
        }
    }
    */

   // ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
   // ::::::::::::::::::::::::: Get sum of total energy deposited in sensitive detector ::::::::::::::::::::::::::::::::::
   // ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
   


    // ::::::::::::::::::::::::: Read Sensitive Detector Hits into ROOT Ntuple ::::::::::::::::::::::::::::::::::::::::::::::


    // const G4VTouchable *touchable = aStep->GetPreStepPoint()->GetTouchable();
    // G4VPhysicalVolume *physVol = touchable->GetVolume();
    // G4ThreeVector posDetector = physVol->GetTranslation();

/*
    G4AnalysisManager *manager = G4AnalysisManager::Instance();
    manager->FillNtupleIColumn(0, 0, event);
    manager->FillNtupleDColumn(0, 1, time);
    // manager->FillNtupleDColumn(1, posDetector[0]);
    // manager->FillNtupleDColumn(2, posDetector[1]);
    // manager->FillNtupleDColumn(3, posDetector[2]);
    manager->AddNtupleRow(0);
*/


    
 

    // G4cout << "Photon Position:" << posPhoton << G4endl;

    // Get copy number of detector which photon hit:
    const G4VTouchable *touchable = aStep->GetPreStepPoint()->GetTouchable();
    G4int copyNo = touchable->GetCopyNumber();

    // Get position of detector:
    // G4VPhysicalVolume *physVol = touchable->GetVolume();
    // G4ThreeVector posDetector = physVol->GetTranslation();


    // ::::::::::::::::::::::::: Read Sensitive Detector Hits into CSV Ntuples ::::::::::::::::::::::::::::::::::::::::::::::
    
    G4CsvAnalysisManager* csvmanager{ G4CsvAnalysisManager::Instance() };
    csvmanager->FillNtupleIColumn(0, event);
    csvmanager->FillNtupleDColumn(1, copyNo);
    csvmanager->FillNtupleDColumn(2, 1); // used to be edep, now just 1 for photon count
    csvmanager->FillNtupleDColumn(2, fTime);
    csvmanager->AddNtupleRow(0);
 
    return true;
}

G4double MySensitiveDetector::GetTotalDepositedEnergyDetector() 
{
    // G4cout << "GET TOTAL ENERGY METHOD WAS CALLED: "<< totalEnergyDepositDetector << G4endl;
    return totalEnergyDepositDetector;
}

void MySensitiveDetector::ResetTotalDepositedEnergyDetector() 
{
    totalEnergyDepositDetector = 0.0;
}

G4double MySensitiveDetector::GetTotalDepositedLightYieldDetector() 
{
    // G4cout << "GET TOTAL LIGHT YIELD METHOD WAS CALLED: "<< totalLightYieldDetector << G4endl;
    return totalLightYieldDetector;
}

void MySensitiveDetector::ResetTotalDepositedLightYieldDetector() 
{
    totalLightYieldDetector = 0.0;
}

