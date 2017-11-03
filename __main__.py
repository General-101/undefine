import os
import argparse
from SharpCleaner import SharpCleaner


def test(p_args):
    defined = p_args.define if p_args.define is not None else []
    undefined = p_args.undef if p_args.undef is not None else []
    keys = dict([(n, True) for n in defined] + [(n, False) for n in undefined])
    print("Checking for applying the following name definitions:")
    for name, value in keys.items():
        print(str.format("#{0} {1}", 'define' if value else 'undef', name))
    print('...', end='\r')
    cleaner = SharpCleaner(keys)
    results = cleaner.clean_folder(p_args.path, False)
    body_lines = 0
    total_lines = 0
    files_count = 0
    error_files = []
    for result in results:
        if result is not None:
            if not result['success']:
                error_files.append(result['file'])
            else:
                body_lines += result['body_lines']
                total_lines += result['total_lines']
                if result['total_lines'] > 0:
                    files_count += 1
    print(str.format("Completed. {0} code lines can be removed. {1} files and {2} lines would be affected",
                     body_lines, files_count, total_lines))
    if len(error_files) > 0:
        print("Failed on these files:")
        for file in error_files:
            print(file)


def apply(p_args):
    print("apply")
    print(p_args)


def scan(p_args):
    print("stats")
    print(p_args)


def _add_name_definition_args(p):
    p.add_argument('-d', '--define', action='append', metavar='name', help='define global preprocessor var')
    p.add_argument('-u', '--undef', action='append', metavar='name', help='undefine global preprocessor var')


parser = argparse.ArgumentParser()
parser.add_argument('path', default=os.getcwd(), metavar='path', nargs='?',
                    help='working path, current working folder by default')
subparsers = parser.add_subparsers(help='commands')

parser_check = subparsers.add_parser('test', help='test command')
_add_name_definition_args(parser_check)
parser_check.set_defaults(act=test)

parser_clean = subparsers.add_parser('apply', help='apply command')
_add_name_definition_args(parser_clean)
parser_clean.set_defaults(act=apply)

parser_stats = subparsers.add_parser('scan', help='scan command')
parser_stats.set_defaults(act=scan)

args = parser.parse_args()
if hasattr(args, 'act'):
    args.act(args)



