#include "Action.hh"

MyActionInitialization::MyActionInitialization() {}

MyActionInitialization::~MyActionInitialization() {}

void MyActionInitialization::Build() const {

    MyPrimaryGenerator *generator = new MyPrimaryGenerator();
    MySteppingAction* steppingAction = new MySteppingAction();
    MySensitiveDetector* sensitiveDetector = new MySensitiveDetector("MySensitiveDetector");
    MyEventAction* eventAction = new MyEventAction(steppingAction, sensitiveDetector);
    MyRunAction* runAction = new MyRunAction();

    SetUserAction(generator);
    SetUserAction(steppingAction);
    SetUserAction(eventAction);
    SetUserAction(runAction);

}