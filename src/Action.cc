#include "Action.hh"

MyActionInitialization::MyActionInitialization() {}

MyActionInitialization::~MyActionInitialization() {}

void MyActionInitialization::Build() const {

    MyPrimaryGenerator *generator = new MyPrimaryGenerator();
    MySteppingAction* steppingAction = new MySteppingAction();
    MyEventAction* eventAction = new MyEventAction(steppingAction);
    MyRunAction* runAction = new MyRunAction();

    SetUserAction(generator);
    SetUserAction(steppingAction);
    SetUserAction(eventAction);
    SetUserAction(runAction);

}