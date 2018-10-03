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



Let's say we have a file called logo.png which we would like to embed into a
c++ library.

First call the pycppembed tool::

    mkdir cpp
    pycppembed logo.png image_files cpp/

This would then create two files in the cpp folder::

    ls cpp/
    > image_files.cpp  image_files.hpp

Let's make a small application which simply prints out the size of the embedded
image file::

    #include "image_files.hpp"

    #include <cassert>
    #include <iostream>

    int main()
    {
        auto img = pycppembed::image_files::get_file("logo.png");

        /// if the given file wasn't found the pointer will be null.
        assert(img.data != nullptr);

        std::cout << "Size of img: " << img.size << std::endl;
        return 0;
    }

We add this to the file cpp/main.cpp, and compile the project::

    g++ main.cpp image_files.cpp -o embedded_img
    ./embedded_img
    > Size of img: 0
