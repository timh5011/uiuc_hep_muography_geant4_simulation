#include "Generator.hh"

MyPrimaryGenerator::MyPrimaryGenerator() {
    fParticleGun = new G4ParticleGun(1);
}

MyPrimaryGenerator::~MyPrimaryGenerator() {
    delete fParticleGun;
}

void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent){
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition *particle = particleTable->FindParticle("mu+");

    G4double width = 1.875 * m;  // Example width
    G4double height = 5.0 * cm; // Example height

    // Generate random x and y coordinates within the scintillator volume
    G4double randomX = G4UniformRand() * width - (width / 2); // Centered at 0
    G4double randomY = G4UniformRand() * height - (height / 2); 

    G4ThreeVector pos(randomX, randomY, -40*cm); // Defines particle initial position
    G4ThreeVector mom(0.,0.,1.);// Defines particle initial momentum direction

    fParticleGun->SetParticlePosition(pos);
    fParticleGun->SetParticleMomentumDirection(mom);
    fParticleGun->SetParticleMomentum(100.*GeV);
    fParticleGun->SetParticleDefinition(particle);

    fParticleGun->GeneratePrimaryVertex(anEvent);
}