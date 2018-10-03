#include "binaries.hpp"

#include <cassert>
#include <iostream>

int main()
{
    auto binary1 = test_pycppembed::binaries::get_file("binary_files/binary1.bin");
    assert(binary1.data != nullptr);
    std::cout << "binary1 size: " << binary1.size << std::endl;

    auto binary2 = test_pycppembed::binaries::get_file("binary_files/binary2.bin");
    assert(binary2.data != nullptr);
    std::cout << "binary2 size: " << binary2.size << std::endl;
    return 0;
}
