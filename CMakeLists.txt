cmake_minimum_required(VERSION 3.12)
project(cross-platform-lib)

# Specify the version
file(READ VERSION version_string)
string(STRIP ${version_string} version)

# Set library output directory
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)

# Include directories
include_directories(include)

# Add source files
add_library(cross-platform-lib SHARED src/cross_platform_lib.cpp src/version.cpp)

# CMake version handling
if(NOT version STREQUAL "")
    message(STATUS "Library version: ${version}")
endif()

# Add the example projects
add_subdirectory(examples)

# Add the tests
add_subdirectory(tests)

# Doxygen documentation
find_package(Doxygen REQUIRED)
if(Doxygen_FOUND)
    add_subdirectory(docs)
endif()

