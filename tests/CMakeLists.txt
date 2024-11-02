# Add test executable
add_executable(test_version test_version.cpp)

# Link against GTest and our library
target_link_libraries(test_version
    PRIVATE
    gtest
    gtest_main
    ${PROJECT_NAME}
)

# Add the test
include(GoogleTest)
gtest_discover_tests(test_version)