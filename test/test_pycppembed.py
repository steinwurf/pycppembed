#! /usr/bin/env python
# encoding: utf-8

import pycppembed

def test_pycppembed(testdirectory):
    cmd = 'pycppembed --help'
    output = testdirectory.run(cmd)
    print(output)
    print(dir(output))
    print(type(output))
    assert output.stdout.match('*pycppembed*')
