from subprocess import Popen, PIPE
from random import random, seed, shuffle
from tqdm import tqdm
from pprint import pprint
import json
import time

SMALL_TEST_COUNT = 100
MEDIUM_TEST_COUNT = 100
LARGE_TEST_COUNT = 10
SEED = 0
TEST_FILE = 'tests.json'

seed(SEED)

class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'{self.name}: {time.time() - self.t0:.2f}')

def generate_random_input(max_instances=10000, max_elements=2000, max_start=10**7 - 1, max_end=10**7, max_value=10**7):
    '''returns a string that is valid input'''
    instances = int(random() * (max_instances)) + 1
    test = f'{instances}'

    for _ in range(instances):
        size = int(random() * (max_elements)) + 1
        # size = max_elements - 1

        test += f'\n{size}'
        for i in range(size):
            start = int(random() * max_start) + 1
            # start = i
            end = int(random() * (max_end - start)) + start + 1
            # end = i + 1
            # weight = max_value
            weight = int(random() * max_value) + 1
            test += f'\n{start} {end} {weight}'

    return test + '\n'

def shell(cmd, stdin=None):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = p.communicate(input=stdin.encode() if stdin else None)
    return out.decode('utf8'), err.decode('utf8')

get_python = lambda testCase: shell('./WeightedS', stdin=testCase)
get_cpp = lambda testCase: shell('./Weighted', stdin=testCase)

print('Building:')
buildOutput, buildError = shell('make build')
if buildOutput:
    print(buildOutput)
if buildError:
    print('Error running `make build`:\n')
    print(buildError)
    exit()

tests = dict()

# manual tests
tests['given-test-0'] = {'input':'2\n1\n1 4 5\n3\n1 2 1\n3 4 2\n2 6 4\n', 'output':"5\n5\n"}

tests['edge-test-0'] = {'note':'Make sure you can handle results over 2^31', 'input':"1\n4\n7 9 1000000000\n4 7 1000000000\n1 3 1000000000\n3 8 1000000000\n", 'output':"3000000000\n"}

# random tests

for i in tqdm(range(SMALL_TEST_COUNT)):
    test = generate_random_input(max_instances=1, max_elements=10, max_start=10, max_end=10, max_value=10)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'small-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(MEDIUM_TEST_COUNT)):
    test = generate_random_input(max_instances=10, max_elements=20, max_start=20, max_end=20, max_value=100)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'medium-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(LARGE_TEST_COUNT)):
    test = generate_random_input(max_instances=100)
    # test = generate_random_input(max_instances=100, max_elements=2000, max_start=1000 - 1, max_end=1000, max_value=10**4)
    # with Timer('python'):
    python, p_err = get_python(test)
    # with Timer('c'):
    cpp, c_err1 = get_cpp(test)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        # print(f'Input\n{test}')
        exit()
    tests[f'large-test-{i}'] = {'input':test, 'output':python}

# pprint(tests)
with open(TEST_FILE, 'w+') as f:
    json.dump(tests, f, indent=4)
