#!/bin/bash
# Test script to verify C++ build works locally
# This mimics what happens in GitHub Actions

set -e

echo "🔧 Testing C++ build locally..."

# Check if we're on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detected macOS"
    # Install dependencies using Homebrew
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    echo "📦 Installing dependencies with Homebrew..."
    brew install protobuf abseil cmake
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux"
    # Install dependencies using apt
    echo "📦 Installing dependencies with apt..."
    sudo apt-get update
    sudo apt-get install -y libprotobuf-dev protobuf-compiler libabsl-dev cmake build-essential
    
    # Install newer protobuf version
    echo "📦 Installing protobuf v24.4..."
    wget https://github.com/protocolbuffers/protobuf/releases/download/v24.4/protobuf-24.4.tar.gz
    tar -xzf protobuf-24.4.tar.gz
    cd protobuf-24.4
    mkdir build && cd build
    # Build protobuf without Abseil to avoid target naming conflicts
    cmake -DCMAKE_BUILD_TYPE=Release -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_ABSL_PROVIDER=none -DCMAKE_INSTALL_PREFIX=/usr/local ..
    make -j$(nproc)
    sudo make install
    sudo ldconfig
    cd ../..
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

# Generate protobuf code
echo "🔄 Generating protobuf code..."
buf generate proto

# Build C++ library
echo "🔨 Building C++ library..."
cmake -S gen/cpp -B build/cpp
cmake --build build/cpp -j

echo "✅ C++ build successful!"
echo "📁 Static library created at: build/cpp/libampy_proto.a"

# Test the library
echo "🧪 Testing the library..."
if [[ -f "build/cpp/libampy_proto.a" ]]; then
    echo "✅ Static library exists and is ready to use"
    ls -la build/cpp/libampy_proto.a
else
    echo "❌ Static library not found"
    exit 1
fi

echo "🎉 All tests passed! The C++ build should work in CI."
