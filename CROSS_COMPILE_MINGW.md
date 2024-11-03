# Windows (MinGW) Cross-Compilation Guide

This document describes how to cross-compile Windows executables from a Linux workstation using Distrobox and MinGW-w64. This setup provides an isolated, reproducible build environment for Windows targets.

## Verified Environment

### Host System Requirements
- Linux workstation (tested on Ubuntu 22.04 or compatible)
- Distrobox installed
- Internet connection for package installation

### Container Environment (Fedora 41)
The following package versions have been tested and confirmed working:

#### Compilers and Build Tools
- mingw64-gcc: 14.2.1-3.fc41
- mingw64-gcc-c++: 14.2.1-3.fc41
- cmake: 3.28.3-7.fc41
- make: (from base Fedora repository)

#### Wine Environment
- wine: 9.15-1.fc41
- wine-core: 9.15-1.fc41
- wine-common: 9.15-1.fc41

## Quick Start

### 1. Create Build Environment
```bash
# Create and setup Fedora 41 container with all required tools
distrobox create -i fedora:41 -n mingw-build && \
distrobox enter mingw-build -- sudo dnf install -y \
    mingw64-gcc \
    mingw64-gcc-c++ \
    mingw64-winpthreads-static \
    mingw64-winpthreads \
    wine \
    wine-core \
    cmake \
    make \
    git \
    gcc \
    gcc-c++ \
    python3 \
    python3-pip \
    python3-pefile \
    llvm
```

### 2. Verify Installation
```bash
# Enter the container
distrobox enter mingw-build

# Check installed versions
rpm -qa | grep -E "mingw64-gcc|wine|cmake"

# Verify compiler
x86_64-w64-mingw32-gcc --version  # Should show 14.2.1
x86_64-w64-mingw32-g++ --version  # Should show 14.2.1

# Verify Wine
wine --version  # Should show wine-9.15
```

### 3. Build Project
```bash
cd /path/to/your/project
mkdir build-windows && cd build-windows
cmake -DCMAKE_TOOLCHAIN_FILE=../cmake/mingw-w64-toolchain.cmake -DBUILD_TESTS=ON ..
cmake --build .
```

### 4. Run Tests and Examples

#### Runnthing through CTest
```bash
ctest
```
Another way, more verbose:
```bash
ctest --verbose
```

#### Running Directly with Wine
```bash
cd bin
# Unit Tests
wine test_version.exe
# Examples
wine version.exe
wine dynamic_example.exe
wine static_example.exe
```

## Build Configuration

### CMake Toolchain Settings
The MinGW-w64 toolchain file (`cmake/mingw-w64-toolchain.cmake`) includes:
- Cross-compilation settings
- Threading support
- Static linking configuration
- Windows-specific flags

### Important CMake Flags
```bash
-DBUILD_TESTS=ON        # Enable building tests (default OFF)
-DBUILD_EXAMPLES=ON     # Enable building examples (default ON)
```

## Testing

### Running Tests with Wine
- Tests are built as Windows executables (.exe)
- Wine is used to run the tests on Linux
- Test results are reported in standard GTest format

## Container Management

### Creating New Container
```bash
distrobox create -i fedora:41 -n mingw-build
```

### Removing Container
```bash
distrobox rm mingw-build -f
```

### Entering Container
```bash
distrobox enter mingw-build
```

## Version Control
Add these version requirements to your project documentation:
```txt
[build-dependencies]
mingw64-gcc = "14.2.1"
mingw64-gcc-c++ = "14.2.1"
cmake = "3.28.3"
wine = "9.15"
```

## Tools
### Inspecting DLL Resources

Windows DLLs contain resource information including version, copyright, and other metadata. 
Here are the tools available for inspecting these resources:

#### Using Python pefile (Recommended)
```bash
# View DLL resources
../tools/pe_resource_parser.py bin/cross_platform_lib.dll
```
Output includes:
- FileVersion
- ProductVersion
- FileDescription
- InternalName
- OriginalFilename
- ProductName
- LegalCopyright

### Using LLVM Tools
```bash
# View detailed resource information
llvm-readobj --coff-resources bin/cross_platform_lib.dll
```

Note: While Wine's tools (`winedump`, `strings`) are available, they may not work 
reliably in a cross-compilation environment. Stick to the native Linux tools listed above 
for resource inspection.

## Common Issues and Solutions

### 1. GTest Threading Issues
- Ensure proper static linking in CMake configuration
- Verify MinGW-w64 version 14.2.1 or newer
- Verify threading support is enabled (thread support flags)

### 2. Wine Configuration
- Run `winecfg` to set up Wine environment
- Verify 64-bit Wine installation
- Check Wine prefix settings
- Missing DLLs
   - Check if required MinGW DLLs are present
   - Verify Wine configuration with `winecfg`

### 3. Build Failures
- Verify exact package versions match
- Check for missing dependencies
- Ensure proper toolchain configuration

## References
- [MinGW-w64 ](https://www.mingw-w64.org/)
- [Wine Documentation](https://www.winehq.org/documentation)
- [CMake Cross Compilation Guide](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html)
