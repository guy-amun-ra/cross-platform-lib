# Add test executable
add_executable(test_version test_version.cpp)

# Link against GTest and our library
target_link_libraries(test_version
    PRIVATE
    gtest
    gtest_main
    ${PROJECT_NAME}
)

# Set C++11 standard for the test
set_target_properties(test_version PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
)

if(MINGW)
    # Add required libraries for MinGW
    target_link_libraries(test_version
        PRIVATE
        pthread
        ws2_32
        wsock32
    )
endif()

# Add the test
include(GoogleTest)
if(NOT MINGW)
    gtest_discover_tests(test_version)
else()
    add_test(NAME test_version 
             COMMAND wine ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/test_version.exe)
endif()