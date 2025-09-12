# ampy-proto

[![Go Version](https://img.shields.io/badge/Go-1.23+-blue.svg)](https://golang.org/)
[![Python Version](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org/)
[![Protocol Buffers](https://img.shields.io/badge/Protocol%20Buffers-v3.21+-orange.svg)](https://developers.google.com/protocol-buffers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Canonical Protocol Buffer schemas for financial data processing**

ampy-proto provides type-safe, cross-language schemas for financial market data including bars, ticks, orders, fills, and more. Built for high-precision trading systems with support for Go, Python, and C++.

## 🚀 Quick Start

### Go

```bash
# Install the convenience package (imports all schemas)
go get github.com/AmpyFin/ampy-proto/v2@v2.0.9

# Or install specific packages only
go get github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/bars/v1@v2.0.9
```

```go
package main

import (
    "fmt"
    "time"
    
    "github.com/AmpyFin/ampy-proto/v2/pkg/ampy"
    bars "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/bars/v1"
    common "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/common/v1"
    "google.golang.org/protobuf/proto"
    "google.golang.org/protobuf/types/known/timestamppb"
)

func main() {
    bar := &bars.Bar{
        Security: &common.SecurityId{
            Symbol: "AAPL",
            Mic:    "XNAS",
        },
        Start: timestamppb.New(time.Now().Add(-time.Minute)),
        End:   timestamppb.New(time.Now()),
        Open: &common.Decimal{
            Scaled: 15000,  // 150.00 with scale 2
            Scale:  2,
        },
        Close: &common.Decimal{
            Scaled: 15050,  // 150.50 with scale 2
            Scale:  2,
        },
        Volume: 1000,
    }

    data, _ := proto.Marshal(bar)
    fmt.Printf("Serialized %d bytes using ampy-proto v%s\n", len(data), ampy.Version)
}
```

### Python

```bash
pip install ampy-proto==2.0.9
```

```python
from ampy.bars.v1 import bars_pb2
from ampy.common.v1 import common_pb2

bar = bars_pb2.Bar()
bar.security.symbol = "AAPL"
bar.security.mic = "XNAS"
bar.open.scaled = 15000
bar.open.scale = 2
bar.close.scaled = 15050
bar.close.scale = 2
bar.volume = 1000

print(f"Price: ${bar.close.scaled / (10 ** bar.close.scale):.2f}")
```

## 📊 Available Schemas

| Domain | Purpose | Key Messages |
|--------|---------|--------------|
| **bars** | OHLCV price bars | `Bar`, `BarBatch` |
| **ticks** | Trade and quote data | `Tick`, `TickBatch` |
| **orders** | Order management | `Order`, `OrderRequest` |
| **fills** | Trade executions | `Fill` |
| **signals** | Trading signals | `Signal` |
| **fundamentals** | Financial statements | `Fundamental` |
| **news** | Market news | `NewsItem` |
| **fx** | Foreign exchange | `FxRate` |
| **positions** | Portfolio positions | `Position` |
| **universe** | Tradable securities | `Universe` |
| **common** | Shared types | `Decimal`, `SecurityId`, `Money` |

## 🎯 Key Features

### High-Precision Decimals
Avoid floating-point errors with scaled decimal types:

```go
price := &common.Decimal{
    Scaled: 15050,  // 150.50
    Scale:  2,      // 2 decimal places
}
```

### Time Discipline
Clear separation of event time vs. ingest time:

```go
bar := &bars.Bar{
    EventTime:  timestamppb.New(marketTime),  // When it happened
    IngestTime: timestamppb.New(now),         // When we received it
}
```

### Security Identification
Proper market identification beyond just tickers:

```go
security := &common.SecurityId{
    Symbol: "AAPL",
    Mic:    "XNAS",  // Market identifier code
    Figi:   "BBG000B9XRY4",  // Optional
}
```

## 🛠️ Development

### Prerequisites
- [Buf](https://buf.build/docs/installation) for protobuf management
- Go 1.23+ for Go code generation
- Python 3.9+ for Python code generation
- CMake and C++17 compiler for C++ code generation

### Building

```bash
# Generate code for all languages
make gen

# Lint protobuf files
make lint

# Run tests
make test

# Build Python package
make py-build
```

### Testing

```bash
# Test Go imports
go run examples/go/smoke/main.go

# Test Python imports
python examples/python/smoke.py

# Run roundtrip tests
make test
```

## 📈 Versioning

This project follows semantic versioning:
- **Major versions** (v2, v3): Breaking changes requiring migration
- **Minor versions** (v2.1, v2.2): Additive changes, backward compatible
- **Patch versions** (v2.0.8, v2.0.9): Bug fixes, backward compatible

**Current version: v2.0.9**

## 🔧 Requirements

### Go
```go
require (
    github.com/AmpyFin/ampy-proto/v2 v2.0.9+
    google.golang.org/protobuf v1.36.8
)
```

### Python
```python
# pyproject.toml
dependencies = ["protobuf>=6.32.0,<7"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run `make lint` and `make test`
5. Submit a pull request

### Schema Evolution Rules

- ✅ **Add new optional fields** with default values
- ✅ **Add new enum values** (append only)
- ✅ **Add new messages** or services
- ❌ **Never change field numbers** of existing fields
- ❌ **Never change field types** of existing fields
- ❌ **Never remove fields** (mark as deprecated instead)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/AmpyFin/ampy-proto/issues)
- **Documentation**: [Project Wiki](https://github.com/AmpyFin/ampy-proto/wiki)

---

**Part of the AmpyFin ecosystem - building the future of algorithmic trading.**