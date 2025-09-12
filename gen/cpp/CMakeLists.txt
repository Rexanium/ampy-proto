cmake_minimum_required(VERSION 3.16)
project(ampy_proto VERSION 2.0.9 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(Protobuf REQUIRED)
find_package(absl REQUIRED)

# Collect all generated protobuf source files
file(GLOB_RECURSE PROTOBUF_SOURCES "*.cc")
file(GLOB_RECURSE PROTOBUF_HEADERS "*.h")

# Create the static library
add_library(ampy_proto STATIC ${PROTOBUF_SOURCES})

# Set target properties
set_target_properties(ampy_proto PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    PUBLIC_HEADER "${PROTOBUF_HEADERS}"
)

# Link libraries
target_link_libraries(ampy_proto
    PRIVATE
    protobuf::libprotobuf
    absl::base
    absl::strings
    absl::str_format
    absl::time
    absl::log
)

# Include directories
target_include_directories(ampy_proto
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

# Compiler flags
target_compile_options(ampy_proto PRIVATE
    -Wall
    -Wextra
    -Wpedantic
    -Wno-unused-parameter
)

# Install targets
install(TARGETS ampy_proto
    EXPORT ampy_protoTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include
)

# Install headers
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)

# Export targets
install(EXPORT ampy_protoTargets
    FILE ampy_protoTargets.cmake
    NAMESPACE ampy_proto::
    DESTINATION lib/cmake/ampy_proto
)

# Create config file
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    ampy_protoConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/ampy_protoConfigVersion.cmake
    DESTINATION lib/cmake/ampy_proto
)

# Create a simple config file
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/ampy_protoConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/ampy_protoConfig.cmake
    INSTALL_DESTINATION lib/cmake/ampy_proto
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/ampy_protoConfig.cmake
    DESTINATION lib/cmake/ampy_proto
)
