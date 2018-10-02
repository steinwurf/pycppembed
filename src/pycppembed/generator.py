import os
import array

HPP_FILE ="""// Auto generated, do not modify
#pragma once

#include <cstdint>
#include <map>
#include <string>

namespace {namespace}
{{
class {class_name}
{{
private:
    {declare_file_variables}
public:

    struct file
    {{
        const uint8_t* data = nullptr;
        uint64_t size = 0;
    }};

    static file get_file(const std::string& name)
    {{
        if (m_files.count(name) == 0)
            return file();
        return m_files.at(name);
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
MAP_ENTRY = "    {{ \"{file_name}\", {{ {class_name}::{name}_data, {class_name}::{name}_size}} }},\n"

def generate(embed_files, output_file, namespace):

    class_name = os.path.basename(output_file)
    map_entries = ""
    declare_file_variables = ""
    define_file_variables = ""

    for file_name in embed_files:
        name = file_name.replace('.', '_')
        data = array.array('B')
        with open(file_name, 'rb') as f:
            data.fromstring(f.read())
        size = len(data)

        map_entries += MAP_ENTRY.format(
            class_name=class_name,
            name=name,
            file_name=file_name
        )
        declare_file_variables += FILE_VARIABLE_DECLARATION.format(
            name=name,
            size=size
        )

        define_file_variables += FILE_VARIABLE_DEFINITION.format(
            class_name=class_name,
            name=name,
            size=size,
            data=', '.join([hex(d) for d in data]),
        )

    hpp_content = HPP_FILE.format(
        namespace=namespace,
        class_name=class_name,
        map_entries=map_entries,
        define_file_variables=define_file_variables,
        declare_file_variables=declare_file_variables,
    )
    cpp_content = CPP_FILE.format(
        namespace=namespace,
        class_name=class_name,
        map_entries=map_entries,
        define_file_variables=define_file_variables,
        declare_file_variables=declare_file_variables,
    )

    with open('{}.hpp'.format(output_file), 'w') as f:
        f.write(hpp_content)
    with open('{}.cpp'.format(output_file), 'w') as f:
        f.write(cpp_content)
