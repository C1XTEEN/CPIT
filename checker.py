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
    UNDERLINE = '\033[4m',
    WARNING2 = '\u001b[38;5;204m'


def get_tests():
    """
    Gets all the test cases for the current directory
    Test cases must have the .in extension
    """
    input_files = []
    output_files = []
    p = subprocess.Popen(
        'ls', shell=True, stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        line = line.decode("utf-8").strip()
        if(line.endswith(".in")):
            input_files.append(line)
        elif(line.endswith(".out")):
            output_files.append(line)
    return input_files, output_files


def print_input_file(input_file: str):
    """
    Print contents of input file in clean format
    """
    print(bcolors.BOLD + "Input:" + bcolors.ENDC)
    print("=================================")
    print(bcolors.OKBLUE, end="")
    cur_lines = 0
    with open(f"{input_file}") as f:
        for line in f.readlines():
            line = line.strip()
            if(len(line)):
                print(line)
            cur_lines += 1
            if(cur_lines > 50):
                print(bcolors.BOLD + "(Data truncated)")
                break
    print(bcolors.ENDC, end="")
    print("=================================")

def run_test(input_file: str, output_files: list[str], executable: str):
    """
    Run the executable with the given input file
    Capature the output and debug print statements
    """
    p = subprocess.Popen('./{0} < {1}'.format(executable, input_file), shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    results_lines = []
    debug_lines = []
    expected_lines = []
    for line in p.stdout.readlines():
        line = line.decode("utf-8").strip()
        if(len(line)):
            results_lines.append(line)
    for line in p.stderr.readlines():
        line = line.decode("utf-8").strip()
        if(len(line)):
            debug_lines.append(line)
    
    expected_output_file = input_file.replace(".in", ".out")
    if expected_output_file in output_files:
        with open(expected_output_file) as f:
            for line in f.readlines():
                line = line.strip()
                if(len(line)):
                    expected_lines.append(line)
    return results_lines, debug_lines, expected_lines

def determine_status(results_lines, expected_lines):
    """
    Return true if test didn't fail
    Return false if test failed
    Prints out the header for the test case
    """
    if len(expected_lines) == 0:
        print(bcolors.WARNING + "No input file found" + bcolors.ENDC)
        return True
    capatalization = False
    if(len(results_lines) != len(expected_lines)):
        print(bcolors.FAIL + "FAILED" + bcolors.ENDC)
        return False
    else:
        for i in range(len(results_lines)):
            if(results_lines[i].lower() != expected_lines[i].lower()):
                print(bcolors.FAIL + "FAILED" + bcolors.ENDC)
                return False
            elif(results_lines[i] != expected_lines[i]):
                capatalization = True
    # Test case passed
    print(bcolors.OKGREEN + "ACCEPTED" + bcolors.ENDC, end="")
    if(capatalization):
        print(bcolors.WARNING + " (capatalization)" + bcolors.ENDC)
    else:
        print()
    return True

def print_results(results_lines, debug_lines, expected_lines):
    current_line = 0
    print(bcolors.BOLD + "Results:" + bcolors.ENDC)
    print("=================================")
    print(bcolors.OKBLUE, end="")
    for line in results_lines:
        if len(expected_lines) != 0 and (current_line >= len(expected_lines) or line.lower() != expected_lines[current_line].lower()):
            print(bcolors.WARNING2 + line + bcolors.OKBLUE)
        else:
            print(line)
        current_line += 1
        if(current_line > 50):
            print(bcolors.BOLD + "(Data truncated)")
            break
    print(bcolors.ENDC, end="")
    print("=================================")

    if len(expected_lines) > 0:
        current_line = 0
        print(bcolors.BOLD + "Expected:" + bcolors.ENDC)
        print("=================================")
        print(bcolors.OKBLUE, end="")
        for line in expected_lines:
            if(current_line >= len(results_lines) or line.lower() != results_lines[current_line].lower()):
                print(bcolors.WARNING2 + line + bcolors.OKBLUE)
            else:
                print(line)
            current_line += 1
            if(current_line > 50):
                print(bcolors.BOLD + "(Data truncated)")
                break
        print(bcolors.ENDC, end="")
        print("=================================")

    if(len(debug_lines) > 0):
        has_debug = True
        print(bcolors.BOLD + "Debug:" + bcolors.ENDC)
        print("=================================")
        print(bcolors.WARNING, end="")
        for line in debug_lines:
            print(line)
        print(bcolors.ENDC, end="")
        print("=================================")
    print()

def test_code(executable: str):
    """
    Given all test files, run code on it and see if output is correct
    """
    input_files, output_files = get_tests()
    successful = True
    has_debug = False
    for test in input_files:
        results_lines, debug_lines, expected_lines = run_test(test, output_files, executable)
        print("Running on test {0}{1}{2}\nVerdict: ".format(
            bcolors.BOLD, test, bcolors.ENDC), end="")
        successful &= determine_status(results_lines, expected_lines)
        print_input_file(test)
        print_results(results_lines, debug_lines, expected_lines)
        if len(debug_lines) > 0:
            has_debug = True
        
    if successful == False:
        print("{0}FAILED SAMPLES{1}".format(bcolors.FAIL, bcolors.ENDC))
    else:
        print("{0}ALL SAMPLES PASSED{1}".format(bcolors.OKGREEN, bcolors.ENDC))
    if(has_debug):
        print(bcolors.WARNING +
              "WARNING: YOUR CODE PRINTED DEBUG STATEMENTS" + bcolors.ENDC)


if __name__ == "__main__":
    executable = sys.argv[1]
    test_code(executable)
