#include "binaries.hpp"

#include <cassert>
#include <iostream>

int main()
{
    auto binary1 = test_pycppembed::binaries::get_file("binary1.bin");
    std::cout << "binary1 size: " << binary1.m_size << std::endl;
    std::cout << "binary1 first byte: " << (int)binary1.m_data[0] << std::endl;
    std::cout << "binary1 last byte: " << (int)binary1.m_data[binary1.m_size - 1] << std::endl;

    auto binary2 = test_pycppembed::binaries::get_file("binary2.bin");
    std::cout << "binary2 size: " << binary2.m_size << std::endl;
    std::cout << "binary2 first byte: " << (int)binary2.m_data[0] << std::endl;
    std::cout << "binary2 last byte: " << (int)binary2.m_data[binary2.m_size - 1] << std::endl;
    std::cout << "file names: ";
    for (auto file_name : test_pycppembed::binaries::file_names())
    {
        std::cout << file_name << " ";
    }
    std::cout << std::endl;
    return 0;
}
