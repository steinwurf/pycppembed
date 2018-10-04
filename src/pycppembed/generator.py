import os
import array

HPP_FILE ="""// Auto generated, do not modify
#pragma once

#include <algorithm>
#include <cassert>
#include <cstdint>
#include <map>
#include <string>
#include <vector>

namespace {namespace}
{{
class {class_name}
{{
private:
    {declare_file_variables}
public:

    struct file
    {{
        file(const uint8_t* data, uint64_t size) :
            m_data(data),
            m_size(size)
        {{
            assert(m_data != nullptr);
        }}
        const uint8_t* m_data;
        uint64_t m_size;
    }};

    static bool has_file(const std::string& name)
    {{
        return m_files.count(name) == 1;
    }}

    static file get_file(const std::string& name)
    {{
        return m_files.at(name);
    }}

    static std::vector<std::string> file_names()
    {{
        std::vector<std::string> file_names;
        for(auto const& file: m_files) file_names.push_back(file.first);
        return file_names;
    }}

private:

    const static std::map<std::string, file> m_files;
}};
}}
"""

CPP_FILE ="""// Auto generated, do not modify
#include "{class_name}.hpp"
namespace {namespace}
{{
    {define_file_variables}
const std::map<std::string, {class_name}::file> {class_name}::m_files = {{
{map_entries}}};
}}
"""

FILE_VARIABLE_DECLARATION = """
    static const uint8_t {name}_data[{size}];
    static const uint64_t {name}_size;
"""
FILE_VARIABLE_DEFINITION = """
const uint8_t {class_name}::{name}_data[{size}] = {{{data}}};
const uint64_t {class_name}::{name}_size = {size};
"""
MAP_ENTRY = "    {{ \"{file_name}\", {class_name}::file{{ {class_name}::{name}_data, {class_name}::{name}_size}} }},\n"

def generate(files, output_path, class_name, namespace):
    embed_files = []
    for filename in files:
        name = filename.replace('.', '_').replace(os.sep, '_')
        data = array.array('B')
        with open(filename, 'rb') as f:
            data.fromstring(f.read())
        embed_files.append((filename, name, data))

    with open('{}.hpp'.format(os.path.join(output_path, class_name)), 'w') as f:
        f.write(generate_hpp(embed_files, class_name, namespace))
    with open('{}.cpp'.format(os.path.join(output_path, class_name)), 'w') as f:
        f.write(generate_cpp(embed_files, class_name, namespace))

def generate_cpp(embed_files, class_name, namespace):
    map_entries = ""
    define_file_variables = ""

    for file_name, var_name, data in embed_files:
        size = len(data)

        map_entries += MAP_ENTRY.format(
            class_name=class_name,
            name=var_name,
            file_name=file_name
        )

        define_file_variables += FILE_VARIABLE_DEFINITION.format(
            class_name=class_name,
            name=var_name,
            size=size,
            data=', '.join([hex(d) for d in data]),
        )

    return CPP_FILE.format(
        namespace=namespace,
        class_name=class_name,
        map_entries=map_entries,
        define_file_variables=define_file_variables,
    )

def generate_hpp(embed_files, class_name, namespace):
    declare_file_variables = ""

    for _, var_name, data in embed_files:
        size = len(data)
        declare_file_variables += FILE_VARIABLE_DECLARATION.format(
            name=var_name,
            size=size
        )

    return HPP_FILE.format(
        namespace=namespace,
        class_name=class_name,
        declare_file_variables=declare_file_variables,
    )
