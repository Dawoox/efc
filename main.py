import subprocess, shutil, sys
from typing import List


def get_functions(bin_path: str) -> List[str]:
    nm_process = subprocess.run(['nm', '-C', bin_path], stdout=subprocess.PIPE)
    lines = nm_process.stdout.decode().split('\n')
    f_list = [line.split(' ')[-1] for line in lines if ' U ' in line]
    f_list = [fx.split(' ')[-1] for fx in f_list if not fx.startswith('__')]
    return f_list


def is_tool_present(tool_name: str) -> bool:
    return shutil.which(tool_name) is not None


def print_usage() -> None:
    print('Usage: python3 main.py /path/to/your/binary')


if __name__ == '__main__':
    if (len(sys.argv) != 2) or (sys.argv[1] == '-h') or (sys.argv[1] == '--help'):
        print_usage()
        exit(0)
    binary_path = sys.argv[1]
    if not is_tool_present('nm'):
        print('Cannot find nm executable, please install nm')
        exit(1)
    functions = get_functions(binary_path)
    for function in functions:
        print(function)
