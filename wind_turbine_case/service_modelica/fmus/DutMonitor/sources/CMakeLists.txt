
cmake_minimum_required(VERSION 3.5)

set(FMU_NAME DutMonitor)

project(${FMU_NAME})

# Test if RUNTIME_DEPENDENCIES is needed and available
set(RUNTIME_DEPENDENCIES_LEVEL modelica)
if(${CMAKE_VERSION} VERSION_LESS "3.21" AND NOT ${RUNTIME_DEPENDENCIES_LEVEL} STREQUAL "none")
  message(FATAL_ERROR
          "--fmuRuntimeDepends=${RUNTIME_DEPENDENCIES_LEVEL} requiers CMake version 3.21 or higher.\n"
          "You are running version ${CMAKE_VERSION}.\n"
          "Use OpenModelica compiler flag '--fmuRuntimeDepends=none' to disable including runtime dependencies into FMU.")
endif()

if(NOT FMI_INTERFACE_HEADER_FILES_DIRECTORY)
  message(FATAL_ERROR "No FMI export headers provided. Set -DFMI_INTERFACE_HEADER_FILES_DIRECTORY=/path/to/fmi/headers")
endif()
find_file(FMI2_FUNCTIONS_H "fmi2Functions.h"
          PATHS ${FMI_INTERFACE_HEADER_FILES_DIRECTORY}
          NO_DEFAULT_PATH,
          NO_CMAKE_FIND_ROOT_PATH)
if(NOT FMI2_FUNCTIONS_H)
  message(FATAL_ERROR "Could not find fmi2Functions.h in FMI_INTERFACE_HEADER_FILES_DIRECTORY=${FMI_INTERFACE_HEADER_FILES_DIRECTORY}")
endif()
message(STATUS "FMI2 include directory: ${FMI_INTERFACE_HEADER_FILES_DIRECTORY}")

set(THREADS_PTHREAD_ARG "2" CACHE STRING "Forcibly set by CMakeLists.txt." FORCE)
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

file(GLOB_RECURSE FMU_RUNTIME_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/external_solvers/*.c
                                      ${CMAKE_CURRENT_SOURCE_DIR}/gc/*.c
                                      ${CMAKE_CURRENT_SOURCE_DIR}/math-support/pivot.c
                                      ${CMAKE_CURRENT_SOURCE_DIR}/meta/*.c
                                      ${CMAKE_CURRENT_SOURCE_DIR}/simulation/*.c
                                      ${CMAKE_CURRENT_SOURCE_DIR}/util/*.c)

file(GLOB FMU_GENERATED_MODEL_SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/*.c)

if(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
  set(FMU_TARGET_SYSTEM_NAME "win")
elseif(${CMAKE_SYSTEM_NAME} STREQUAL "Linux")
  set(FMU_TARGET_SYSTEM_NAME "linux")
elseif(${CMAKE_SYSTEM_NAME} STREQUAL "Darwin")
  set(FMU_TARGET_SYSTEM_NAME "darwin")
else()
  message(FATAL_ERROR "Unknown target system: ${CMAKE_SYSTEM_NAME}")
endif()

if(${CMAKE_SIZEOF_VOID_P} EQUAL 8)
  set(FMU_TARGET_PLATFORM "${FMU_TARGET_SYSTEM_NAME}64")
else()
  set(FMU_TARGET_PLATFORM "${FMU_TARGET_SYSTEM_NAME}32")
endif()

message(STATUS "Building for FMI platform ${FMU_TARGET_PLATFORM}")

set(CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_SOURCE_DIR}/../binaries/${FMU_TARGET_PLATFORM})
set(CMAKE_INSTALL_LIBDIR ${CMAKE_INSTALL_PREFIX})
set(CMAKE_INSTALL_BINDIR ${CMAKE_INSTALL_PREFIX})
set(CMAKE_SHARED_LIBRARY_PREFIX "")

# Set RPATH
if(APPLE)
  set(CMAKE_INSTALL_RPATH "@loader_path")
else()
  set(CMAKE_INSTALL_RPATH "$ORIGIN")
endif()

add_library(${FMU_NAME} SHARED
            ${FMU_RUNTIME_SOURCES}
            ${FMU_GENERATED_MODEL_SOURCES})

if(NOT ${CMAKE_VERSION} VERSION_LESS "3.13")
  target_link_options(${FMU_NAME} PRIVATE "LINKER:SHELL:--no-undefined")
endif()
target_link_libraries(${FMU_NAME} PRIVATE m Threads::Threads)
set(EXTERNAL_LIBDIRECTORIES "C:/Program Files/OpenModelica1.20.0-64bit/bin")


target_include_directories(${FMU_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_include_directories(${FMU_NAME} PRIVATE ${FMI_INTERFACE_HEADER_FILES_DIRECTORY}
                                               sundials)

target_compile_definitions(${FMU_NAME} PRIVATE OMC_MINIMAL_RUNTIME=1;OMC_FMI_RUNTIME=1;CMINPACK_NO_DLL)

if(RUNTIME_DEPENDENCIES_LEVEL STREQUAL "all")
  install(TARGETS ${FMU_NAME}
    RUNTIME_DEPENDENCIES
      DIRECTORIES ${EXTERNAL_LIBDIRECTORIES}
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR})
elseif(RUNTIME_DEPENDENCIES_LEVEL STREQUAL "modelica")
  install(TARGETS ${FMU_NAME}
    RUNTIME_DEPENDENCIES
      DIRECTORIES ${EXTERNAL_LIBDIRECTORIES}
      PRE_EXCLUDE_REGEXES "api-ms-" "ext-ms-"
      POST_EXCLUDE_REGEXES "^\\/lib.*" "^\\/usr\\/lib.*" "^\\/usr\\/local\\/lib.*" ".*system32/.*\\.dll"
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR})
else()
  install(TARGETS ${FMU_NAME}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_LIBDIR})
endif()

add_custom_target(create_zip COMMAND
    ${CMAKE_COMMAND} -E tar "cfv" "../${CMAKE_PROJECT_NAME}.fmu" --format=zip
    "binaries/"
    "resources/"
    "sources/"
    "modelDescription.xml"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../")
