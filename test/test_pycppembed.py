#! /usr/bin/env python
# encoding: utf-8

import pycppembed
import os

def test_pycppembed(testdirectory):
    binary_files = testdirectory.mkdir("binary_files")
    binary_files.copy_files('test/data/binary1.bin')
    binary_files.copy_files('test/data/binary2.bin')
    cpp = testdirectory.mkdir("cpp")
    cpp.copy_files('test/data/main.cpp')
    cmd = ['pycppembed']
    cmd += ['binary_files/binary1.bin']
    cmd += ['binary_files/binary2.bin']
    cmd += ['binaries']
    cmd += ['cpp/']
    cmd += ['-ns test_pycppembed']
    testdirectory.run(' '.join(cmd))

    assert cpp.contains_file('binaries.hpp')
    assert cpp.contains_file('binaries.cpp')
    # We don't expect g++ to be on other os
    if os.name != 'posix':
        return

    cpp.run('g++ main.cpp binaries.cpp -o test_binaries')
    output = cpp.run('./test_binaries')
    assert output.stdout.match('*binary1 size: 42*')
    assert output.stdout.match('*binary2 size: 42*')

def test_pycppembed_help(testdirectory):
    output = testdirectory.run('pycppembed --help')
    assert output.stdout.match('*pycppembed*')
