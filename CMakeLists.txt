cmake_minimum_required(VERSION 3.12)

# Read version from file
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" VERSION_STRING)
string(STRIP "${VERSION_STRING}" VERSION_STRING)

# Set project name and version
project(cross_platform_lib VERSION ${VERSION_STRING} LANGUAGES C CXX)
set(OUTPUT_NAME "cross_platform_lib")

include(FetchContent)

# Set output directories for all platforms
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin)

# Platform-specific settings
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
elseif(WIN32)
    # Windows-specific settings
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
endif()

# Output the project version
message(STATUS "Building ${PROJECT_NAME} version ${PROJECT_VERSION}")

# Specify the C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

# Include directories
include_directories(include)

# Add source files
set(COMMON_SOURCES
    src/common/cross_platform_lib.c
    src/common/version.c
)

set(WINDOWS_SOURCES "")
if(WIN32)
    # Configure the Windows resource file
    configure_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/src/windows/version.rc.in"
        "${CMAKE_CURRENT_BINARY_DIR}/version.rc"
        @ONLY
    )
    
    set(WINDOWS_SOURCES
        src/windows/cross_platform_lib.def
        "${CMAKE_CURRENT_BINARY_DIR}/version.rc"
    )
endif()

# Combine all sources
set(SOURCES
    ${COMMON_SOURCES}
    ${WINDOWS_SOURCES}
)

# Create dynamic library
add_library(${PROJECT_NAME} SHARED ${SOURCES})

# Create static library
add_library(${PROJECT_NAME}_static STATIC ${SOURCES})

# Set properties for shared library
if(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VERSION ${PROJECT_VERSION}
        OUTPUT_NAME "cross_platform_lib"  # Explicitly set name with underscores
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
        PREFIX ""
    )
else()
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VERSION ${PROJECT_VERSION}
        SOVERSION ${PROJECT_VERSION_MAJOR}
        OUTPUT_NAME ${PROJECT_NAME}
    )
endif()

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

# Platform-specific compile definitions
if(WIN32)
    target_compile_definitions(${PROJECT_NAME}
        PRIVATE CROSS_PLATFORM_LIB_EXPORTS
        PUBLIC CROSS_PLATFORM_LIB_DLL)
    
    # Copy DLL to bin directory for Windows
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "$<TARGET_FILE:${PROJECT_NAME}>"
        "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/$<TARGET_FILE_NAME:${PROJECT_NAME}>")
elseif(APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        MACOSX_RPATH ON)
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
    # Fetch and make Google Test available
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG release-1.12.1
    )
    
    # For Windows: Prevent overriding the parent project's compiler/linker settings
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)
    enable_testing()
    include(GoogleTest)
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

# Doxygen documentation (uncomment when ready)
# find_package(Doxygen)
# if(DOXYGEN_FOUND)
#     add_subdirectory(docs)
# endif()