#include <gtest/gtest.h>
#include <regex>
#include "cross_platform_lib/cross_platform_lib.h"

TEST(VersionTest, GetVersion) {
    const char* version = get_library_version();
    ASSERT_NE(version, nullptr);
    EXPECT_STRNE(version, "");
}

TEST(VersionTest, VersionFormat) {
    const char* version = get_library_version();
    // Expect version to match format X.Y.Z
    EXPECT_TRUE(std::regex_match(version, std::regex("\\d+\\.\\d+\\.\\d+")));
}
