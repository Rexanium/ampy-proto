cmake_minimum_required(VERSION 3.16)
project(ampy_proto LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Protobuf REQUIRED)
find_package(absl REQUIRED)

# Collect all generated C++ sources
file(GLOB_RECURSE AMPYPB_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/ampy/**/*.cc")

add_library(ampy_proto STATIC ${AMPYPB_SRCS})

target_include_directories(ampy_proto
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Add compiler flags to help with compatibility
target_compile_options(ampy_proto PRIVATE
  -Wno-unused-parameter
  -Wno-sign-compare
  -Wno-deprecated-declarations
)

target_link_libraries(ampy_proto
  PUBLIC
    protobuf::libprotobuf
    absl::base
    absl::strings
    absl::log
)

# Optional install if you want consumers to 'make install'
install(TARGETS ampy_proto EXPORT ampy_protoTargets ARCHIVE DESTINATION lib)
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/ampy DESTINATION include)

export(EXPORT ampy_protoTargets FILE "${CMAKE_CURRENT_BINARY_DIR}/ampy_protoTargets.cmake")