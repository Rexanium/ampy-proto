#!/usr/bin/env python3
"""
ampy-proto Python functionality test
Tests serialization, deserialization, and data integrity of financial protobuf messages.
"""

import time
from datetime import datetime, timedelta, timezone
from ampy.bars.v1 import bars_pb2 as bars
from ampy.common.v1 import common_pb2 as common
from google.protobuf.timestamp_pb2 import Timestamp

def create_timestamp(dt):
    """Convert datetime to protobuf Timestamp"""
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts

def main():
    print("🧪 Testing ampy-proto Python functionality...")
    
    # Create a realistic financial bar
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=1)
    
    bar = bars.Bar()
    
    # Set security
    bar.security.symbol = "AAPL"
    bar.security.mic = "XNAS"
    
    # Set timestamps
    bar.start.CopyFrom(create_timestamp(start_time))
    bar.end.CopyFrom(create_timestamp(now))
    
    # Set prices using Decimal
    bar.open.scaled = 1923450  # $192.3450
    bar.open.scale = 4
    
    bar.high.scaled = 1925600  # $192.5600
    bar.high.scale = 4
    
    bar.low.scaled = 1922200   # $192.2200
    bar.low.scale = 4
    
    bar.close.scaled = 1924100 # $192.4100
    bar.close.scale = 4
    
    # Set other fields
    bar.volume = 184230
    bar.trade_count = 1250
    bar.adjusted = False
    
    # Set event and ingest times
    bar.event_time.CopyFrom(create_timestamp(now))
    bar.ingest_time.CopyFrom(create_timestamp(now + timedelta(seconds=1)))
    
    # Test serialization
    try:
        serialized_data = bar.SerializeToString()
        print(f"✅ Serialized {len(serialized_data)} bytes")
    except Exception as e:
        print(f"❌ Serialization failed: {e}")
        return 1
    
    # Test deserialization
    try:
        deserialized_bar = bars.Bar()
        deserialized_bar.ParseFromString(serialized_data)
    except Exception as e:
        print(f"❌ Deserialization failed: {e}")
        return 1
    
    # Verify data integrity
    if deserialized_bar.security.symbol != "AAPL":
        print(f"❌ Symbol mismatch: {deserialized_bar.security.symbol} != AAPL")
        return 1
    
    if deserialized_bar.close.scaled != 1924100:
        print(f"❌ Close price mismatch: {deserialized_bar.close.scaled} != 1924100")
        return 1
    
    if deserialized_bar.volume != 184230:
        print(f"❌ Volume mismatch: {deserialized_bar.volume} != 184230")
        return 1
    
    close_price = deserialized_bar.close.scaled / 10000.0
    print(f"✅ AAPL bar: ${close_price:.4f} (Volume: {deserialized_bar.volume})")
    
    # Test batch functionality
    batch = bars.BarBatch()
    batch.bars.append(bar)
    
    try:
        batch_data = batch.SerializeToString()
    except Exception as e:
        print(f"❌ Batch serialization failed: {e}")
        return 1
    
    try:
        deserialized_batch = bars.BarBatch()
        deserialized_batch.ParseFromString(batch_data)
    except Exception as e:
        print(f"❌ Batch deserialization failed: {e}")
        return 1
    
    if len(deserialized_batch.bars) != 1:
        print(f"❌ Batch size mismatch: {len(deserialized_batch.bars)} != 1")
        return 1
    
    print(f"✅ Batch test passed: {len(deserialized_batch.bars)} bars")
    print("🎉 All ampy-proto Python tests passed!")
    return 0

if __name__ == "__main__":
    exit(main())
