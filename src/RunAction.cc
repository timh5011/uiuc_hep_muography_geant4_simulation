#include "RunAction.hh"

MyRunAction::MyRunAction() {}

MyRunAction::~MyRunAction() {}

void MyRunAction::BeginOfRunAction(const G4Run*) {
    
    G4AnalysisManager *manager = G4AnalysisManager::Instance();
    
    manager->OpenFile("output.root");

    manager->CreateH1("SiPMLightYield", "Total Photon Hits per Event", 100, 0, 20000);
    manager->CreateH1("SiPMEnergy", "Total Energy Deposited by Photons per Event", 100, 0, 100000/keV);  // Histogram ID = 1
    manager->CreateH1("TotalEnergy", "Total Energy of Photons per Event", 100, 0, 500/keV);
    
/*
    manager->CreateNtuple("Hits", "Hits");
    manager->CreateNtupleIColumn("fEvent");
    manager->CreateNtupleDColumn("fX");
    manager->CreateNtupleDColumn("fY");
    manager->CreateNtupleDColumn("fZ");
    manager->FinishNtuple(0);
*/

    //code for writing into csv file
    auto csvmanager{ G4CsvAnalysisManager::Instance() };
    csvmanager->OpenFile("output.csv");
    csvmanager->CreateNtuple("Hits", "Hits");
    csvmanager->CreateNtupleIColumn("fEvent");
    csvmanager->CreateNtupleDColumn("trackID");
    csvmanager->CreateNtupleDColumn("Energy");
    csvmanager->FinishNtuple(0);
}

void MyRunAction::EndOfRunAction(const G4Run*) {
    G4AnalysisManager *manager = G4AnalysisManager::Instance();

    manager->Write();
    manager->CloseFile();

    //code for writing into csv file
    auto csvmanager{ G4CsvAnalysisManager::Instance() };
    csvmanager->Write();
    csvmanager->CloseFile();
}
