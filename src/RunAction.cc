#include "RunAction.hh"

MyRunAction::MyRunAction() {}

MyRunAction::~MyRunAction() {}

void MyRunAction::BeginOfRunAction(const G4Run*) {
    
    G4AnalysisManager *manager = G4AnalysisManager::Instance();
    
    manager->OpenFile("output.root");
}

void MyRunAction::EndOfRunAction(const G4Run*) {
    G4AnalysisManager *manager = G4AnalysisManager::Instance();

    manager->Write();
    manager->CloseFile();
}
