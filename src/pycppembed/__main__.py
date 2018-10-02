import argparse
import os
import pycppembed.generator

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file '{}' does not exist!".format(arg))
    else:
        return arg

def cli():
    parser = argparse.ArgumentParser(description='cppembed Commandline options')
    parser.add_argument(
        'files',
        nargs='+',
        type=lambda arg: is_valid_file(parser, arg),
        help='file to embed into .cpp file')
    parser.add_argument(
        'output_file',
        help='name of output files - without extension.'
             'Both a cpp and hpp will be created.')
    parser.add_argument(
        '-ns',
        '--namespace',
        help='namespace to use')

    args = parser.parse_args()
    pycppembed.generator.generate(args.files, args.output_file, args.namespace)

if __name__ == "__main__":
    cli()
