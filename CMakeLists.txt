cmake_minimum_required(VERSION 3.12)

# Read version from file
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" VERSION_STRING)
string(STRIP "${VERSION_STRING}" VERSION_STRING)

# Set project name and version
project(cross-platform-lib VERSION ${VERSION_STRING} LANGUAGES C)

# For non-Windows systems, set rpath to find the shared library relatively to the installed binary
if(UNIX)
    # Enable RPATH
    set(CMAKE_SKIP_BUILD_RPATH FALSE)
    set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
    set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

    # Set RPATH for use in the build tree
    if(APPLE)
        set(CMAKE_INSTALL_RPATH "@loader_path/../lib")
    else()
        set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
    endif()
endif()

# Output the project version
message(STATUS "Building ${PROJECT_NAME} version ${PROJECT_VERSION}")

# Specify the C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

# Set library output directory for both static and dynamic libraries
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin)

# Include directories
include_directories(include)

# Add source files
set(SOURCES
    src/cross_platform_lib.c
    src/version.c
)

# Create dynamic library
add_library(${PROJECT_NAME} SHARED ${SOURCES})

# Create static library
add_library(${PROJECT_NAME}_static STATIC ${SOURCES})

# Set properties for shared library
set_target_properties(${PROJECT_NAME} PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    OUTPUT_NAME ${PROJECT_NAME}
)

# Set properties for static library
set_target_properties(${PROJECT_NAME}_static PROPERTIES
    OUTPUT_NAME ${PROJECT_NAME}
)

# Define LIBRARY_VERSION for use in source files
target_compile_definitions(${PROJECT_NAME} PRIVATE 
    LIBRARY_VERSION="${PROJECT_VERSION}"
    LIBRARY_VERSION_MAJOR=${PROJECT_VERSION_MAJOR}
    LIBRARY_VERSION_MINOR=${PROJECT_VERSION_MINOR}
    LIBRARY_VERSION_PATCH=${PROJECT_VERSION_PATCH}
)
target_compile_definitions(${PROJECT_NAME}_static PRIVATE 
    LIBRARY_VERSION="${PROJECT_VERSION}"
    LIBRARY_VERSION_MAJOR=${PROJECT_VERSION_MAJOR}
    LIBRARY_VERSION_MINOR=${PROJECT_VERSION_MINOR}
    LIBRARY_VERSION_PATCH=${PROJECT_VERSION_PATCH}
)

# Platform-specific settings
if(WIN32)
    target_compile_definitions(${PROJECT_NAME} PRIVATE CROSS_PLATFORM_LIB_EXPORTS)
    target_compile_definitions(${PROJECT_NAME}_static PRIVATE CROSS_PLATFORM_LIB_STATIC)
elseif(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_RPATH ON
    )
endif()

# Options for building examples and tests
option(BUILD_EXAMPLES "Build example projects" ON)
option(BUILD_TESTS "Build and run tests" OFF)

# Add example projects
if(BUILD_EXAMPLES)
    add_subdirectory(examples)
endif()

# Add tests
if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()

# Install targets
install(TARGETS ${PROJECT_NAME} ${PROJECT_NAME}_static
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)

# Install headers
install(DIRECTORY include/ DESTINATION include)

# Copy shared library to bin directory for Windows
if(WIN32)
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:${PROJECT_NAME}>
        ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}
    )
endif()

# Doxygen documentation (uncomment when ready)
# find_package(Doxygen)
# if(DOXYGEN_FOUND)
#     add_subdirectory(docs)
# endif()