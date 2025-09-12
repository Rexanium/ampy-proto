cmake_minimum_required(VERSION 3.16)
project(cpp_smoke_test LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(Protobuf REQUIRED)
find_package(absl REQUIRED)

# Add the smoke test executable
add_executable(smoke_test smoke.cpp)

# Link libraries
target_link_libraries(smoke_test
    PRIVATE
    /Users/yeonlee/ampy-proto/build/cpp/libampy_proto.a
    protobuf::libprotobuf
    absl::base
    absl::strings
    absl::str_format
    absl::time
    absl::log_entry
    absl::log_flags
    absl::log_globals
    absl::log_initialize
    absl::log_internal_check_op
    absl::log_internal_conditions
    absl::log_internal_format
    absl::log_internal_globals
    absl::log_internal_message
    absl::log_internal_proto
    absl::log_severity
    absl::log_sink
    absl::raw_logging_internal
)

# Include directories
target_include_directories(smoke_test
    PRIVATE
    /Users/yeonlee/ampy-proto/gen/cpp
)
