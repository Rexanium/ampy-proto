package main

import (
    "testing"
    bars "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/bars/v1"
    common "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/common/v1"
    "google.golang.org/protobuf/proto"
)

func TestProtoValidation(t *testing.T) {
    // Test that types can be created without panic
    bar := &bars.Bar{
        Security: &common.SecurityId{Symbol: "TEST"},
    }
    
    // Test marshaling/unmarshaling
    data, err := proto.Marshal(bar)
    if err != nil {
        t.Fatalf("Marshal failed: %v", err)
    }
    
    newBar := &bars.Bar{}
    if err := proto.Unmarshal(data, newBar); err != nil {
        t.Fatalf("Unmarshal failed: %v", err)
    }
}