cmake_minimum_required(VERSION 3.16)

project(Simulation_BC408)

##

option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

##

include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)

##

file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

# add_subdirectory(OPSim)
# add_subdirectory(sslg4)

##

add_executable(sim_bc408_1 sim_bc408_1.cc ${sources} ${headers})
target_link_libraries(sim_bc408_1 ${Geant4_LIBRARIES})

# target_link_libraries(sim_bc408_1 OPSim sslg4 ${Geant4_LIBRARIES} )

##

add_custom_target(Simulation1 DEPENDS sim_bc408_1)

