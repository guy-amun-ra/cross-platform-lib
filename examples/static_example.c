#include <stdio.h>
#include "cross_platform_lib/cross_platform_lib.h"

int main() {
    printf("Static linking example\n");
    printf("Library version: %s\n", get_library_version());
    return 0;
}