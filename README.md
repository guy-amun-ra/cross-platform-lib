# Cross-Platform Library

A cross-platform shared library skeleton with CMake support.

## Features

- Easy to rename
- CMake-based build system (for C projects)
- Cross-platform support (Linux, Windows, macOS, Android, iOS)
- Multi-architecture support (ARM, x86, etc.)
- Version management with a VERSION file
- Example projects (dynamic and static linking) - to be implemented
- Google Test integration - to be implemented
- Doxygen documentation support - to be implemented

## Getting Started

### Prerequisites

- CMake (version 3.12 or higher)
- A C++ compiler (e.g., GCC, Clang, MSVC)

### Building the Library

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cross-platform-lib.git
   cd cross-platform-lib
   ```

2. Create a build directory:
   ```
   mkdir build && cd build
   ```

3. Configure and build the project:
   ```
   cmake ..
   cmake --build .
   ```

## Renaming the Project

To rename the project and set the author name, use the provided Python script:

```
python rename_project.py cross-platform-lib <new-name> "<First Last>"
```

Example:
```
python rename_project.py cross-platform-lib my-awesome-lib "John Doe"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- CMake
- Google Test
- Doxygen

