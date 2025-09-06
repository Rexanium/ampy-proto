#include <iostream>
#include "ampy/bars/v1/bars.pb.h"

int main() {
    ampy::bars::v1::BarBatch batch;
    std::cout << "C++ import OK: " << batch.DebugString() << std::endl;
    return 0;
}
