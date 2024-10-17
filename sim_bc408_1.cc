#include <iostream>

#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "G4VisManager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"

#include "DetectorConstruction.hh"
#include "Physics.hh"
#include "Action.hh"
#include "Detector.hh"

int main(int argc, char** argv) {
    G4RunManager *runManager = new G4RunManager();

    runManager->SetUserInitialization(new MyDetectorConstruction());
    runManager->SetUserInitialization(new MyPhysicsList());
    runManager->SetUserInitialization(new MyActionInitialization());

    runManager->Initialize();

    G4UIExecutive *ui =  new G4UIExecutive(argc, argv);

    G4VisManager *visManager = new G4VisExecutive();
    visManager->Initialize();

    G4UImanager *UImanager = G4UImanager::GetUIpointer();
    
    UImanager->ApplyCommand("/vis/open OGL");
    UImanager->ApplyCommand("/vis/viewer/set/viewpointVector 1 1 1");
    UImanager->ApplyCommand("/vis/drawVolume");
    UImanager->ApplyCommand("/vis/viewer/set/autoRefresh true");
    UImanager->ApplyCommand("/vis/scene/add/trajectories smooth");
    UImanager->ApplyCommand("/tracking/verbose 0");
    /*
    */

    //UImanager->ApplyCommand("/vis/scene/endOfEventAction accumulate");

    //UImanager->ApplyCommand("/vis/scene/add/trajectories optical");
    //UImanager->ApplyCommand("/vis/filtering/trajectories/OpticsFilter/active false");
    //UImanager->ApplyCommand("/process/optical/scintillation/setTrackSecondaries 1");
    //UImanager->ApplyCommand("/process/optical/setTrackStatus secondary");

    ui->SessionStart();

    return 0;
}
