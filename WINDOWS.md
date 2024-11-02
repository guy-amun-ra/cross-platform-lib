# Windows Support Documentation

This document describes how to set up and use Windows DLL support and cross-compilation from Linux to Windows.

## Prerequisites

### On Ubuntu/Debian
```bash
# Install MinGW-w64 cross-compiler and tools
sudo apt-get update
sudo apt-get install -y \
    mingw-w64 \
    wine64 \
    cmake \
    make \
    gcc \
    g++
```

### On Fedora
```bash
sudo dnf install -y \
    mingw64-gcc \
    mingw64-gcc-c++ \
    wine \
    cmake \
    make
```

### On Arch Linux
```bash
sudo pacman -S \
    mingw-w64-gcc \
    wine \
    cmake \
    make
```

## Directory Structure
```
project/
├── src/
│   ├── common/           # Platform-independent code
│   │   ├── cross_platform_lib.c
│   │   └── version.c
│   └── windows/         # Windows-specific code
│       ├── cross_platform_lib.def
│       └── version.rc
└── include/
    └── cross_platform_lib/
        └── cross_platform_lib.h
```

## Building

### Native Linux Build (Verification)
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

### Cross-Compilation to Windows
```bash
mkdir build-windows && cd build-windows
cmake -DCMAKE_TOOLCHAIN_FILE=../cmake/mingw-w64-toolchain.cmake ..
cmake --build .
```

## Testing

### Testing DLL Exports
```bash
# List exports from DLL
x86_64-w64-mingw32-objdump -p bin/cross-platform-lib.dll | grep "Export"

# Check version information
wine bin/cross-platform-lib.dll
```

### Running Examples
```bash
# Run the version example
wine bin/version.exe

# Run the dynamic linking example
wine bin/dynamic_example.exe
```

### Verifying Version Resource
```bash
# Check embedded version information
x86_64-w64-mingw32-strings bin/cross-platform-lib.dll | grep -i version
```

## Troubleshooting

### Common Issues

1. **DLL Not Found**
   - Ensure the DLL is in the same directory as the executable
   - Check PATH environment variable in Wine
   - Verify DLL dependencies using `x86_64-w64-mingw32-objdump -p`

2. **Compilation Errors**
   - Verify MinGW-w64 installation
   - Check if all required tools are in PATH
   - Ensure .def file exports match function declarations

3. **Wine Issues**
   - Run `winecfg` to configure Wine
   - Check Wine version compatibility
   - Verify 64-bit Wine installation

### Verification Commands
```bash
# Check MinGW version
x86_64-w64-mingw32-gcc --version

# Check Wine version
wine --version

# Verify toolchain installation
which x86_64-w64-mingw32-gcc
which x86_64-w64-mingw32-g++
which x86_64-w64-mingw32-windres
```

## Development Guidelines

1. **Windows-Specific Code**
   - Keep Windows-specific code in `src/windows/`
   - Use `#ifdef _WIN32` for platform-specific code
   - Follow Windows DLL best practices

2. **Version Information**
   - Version information is maintained in `VERSION` file
   - Windows resource file automatically uses project version
   - Version appears in DLL properties on Windows

3. **Cross-Platform Considerations**
   - Use platform-independent types
   - Avoid Windows-specific APIs in common code
   - Test both static and dynamic linking

## References

- [MinGW-w64 Documentation](http://mingw-w64.org/doku.php)
- [Wine Documentation](https://www.winehq.org/documentation)
- [Microsoft DLL Best Practices](https://docs.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices)
