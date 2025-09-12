package main

import (
	"fmt"
	"time"
	
	barspb "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/bars/v1"
	commonpb "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/common/v1"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/types/known/timestamppb"
)

func main() {
	fmt.Println("🧪 Testing ampy-proto Go functionality...")
	
	// Create a realistic financial bar
	now := time.Now()
	bar := &barspb.Bar{
		Security: &commonpb.SecurityId{
			Symbol: "AAPL",
			Mic:    "XNAS",
		},
		Start: timestamppb.New(now.Add(-time.Hour)),
		End:   timestamppb.New(now),
		Open: &commonpb.Decimal{
			Scaled: 1923450, // $192.3450
			Scale:  4,
		},
		High: &commonpb.Decimal{
			Scaled: 1925600, // $192.5600
			Scale:  4,
		},
		Low: &commonpb.Decimal{
			Scaled: 1922200, // $192.2200
			Scale:  4,
		},
		Close: &commonpb.Decimal{
			Scaled: 1924100, // $192.4100
			Scale:  4,
		},
		Volume: 184230,
		TradeCount: 1250,
		Adjusted: false,
		EventTime: timestamppb.New(now),
		IngestTime: timestamppb.New(now.Add(time.Second)),
	}
	
	// Test serialization
	data, err := proto.Marshal(bar)
	if err != nil {
		fmt.Printf("❌ Serialization failed: %v\n", err)
		return
	}
	fmt.Printf("✅ Serialized %d bytes\n", len(data))
	
	// Test deserialization
	deserializedBar := &barspb.Bar{}
	err = proto.Unmarshal(data, deserializedBar)
	if err != nil {
		fmt.Printf("❌ Deserialization failed: %v\n", err)
		return
	}
	
	// Verify data integrity
	if deserializedBar.Security.Symbol != "AAPL" {
		fmt.Printf("❌ Symbol mismatch: %s != AAPL\n", deserializedBar.Security.Symbol)
		return
	}
	
	if deserializedBar.Close.Scaled != 1924100 {
		fmt.Printf("❌ Close price mismatch: %d != 1924100\n", deserializedBar.Close.Scaled)
		return
	}
	
	if deserializedBar.Volume != 184230 {
		fmt.Printf("❌ Volume mismatch: %d != 184230\n", deserializedBar.Volume)
		return
	}
	
	fmt.Printf("✅ AAPL bar: $%.4f (Volume: %d)\n", 
		float64(deserializedBar.Close.Scaled)/float64(1e4), 
		deserializedBar.Volume)
	
	// Test batch functionality
	batch := &barspb.BarBatch{
		Bars: []*barspb.Bar{bar},
	}
	
	batchData, err := proto.Marshal(batch)
	if err != nil {
		fmt.Printf("❌ Batch serialization failed: %v\n", err)
		return
	}
	
	deserializedBatch := &barspb.BarBatch{}
	err = proto.Unmarshal(batchData, deserializedBatch)
	if err != nil {
		fmt.Printf("❌ Batch deserialization failed: %v\n", err)
		return
	}
	
	if len(deserializedBatch.Bars) != 1 {
		fmt.Printf("❌ Batch size mismatch: %d != 1\n", len(deserializedBatch.Bars))
		return
	}
	
	fmt.Printf("✅ Batch test passed: %d bars\n", len(deserializedBatch.Bars))
	fmt.Println("🎉 All ampy-proto Go tests passed!")
}
