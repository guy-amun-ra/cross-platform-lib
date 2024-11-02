#include "cross_platform_lib/cross_platform_lib.h"
#include <stdio.h>

// This will be defined by CMake
#ifndef LIBRARY_VERSION
#define LIBRARY_VERSION "0.0.0"
#endif

const char* get_library_version() {
    static char version[15];
    snprintf(version, sizeof(version), "%s", LIBRARY_VERSION);
    return version;
}