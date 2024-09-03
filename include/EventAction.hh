#ifndef MYEVENTACTION_H
#define MYEVENTACTION_H

#include "G4UserEventAction.hh"
#include "G4Event.hh"
#include "SteppingAction.hh"
#include "G4RunManager.hh"
#include "G4SystemOfUnits.hh"

class MyEventAction : public G4UserEventAction
{
public:
    // Constructor
    MyEventAction(MySteppingAction* steppingAction);

    // Destructor
    virtual ~MyEventAction();

    // Called at the beginning of each event
    virtual void BeginOfEventAction(const G4Event* event) override;

    // Called at the end of each event
    virtual void EndOfEventAction(const G4Event* event) override;

private:
    MySteppingAction* fSteppingAction;  // Pointer to the stepping action to access accumulated energy
};

#endif
