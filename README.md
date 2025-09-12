# ampy-proto

[![Go Version](https://img.shields.io/badge/Go-1.23+-blue.svg)](https://golang.org/)
[![Python Version](https://img.shields.io/badge/Python-3.9+-green.svg)](https://python.org/)
[![Protocol Buffers](https://img.shields.io/badge/Protocol%20Buffers-v3.21+-orange.svg)](https://developers.google.com/protocol-buffers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Canonical Protocol Buffer schemas for financial data processing**

ampy-proto provides type-safe, cross-language schemas for financial market data including bars, ticks, orders, fills, and more. Built for high-precision trading systems with support for Go, Python, and C++.

## What We're Solving

AmpyFin is building a self-learning, modular trading system that needs to handle data from multiple sources (DataBento, Tiingo, yfinance, etc.) across different languages (Go, Python, C++). This project provides:

- **Unified schemas** for all financial data (bars, ticks, fundamentals, news, etc.)
- **Cross-language compatibility** with generated code for Go, Python, and C++
- **Precision guarantees** using scaled decimal types instead of floating-point
- **Time discipline** with UTC timestamps and clear event/ingest time separation
- **Versioned contracts** that evolve safely without breaking consumers

## 🚀 Quick Start

### Python

```bash
# Install from PyPI
pip install ampy-proto==2.1.1

# Or install locally
pip install -e .
```

```python
from ampy.bars.v1 import bars_pb2
from ampy.common.v1 import common_pb2

# Create a bar
bar = bars_pb2.Bar()
bar.security.symbol = "AAPL"
bar.security.mic = "XNAS"
bar.open.scaled = 1923450
bar.open.scale = 4
bar.high.scaled = 1925600
bar.high.scale = 4
bar.low.scaled = 1922200
bar.low.scale = 4
bar.close.scaled = 1924100
bar.close.scale = 4
bar.volume = 184230

print(f"AAPL bar: ${bar.close.scaled / (10 ** bar.close.scale):.2f}")
```

### Go

```bash
# Add to your go.mod
go get github.com/AmpyFin/ampy-proto/v2@v2.1.1
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
            Scaled: 1923450,  // 192.3450 with scale 4
            Scale:  4,
        },
        Close: &common.Decimal{
            Scaled: 1924100,  // 192.4100 with scale 4
            Scale:  4,
        },
        Volume: 184230,
    }

    data, _ := proto.Marshal(bar)
    fmt.Printf("Serialized %d bytes using ampy-proto v%s\n", len(data), ampy.Version)
}
```

### C++

**Prerequisites**: Install latest versions of Abseil and Protobuf:

```bash
# Install Abseil (latest version)
git clone https://github.com/abseil/abseil-cpp.git
cd abseil-cpp
mkdir build && cd build
cmake -DCMAKE_CXX_STANDARD=17 -DCMAKE_POSITION_INDEPENDENT_CODE=ON ..
make -j$(nproc)
sudo make install

# Install Protobuf (latest version)
git clone https://github.com/protobuf/protobuf.git
cd protobuf
git submodule update --init --recursive
mkdir build && cd build
cmake -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_CXX_STANDARD=17 ..
make -j$(nproc)
sudo make install
```

**Build the library**:

```bash
# Build the library
cd gen/cpp
mkdir build && cd build
cmake .. && make
```

```cpp
#include <iostream>
#include "ampy/bars/v1/bars.pb.h"

int main() {
    ampy::bars::v1::Bar bar;
    bar.mutable_security()->set_symbol("AAPL");
    bar.mutable_security()->set_mic("XNAS");
    bar.mutable_open()->set_scaled(1923450);
    bar.mutable_open()->set_scale(4);
    bar.mutable_high()->set_scaled(1925600);
    bar.mutable_high()->set_scale(4);
    bar.mutable_low()->set_scaled(1922200);
    bar.mutable_low()->set_scale(4);
    bar.mutable_close()->set_scaled(1924100);
    bar.mutable_close()->set_scale(4);
    bar.set_volume(184230);

    std::cout << "AAPL bar: $" 
              << (bar.close().scaled() / std::pow(10, bar.close().scale()))
              << std::endl;
    return 0;
}
```

## 📊 Available Schemas

| Domain | Purpose | Key Messages |
|--------|---------|--------------|
| **bars** | OHLCV price bars | `Bar`, `BarBatch` |
| **ticks** | Trade and quote data | `Tick`, `TickBatch` |
| **fundamentals** | Financial statements | `Fundamental`, `FundamentalBatch` |
| **news** | Market news and sentiment | `NewsItem` |
| **fx** | Foreign exchange rates | `FxRate` |
| **corporate_actions** | Splits, dividends | `CorporateAction` |
| **universe** | Tradable securities lists | `Universe` |
| **signals** | Model outputs and signals | `Signal` |
| **orders** | Order management | `Order`, `OrderRequest` |
| **fills** | Trade executions | `Fill` |
| **positions** | Portfolio positions | `Position` |
| **metrics** | Operational metrics | `Metric` |
| **common** | Shared types | `Decimal`, `Money`, `SecurityId`, `Meta` |

## 🎯 Key Design Principles

### 1. Precision with Scaled Decimals
Instead of floating-point numbers, we use scaled decimals:
```protobuf
message Decimal {
  int64 scaled = 1;  // The actual value
  int32 scale = 2;   // Decimal places (e.g., 4 = 4 decimal places)
}
```

Example: `scaled: 1923450, scale: 4` represents `192.3450`

### 2. Time Discipline
All timestamps are UTC with clear semantics:
- `event_time`: When the market event actually happened
- `ingest_time`: When our system received it
- `as_of`: Logical timestamp for downstream processing

### 3. Security Identification
Use proper security identifiers, not just tickers:
```protobuf
message SecurityId {
  string symbol = 1;    // e.g., "AAPL"
  string mic = 2;       // Market identifier code, e.g., "XNAS"
  string figi = 3;      // Financial Instrument Global Identifier (optional)
  string isin = 4;      // International Securities Identification Number (optional)
}
```

### 4. Metadata for Traceability
Every message includes metadata for lineage:
```protobuf
message Meta {
  string run_id = 1;           // Unique run identifier
  string source = 2;           // Data source (e.g., "yfinance-go")
  string producer = 3;         // Producer instance ID
  string schema_version = 4;   // Schema version used
  string checksum = 5;         // Optional message checksum
}
```

## 🛠️ Development

### Prerequisites
- [Buf](https://buf.build/docs/installation) for protobuf management
- [Go](https://golang.org/) 1.23+ for Go code generation
- [Python](https://python.org/) 3.9+ for Python code generation
- [CMake](https://cmake.org/) and C++17 compiler for C++ code generation

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

# Test C++ compilation
cd examples/cpp && make && ./build/smoke_test

# Run roundtrip tests
make test
```

## 📈 Versioning

This project follows semantic versioning:
- **Major versions** (v2, v3): Breaking changes requiring migration
- **Minor versions** (v2.1, v2.2): Additive changes, backward compatible
- **Patch versions** (v2.1.0, v2.1.1): Bug fixes, backward compatible

**Current version: v2.1.1**

## 🔧 Requirements

### Go
```go
require (
    github.com/AmpyFin/ampy-proto/v2 v2.1.1+
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
- ❌ **Never renumber enum values**

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/AmpyFin/ampy-proto/issues)
- **Documentation**: [Project Wiki](https://github.com/AmpyFin/ampy-proto/wiki)

---

**Part of the AmpyFin ecosystem - building the future of algorithmic trading.**