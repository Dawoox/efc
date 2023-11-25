import shutil
import subprocess
import sys
from typing import List

TEXT_RED = '\033[31m'
TEXT_GREEN = '\033[32m'
TEXT_CLEAR = '\033[0m'


def get_functions(bin_path: str) -> List[str]:
    nm_process = subprocess.run(['nm', '-C', bin_path], stdout=subprocess.PIPE)
    lines = nm_process.stdout.decode().split('\n')
    f_list = [line.split(' ')[-1] for line in lines if ' U ' in line]
    f_list = [fx.split(' ')[-1] for fx in f_list if not fx.startswith('__')]
    f_list = [fx.split('@')[0] for fx in f_list]
    return f_list


def parse_file(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines


def find_authorized_functions(functions_list: List[str], a_filepath: str) -> List[str]:
    af = parse_file(a_filepath)
    bf_found = [func for func in functions_list if func not in af]
    return bf_found


def is_tool_present(tool_name: str) -> bool:
    return shutil.which(tool_name) is not None


def print_usage() -> None:
    print('Usage: python3 main.py /path/to/your/binary [/path/to/banned_functions.txt]')


def run_analysis(bin_path: str, bf_path: str) -> None:
    print(f'Analyzing {bin_path}...')
    f_list = get_functions(bin_path)
    print(f'Found {len(f_list)} functions')
    print('Checking for banned functions...')
    a_list = find_authorized_functions(f_list, bf_path)
    if len(a_list) == 0:
        print(f'{TEXT_GREEN}No banned functions found{TEXT_CLEAR}')
        exit(0)
    else:
        print(f'{TEXT_RED}Found {len(a_list)} banned functions !{TEXT_CLEAR}')
        print(f'{TEXT_RED}Banned functions:{TEXT_CLEAR}')
        for bf_found in a_list:
            print(TEXT_RED + bf_found + TEXT_CLEAR)
        exit(1)


def main():
    if len(sys.argv) >= 2 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print_usage()
        exit(0)
    if not is_tool_present('nm'):
        print('Cannot find nm executable, please install nm')
        exit(1)
    if len(sys.argv) == 3:
        binary_path = sys.argv[1]
        a_path = sys.argv[2]
        run_analysis(binary_path, a_path)
    if len(sys.argv) == 2:
        binary_path = sys.argv[1]
        a_path = './bonus/authorized_functions.txt'
        run_analysis(binary_path, a_path)
    print_usage()
    exit(1)


if __name__ == '__main__':
    main()
