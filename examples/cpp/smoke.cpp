#include <iostream>
#include <iomanip>
#include <chrono>
#include "ampy/bars/v1/bars.pb.h"
#include "ampy/common/v1/common.pb.h"
#include "google/protobuf/timestamp.pb.h"

int main() {
    std::cout << "🧪 Testing ampy-proto C++ functionality..." << std::endl;
    
    // Create a realistic financial bar
    auto now = std::chrono::system_clock::now();
    auto time_t_now = std::chrono::system_clock::to_time_t(now);
    auto start_time = time_t_now - 3600; // 1 hour ago
    
    ampy::bars::v1::Bar bar;
    
    // Set security
    ampy::common::v1::SecurityId* security = bar.mutable_security();
    security->set_symbol("AAPL");
    security->set_mic("XNAS");
    
    // Set timestamps
    google::protobuf::Timestamp* start_ts = bar.mutable_start();
    start_ts->set_seconds(start_time);
    start_ts->set_nanos(0);
    
    google::protobuf::Timestamp* end_ts = bar.mutable_end();
    end_ts->set_seconds(time_t_now);
    end_ts->set_nanos(0);
    
    // Set prices using Decimal
    ampy::common::v1::Decimal* open = bar.mutable_open();
    open->set_scaled(1923450); // $192.3450
    open->set_scale(4);
    
    ampy::common::v1::Decimal* high = bar.mutable_high();
    high->set_scaled(1925600); // $192.5600
    high->set_scale(4);
    
    ampy::common::v1::Decimal* low = bar.mutable_low();
    low->set_scaled(1922200); // $192.2200
    low->set_scale(4);
    
    ampy::common::v1::Decimal* close = bar.mutable_close();
    close->set_scaled(1924100); // $192.4100
    close->set_scale(4);
    
    // Set other fields
    bar.set_volume(184230);
    bar.set_trade_count(1250);
    bar.set_adjusted(false);
    
    // Set event and ingest times
    google::protobuf::Timestamp* event_ts = bar.mutable_event_time();
    event_ts->set_seconds(time_t_now);
    event_ts->set_nanos(0);
    
    google::protobuf::Timestamp* ingest_ts = bar.mutable_ingest_time();
    ingest_ts->set_seconds(time_t_now + 1);
    ingest_ts->set_nanos(0);
    
    // Test serialization
    std::string serialized_data;
    if (!bar.SerializeToString(&serialized_data)) {
        std::cout << "❌ Serialization failed" << std::endl;
        return 1;
    }
    std::cout << "✅ Serialized " << serialized_data.size() << " bytes" << std::endl;
    
    // Test deserialization
    ampy::bars::v1::Bar deserialized_bar;
    if (!deserialized_bar.ParseFromString(serialized_data)) {
        std::cout << "❌ Deserialization failed" << std::endl;
        return 1;
    }
    
    // Verify data integrity
    if (deserialized_bar.security().symbol() != "AAPL") {
        std::cout << "❌ Symbol mismatch: " << deserialized_bar.security().symbol() 
                  << " != AAPL" << std::endl;
        return 1;
    }
    
    if (deserialized_bar.close().scaled() != 1924100) {
        std::cout << "❌ Close price mismatch: " << deserialized_bar.close().scaled() 
                  << " != 1924100" << std::endl;
        return 1;
    }
    
    if (deserialized_bar.volume() != 184230) {
        std::cout << "❌ Volume mismatch: " << deserialized_bar.volume() 
                  << " != 184230" << std::endl;
        return 1;
    }
    
    double close_price = static_cast<double>(deserialized_bar.close().scaled()) / 10000.0;
    std::cout << "✅ AAPL bar: $" << std::fixed << std::setprecision(4) << close_price 
              << " (Volume: " << deserialized_bar.volume() << ")" << std::endl;
    
    // Test batch functionality
    ampy::bars::v1::BarBatch batch;
    batch.add_bars()->CopyFrom(bar);
    
    std::string batch_data;
    if (!batch.SerializeToString(&batch_data)) {
        std::cout << "❌ Batch serialization failed" << std::endl;
        return 1;
    }
    
    ampy::bars::v1::BarBatch deserialized_batch;
    if (!deserialized_batch.ParseFromString(batch_data)) {
        std::cout << "❌ Batch deserialization failed" << std::endl;
        return 1;
    }
    
    if (deserialized_batch.bars_size() != 1) {
        std::cout << "❌ Batch size mismatch: " << deserialized_batch.bars_size() 
                  << " != 1" << std::endl;
        return 1;
    }
    
    std::cout << "✅ Batch test passed: " << deserialized_batch.bars_size() << " bars" << std::endl;
    std::cout << "🎉 All ampy-proto C++ tests passed!" << std::endl;
    
    return 0;
}
