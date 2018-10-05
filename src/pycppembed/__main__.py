import argparse
import os
import glob
import pycppembed.generator

def does_exists(parser, arg):
    if not os.path.exists(arg):
        parser.error("'{}' does not exist!".format(arg))
    else:
        return arg

def is_valid_dir(parser, arg):
    arg = does_exists(parser, arg)
    if not os.path.isdir(arg):
        parser.error("'{}' is not a directory!".format(arg))
    else:
        return arg

def cli():
    parser = argparse.ArgumentParser(
        description='Commandline options',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--cwd',
        '-c',
        type=lambda arg: is_valid_dir(parser, arg),
        default='.',
        help='Working directory. This can be used for creating proper keys for '
             'each file.')
    args, remaining = parser.parse_known_args()

    old_cwd = os.getcwd()
    os.chdir(args.cwd)

    parser.add_argument(
        'inputs',
        nargs='+',
        help='file to embed into .cpp file')
    parser.add_argument(
        'class_name',
        help='name of the class to contain the files. This will likewise become'
             'the name of the resulting cpp and hpp file.')
    parser.add_argument(
        'output_path',
        type=lambda arg: is_valid_dir(parser, arg),
        help='output folder in which the c++ files should be created.')
    parser.add_argument(
        '-ns',
        '--namespace',
        default='pycppembed',
        help='namespace to use')

    args = parser.parse_args(remaining)

    files = sum([glob.glob(i) for i in args.inputs], [])
    print("Embedding the following files:")
    for f in sorted(files):
        print(f)

    pycppembed.generator.generate(
        files=files,
        class_name=args.class_name,
        output_path=args.output_path,
        namespace=args.namespace)

    os.chdir(old_cwd)

if __name__ == "__main__":
    cli()
