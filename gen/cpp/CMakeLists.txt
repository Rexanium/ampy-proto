cmake_minimum_required(VERSION 3.16)
project(ampy_proto LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Protobuf REQUIRED)
# Try to find Abseil, but make it optional for compatibility
find_package(absl QUIET)

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
)

# Link Abseil libraries if available
if(absl_FOUND)
  target_link_libraries(ampy_proto
    PUBLIC
      absl::base
      absl::strings
      absl::log_internal_message
      absl::log_internal_check_op
      absl::log_internal_format
      absl::log_internal_conditions
      absl::log_internal_globals
      absl::log_internal_proto
      absl::log_internal_structured_proto
      absl::log_internal_log_sink_set
      absl::log_internal_nullguard
      absl::log_internal_entry
      absl::log_internal_voidify
  )
else()
  # Fallback: try to link system Abseil libraries directly
  find_library(ABSL_BASE_LIB absl_base)
  find_library(ABSL_STRINGS_LIB absl_strings)
  find_library(ABSL_LOG_LIB absl_log)
  
  if(ABSL_BASE_LIB)
    target_link_libraries(ampy_proto PUBLIC ${ABSL_BASE_LIB})
  endif()
  if(ABSL_STRINGS_LIB)
    target_link_libraries(ampy_proto PUBLIC ${ABSL_STRINGS_LIB})
  endif()
  if(ABSL_LOG_LIB)
    target_link_libraries(ampy_proto PUBLIC ${ABSL_LOG_LIB})
  endif()
endif()

# Optional install if you want consumers to 'make install'
install(TARGETS ampy_proto EXPORT ampy_protoTargets ARCHIVE DESTINATION lib)
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/ampy DESTINATION include)

export(EXPORT ampy_protoTargets FILE "${CMAKE_CURRENT_BINARY_DIR}/ampy_protoTargets.cmake")