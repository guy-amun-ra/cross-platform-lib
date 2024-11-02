#ifndef CROSS_PLATFORM_LIB_H
#define CROSS_PLATFORM_LIB_H

#ifdef _WIN32
    #ifdef CROSS_PLATFORM_LIB_DLL
        #ifdef CROSS_PLATFORM_LIB_EXPORTS
            #define CROSS_PLATFORM_LIB_API __declspec(dllexport)
        #else
            #define CROSS_PLATFORM_LIB_API __declspec(dllimport)
        #endif
    #else
        #define CROSS_PLATFORM_LIB_API
    #endif
#else
    #define CROSS_PLATFORM_LIB_API __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Gets the library version.
 * @return A string containing the library version.
 */
CROSS_PLATFORM_LIB_API const char* get_library_version(void);

#ifdef __cplusplus
}
#endif

#endif // CROSS_PLATFORM_LIB_H
