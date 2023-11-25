import subprocess
from typing import List


def get_functions(binary_path: str) -> List[str]:
    result = subprocess.run(['nm', '-C', binary_path], stdout=subprocess.PIPE)
    lines = result.stdout.decode().split('\n')
    functions = [line.split(' ')[-1] for line in lines if ' T ' in line]
    return functions


binary_path = '/path/to/your/binary'
functions = get_functions(binary_path)
for function in functions:
    print(function)
