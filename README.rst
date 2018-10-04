pycppembed
==========
.. image:: ./icon.png

.. image:: https://img.shields.io/appveyor/ci/SteinwurfApS/pycppembed/master.svg?style=flat-square&logo=appveyor
    :target: https://ci.appveyor.com/project/SteinwurfApS/pycppembed

.. image:: https://img.shields.io/travis-ci/steinwurf/pycppembed/master.svg?style=flat-square&logo=travis
    :target: https://travis-ci.org/steinwurf/pycppembed

pycppembed is a python c++ resource compiler.

It can be used to embed images or html directly into an application or library.

Install
-------

One way of installing this tool is to run the the following commands::

    python setup.py bdist_wheel --universal
    python -m pip install dist/pycppembed-*.whl

Usage
-----

The pycppembed tool takes the following commandline arguments::

    usage: pycppembed [-h] [-ns NAMESPACE]
                    files [files ...] class_name output_path

    Commandline options

    positional arguments:
    files                 file to embed into .cpp file
    class_name            name of the class to contain the files. This will
                            likewise becomethe name of the resulting cpp and hpp
                            file.
    output_path           output folder in which the c++ files should be
                            created.

    optional arguments:
    -h, --help            show this help message and exit
    -ns NAMESPACE, --namespace NAMESPACE
                            namespace to use (default: pycppembed)



Let's say we have a file called ``icon.png`` which we would like to embed into a
c++ library.

First call the pycppembed tool::

    mkdir sources
    pycppembed icon.png images sources/

This would then create two files in the sources folder::

    ls sources/
    > images.cpp  images.hpp

Let's make a small application which simply prints out the size of the embedded
image file::

    #include "images.hpp"

    #include <cassert>
    #include <iostream>

    int main()
    {
        assert(pycppembed::images::has_file("icon.png"));
        auto icon = pycppembed::images::get_file("icon.png");
        std::cout << "icon size: " << icon.m_size << std::endl;
        return 0;
    }


We add this to the file sources/main.cpp, and compile the project::

    cd sources/
    g++ -std=c++11 main.cpp images.cpp -o example
    ./example
    > Size of img: 15786
