# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.8] - 2024-12-19

### Fixed
- Fixed protobuf generation compatibility issues with protoc-gen-go v1.36.8
- Resolved slice bounds errors that caused runtime panics
- Updated import paths to use correct v2 module structure
- Synchronized protobuf versions across all language bindings

### Changed
- Updated Go examples to use correct import paths and types
- Improved smoke tests for all supported languages
- Enhanced build process reliability

## [2.0.7] - 2024-12-19

### Fixed
- Initial fix for protobuf descriptor corruption
- Updated to protoc-gen-go v1.35.2 for compatibility

## [2.0.6] - 2024-12-19

### Added
- Initial release of ampy-proto v2
- Support for Go, Python, and C++ code generation
- Comprehensive schema definitions for financial data
- High-precision decimal types for price data
- Time discipline with event/ingest time separation
- Security identification with MIC codes
- Metadata support for data lineage

### Security
- All timestamps are UTC with clear semantics
- Proper security identification beyond ticker symbols
- Scaled decimal types prevent floating-point precision errors
