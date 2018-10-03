import argparse
import os
import pycppembed.generator

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file '{}' does not exist!".format(arg))
    else:
        return arg

def cli():
    parser = argparse.ArgumentParser(
        description='Commandline options',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'files',
        nargs='+',
        type=lambda arg: is_valid_file(parser, arg),
        help='file to embed into .cpp file')
    parser.add_argument(
        'class_name',
        help='name of the class to contain the files. This will likewise become'
             'the name of the resulting cpp and hpp file.')
    parser.add_argument(
        'output_path',
        help='output folder in which the c++ files should be created.')
    parser.add_argument(
        '-ns',
        '--namespace',
        default='pycppembed',
        help='namespace to use')

    args = parser.parse_args()
    pycppembed.generator.generate(
        files=args.files,
        class_name=args.class_name,
        output_path=args.output_path,
        namespace=args.namespace)

if __name__ == "__main__":
    cli()
