#include "DetectorConstruction.hh"

MyDetectorConstruction::MyDetectorConstruction() {}

MyDetectorConstruction::~MyDetectorConstruction() {}

G4VPhysicalVolume *MyDetectorConstruction::Construct() {

    // Material |========================================================================================================

    // ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    // MATERIAL REFERENCES FOR BC-408/EJ-200: (NOT NECESSARILY IMPLEMENTED)
    // For Atomic Composition:
    // https://luxiumsolutions.com/radiation-detection-scintillators/plastic-scintillators/bc400-bc404-bc408-bc412-bc416
    // https://eljentechnology.com/products/plastic-scintillators/ej-200-ej-204-ej-208-ej-212
    // For Optical Properties:
    // BC408 Properties from https://github.com/alicelynch/PlasticScint_Fibre/blob/master/src/PSDetectorConstruction.cc
    // BC408 Properties from https://neutrino.erciyes.edu.tr/SSLG4/, which does not include optical properties (?)
    // ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    G4NistManager* nist = G4NistManager::Instance();

    // Elements |==========================================================================================================

    G4Element *C = nist->FindOrBuildElement("C");
    G4Element *H = nist->FindOrBuildElement("H");    

    G4double density;
    G4int nElem, nAtoms;
    
    // ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    density =1.023*g/cm3;
    G4Material* BC408 = new G4Material("BC408", density, nElem=2);

    BC408->AddElement(C, 91.512 * perCent);
    BC408->AddElement(H, 8.488 * perCent);
   
    // Units should be Atoms per cc (x10^22):
    // BC408->AddElement(H, nAtoms=523);
    // BC408->AddElement(C, nAtoms=474);

    G4double PhotonEnergy[4] = {2.640*eV, 2.826*eV, 2.919*eV, 3.026*eV}; // based on common wavelengths: {470*nm, 439*nm, 425*nm, 410*nm} 
    G4double rindex_bc408[4] = {1.58, 1.58, 1.58, 1.58};
    G4double abslength_bc408[4] = {380*cm, 380*cm, 380*cm, 380*cm}; // or {210*cm, 210*cm, 210*cm, 210*cm} ? 
    G4double scintcomp1[4] = {0.3, 0.739, 0.994, 0.378};
    G4double scintcomp2[4] = {0.3, 0.739, 0.994, 0.378}; // ?
    G4double scintcomp3[4] = {0.3, 0.739, 0.994, 0.378}; // ?

    G4MaterialPropertiesTable *BC408_mt = new G4MaterialPropertiesTable();

    BC408_mt->AddProperty("ABSLENGTH", PhotonEnergy, abslength_bc408, 4);
    BC408_mt->AddProperty("RINDEX", PhotonEnergy, rindex_bc408, 4);
    BC408_mt->AddProperty("SCINTILLATIONCOMPONENT1", PhotonEnergy, scintcomp1, 4);
    BC408_mt->AddProperty("SCINTILLATIONCOMPONENT2", PhotonEnergy, scintcomp2, 4);
    BC408_mt->AddProperty("SCINTILLATIONCOMPONENT3", PhotonEnergy, scintcomp3, 4);

    BC408_mt->AddConstProperty("SCINTILLATIONTIMECONSTANT1", 2.1*ns);
    BC408_mt->AddConstProperty("SCINTILLATIONTIMECONSTANT2", 2.1*ns); // ?
    BC408_mt->AddConstProperty("SCINTILLATIONTIMECONSTANT3", 2.1*ns); // ?
    BC408_mt->AddConstProperty("SCINTILLATIONYIELD", 10000./MeV);
    BC408_mt->AddConstProperty("SCINTILLATIONYIELD1", 1.0);
    // BC408_mt->AddConstProperty("SCINTILLATIONYIELD2", 1.0);
    // BC408_mt->AddConstProperty("SCINTILLATIONYIELD3", 0.1);
    BC408_mt->AddConstProperty("RESOLUTIONSCALE", 1.0);
    BC408_mt->AddConstProperty("SCINTILLATIONRISETIME1", 0.9*ns);
    // BC408_mt->AddConstProperty("SCINTILLATIONRISETIME2", 10);
    // BC408_mt->AddConstProperty("SCINTILLATIONRISETIME3", 20);


    BC408->SetMaterialPropertiesTable(BC408_mt);

    // Mirror Surface Boundary ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    G4double reflectivity[4] = {0.95, 0.95, 0.95, 0.95}; // {1.0, 1.0, 1.0, 1.0};
    
    mirrorSurface = new G4OpticalSurface("mirrorSurface");
    mirrorSurface->SetType(dielectric_metal);
    mirrorSurface->SetModel(unified);
    mirrorSurface->SetFinish(polished);

    G4MaterialPropertiesTable *mptMirror = new G4MaterialPropertiesTable();

    mptMirror->AddProperty("REFLECTIVITY", PhotonEnergy, reflectivity, 4);

    mirrorSurface->SetMaterialPropertiesTable(mptMirror);

    // Volumes |=========================================================================================================
    
    G4Material *scintMat = G4Material::GetMaterial("BC408");
    G4Material *worldMat = nist->FindOrBuildMaterial("G4_AIR");
    
    // Define Mother Volume :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    G4Box *solidWorld = new G4Box("solidWorld", 3*m, 3*m, 3*m);

    // Define Logical Volume
    G4LogicalVolume *logicWorld = new G4LogicalVolume(solidWorld, worldMat, "logicWorld");

    // Define Physical Volume
    G4VPhysicalVolume *physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "physWorld", 0, false, 0, true);


    // Define Scintillator Volume: :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    // Define World Volume
    G4Box *solidScint = new G4Box("solidScint", 30.5*cm, 30.5*cm, 0.635*cm);

    // Define Logical Volume
    G4LogicalVolume *logicScint = new G4LogicalVolume(solidScint, scintMat, "logicWorld");

    // Define Logical Reflecive Surface Boundary
    G4LogicalSkinSurface *skin = new G4LogicalSkinSurface("skin", logicScint, mirrorSurface);

    // Define Physical Volume
    G4VPhysicalVolume *physScint = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicScint, "physScint", logicWorld, false, 0, true);




    // Define Four Photon Detectors (in place of SiPMs) ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    G4Box *solidDetector = new G4Box("solidDetector", 3*mm, 3*mm, 1*mm);

    logicDetector = new G4LogicalVolume(solidDetector, scintMat, "logicDetector");

    for (G4int i = 0; i < 2; i++) {
        for (G4int j = 0; j < 2; j++) {
            G4VPhysicalVolume *physDetector = new G4PVPlacement(0, 
            G4ThreeVector(-15.25*cm+i*30.5*cm, -15.25*cm+j*30.5*cm, 0.535*cm), 
            logicDetector, "physDetector", logicScint, false, j+i*2, true);
        }
    }

    /*
    for (G4int i = 0; i < 50; i++) {
        for (G4int j = 0; j < 50; j++) {
            G4VPhysicalVolume *physDetector = new G4PVPlacement(0, 
            G4ThreeVector(-30.5*cm+(10*i+6*cm), -30.5*cm+(10*j+6*cm), 0.535*cm), 
            logicDetector, "physDetector", logicScint, false, j+i*20, true);
        }
    }
    */


    return physWorld;
}

// Implement Sensitive Detector and set equal to logicDetector

void MyDetectorConstruction::ConstructSDandField() {
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicDetector->SetSensitiveDetector(sensDet);
}