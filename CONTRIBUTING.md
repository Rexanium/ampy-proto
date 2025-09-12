# Contributing to ampy-proto

Thank you for your interest in contributing to ampy-proto! This document provides guidelines for contributing to this project.

## 🚀 Getting Started

### Prerequisites

- [Buf](https://buf.build/docs/installation) for protobuf management
- Go 1.23+ for Go code generation
- Python 3.9+ for Python code generation
- CMake and C++17 compiler for C++ code generation

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/ampy-proto.git
   cd ampy-proto
   ```

3. Install dependencies:
   ```bash
   # Install Buf
   go install github.com/bufbuild/buf/cmd/buf@latest
   
   # Install protobuf tools
   go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.36.8
   ```

4. Generate code and run tests:
   ```bash
   make gen
   make test
   ```

## 📋 Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes to the `.proto` files in `proto/`

3. Regenerate code:
   ```bash
   make gen
   ```

4. Run tests to ensure everything works:
   ```bash
   make test
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your feature description"
   ```

6. Push and create a pull request

### Schema Evolution Guidelines

When modifying protobuf schemas, follow these rules:

#### ✅ Allowed Changes
- Add new optional fields with default values
- Add new enum values (append only)
- Add new messages or services
- Add new methods to existing services
- Mark fields as deprecated (but don't remove them)

#### ❌ Breaking Changes (Not Allowed)
- Change field numbers of existing fields
- Change field types of existing fields
- Remove fields (even deprecated ones)
- Renumber enum values
- Change message names
- Change package names

### Testing

All changes must pass the following tests:

```bash
# Lint protobuf files
make lint

# Check for breaking changes
buf breaking proto --against '.git#branch=main'

# Run roundtrip tests
make test

# Test Go smoke test
go run examples/go/smoke/main.go

# Test Python smoke test
python examples/python/smoke.py
```

### Code Style

- Use clear, descriptive field names
- Add comprehensive comments to all messages and fields
- Follow protobuf naming conventions (snake_case for fields)
- Use proper enum naming (UPPER_SNAKE_CASE)

## 🐛 Bug Reports

When reporting bugs, please include:

1. Version of ampy-proto you're using
2. Go/Python version
3. Steps to reproduce
4. Expected vs actual behavior
5. Error messages (if any)

## 💡 Feature Requests

For feature requests, please:

1. Check existing issues first
2. Provide a clear description of the feature
3. Explain the use case and benefits
4. Consider backward compatibility

## 📝 Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new functionality
4. Update CHANGELOG.md
5. Request review from maintainers

### PR Title Format
- `feat: add new feature`
- `fix: resolve issue with X`
- `docs: update documentation`
- `refactor: improve code structure`

## 🏷️ Release Process

Releases are managed through GitHub tags:

1. Update version in `VERSION` and `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create and push a git tag
4. The CI/CD pipeline handles the rest

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/AmpyFin/ampy-proto/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AmpyFin/ampy-proto/discussions)

## 📄 License

By contributing to ampy-proto, you agree that your contributions will be licensed under the MIT License.
