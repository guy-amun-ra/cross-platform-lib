# Version example
add_executable(version version.c)
target_link_libraries(version PRIVATE ${PROJECT_NAME})

# Dynamic linking example
add_executable(dynamic_example dynamic_example.c)
target_link_libraries(dynamic_example PRIVATE ${PROJECT_NAME})

# Static linking example
add_executable(static_example static_example.c)
target_link_libraries(static_example PRIVATE ${PROJECT_NAME}_static)

# Set output directory for examples
set_target_properties(version dynamic_example static_example PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

# For non-Windows systems, set rpath to find the shared library relatively to the binary
if(UNIX)
    set_target_properties(version dynamic_example PROPERTIES
        INSTALL_RPATH "${CMAKE_INSTALL_RPATH}"
        BUILD_WITH_INSTALL_RPATH TRUE
    )
endif()