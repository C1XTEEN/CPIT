import subprocess
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def raw(string: str, replace: bool = False) -> str:
    """Returns the raw representation of a string. If replace is true, replace a single backslash's repr \\ with \."""
    r = repr(string)[1:-1]  # Strip the quotes from representation
    if replace:
        r = r.replace('\\\\', '\\')
    return r


def get_tests():
    """
    Gets all the test cases for the current directory
    Test cases must have the .in extension
    """
    tests = []
    p = subprocess.Popen(
        'ls', shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        line = line.decode("utf-8").strip()
        if('.in' in line):
            tests.append(line[:-3])
    return tests


def test_code(tests, executable):
    """
    Given all test files, run code on it and see if output is correct
    """
    failed_case = False
    for test in tests:
        p = subprocess.Popen('./{0} < {1}.in'.format(executable, test), shell=True,
                             stdout=subprocess.PIPE)
        results_lines = []
        expected_lines = []
        print("Running on test {0}{1}{2}\nVerdict: ".format(
            bcolors.BOLD, test, bcolors.ENDC), end="")
        for line in p.stdout.readlines():
            line = line.decode("utf-8").strip()
            if(len(line)):
                results_lines.append(line)
        with open("{0}.out".format(test)) as f:
            for line in f.readlines():
                line = line.strip()
                if(len(line)):
                    expected_lines.append(line)
        failed = False
        capatalization = False
        if(len(results_lines) != len(expected_lines)):
            print(bcolors.FAIL + "FAILED" + bcolors.ENDC)
            failed = True
        else:
            for i in range(len(results_lines)):
                if(results_lines[i].lower() != expected_lines[i].lower()):
                    print(bcolors.FAIL + "FAILED" + bcolors.ENDC)
                    failed = True
                    break
                elif(results_lines[i] != expected_lines[i]):
                    capatalization = True
        if(failed == False):
            print(bcolors.OKGREEN + "ACCEPTED" + bcolors.ENDC, end="")
            if(capatalization):
                print(bcolors.WARNING + " (capatalization)" + bcolors.ENDC)
            else:
                print()
        else:
            failed_case = True
            print(bcolors.BOLD + "Input:" + bcolors.ENDC)
            print("=================================")
            print(bcolors.OKBLUE, end="")
            with open("{0}.in".format(test)) as f:
                for line in f.readlines():
                    line = line.strip()
                    if(len(line)):
                        print(line)
            print(bcolors.ENDC, end="")
            print("=================================")
        print(bcolors.BOLD + "Results:" + bcolors.ENDC)
        print("=================================")
        print(bcolors.OKBLUE, end="")
        for line in results_lines:
            print(line)
        print(bcolors.ENDC, end="")
        print("=================================")

        print(bcolors.BOLD + "Expected:" + bcolors.ENDC)
        print("=================================")
        print(bcolors.OKBLUE, end="")
        for line in expected_lines:
            print(line)
        print(bcolors.ENDC, end="")
        print("=================================")
        print()
    if(failed_case):
        print("{0}FAILED SAMPLES{1}".format(bcolors.FAIL, bcolors.ENDC))
    else:
        print("{0}ALL SAMPLES PASSED{1}".format(bcolors.OKGREEN, bcolors.ENDC))


executable = sys.argv[1]
tests = get_tests()
test_code(tests, executable)
