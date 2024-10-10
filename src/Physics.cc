#include "Physics.hh"

MyPhysicsList::MyPhysicsList() {
    RegisterPhysics (new G4EmStandardPhysics());
    RegisterPhysics (new G4OpticalPhysics());
    RegisterPhysics (new G4DecayPhysics());
    // should i include G4OpBoundaryProcess.hh?
}

MyPhysicsList::~MyPhysicsList() {}
