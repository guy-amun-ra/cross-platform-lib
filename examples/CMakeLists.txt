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

# Platform-specific settings
if(UNIX)
    # Maintain existing UNIX/Linux/macOS rpath settings
    set_target_properties(version dynamic_example PROPERTIES
        INSTALL_RPATH "${CMAKE_INSTALL_RPATH}"
        BUILD_WITH_INSTALL_RPATH TRUE
    )
elseif(WIN32)
    # For Windows, ensure DLL can be found during development
    set_target_properties(version dynamic_example PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=${CMAKE_BINARY_DIR}/bin;$ENV{PATH}"
    )
    
    # Copy DLL to example binary location for Windows
    foreach(TARGET version dynamic_example)
        add_custom_command(TARGET ${TARGET} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "$<TARGET_FILE:${PROJECT_NAME}>"
            "$<TARGET_FILE_DIR:${TARGET}>"
        )
    endforeach()
endif()
