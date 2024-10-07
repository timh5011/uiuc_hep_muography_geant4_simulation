#ifndef PHYSICS_HH
#define PHYSICS_HH

#include "G4VModularPhysicsList.hh"
#include "G4EmStandardPhysics.hh"
#include "G4OpticalPhysics.hh"
#include "G4DecayPhysics.hh"
#include "FTFP_BERT.hh"
// #include "G4OpBoundaryProcess.hh"

// Not sure I need to explicitly register Scintillation Process. Don't think I do. 
#include "G4Scintillation.hh"
#include "G4OpticalPhoton.hh"
#include "G4MuonPlus.hh"

class MyPhysicsList : public FTFP_BERT {
    public:
        MyPhysicsList();
        ~MyPhysicsList();
};

#endif
