import requests
import re
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


def make_file(file_name, content):
    subprocess.Popen('touch {0}'.format(
        file_name), shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('> {0}'.format(
        file_name), shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('echo "{1}" >> {0}'.format(
        file_name, content), shell=True, stdout=subprocess.PIPE)


LINK = "https://codeforces.com/contest/50/problem/A"


def parse_problem(LINK, path="./"):
    name = ""
    for i in range(len(LINK)-1, -1, -1):
        if(LINK[i] == '/'):
            break
        name += LINK[i]
    f = requests.get(LINK)
    all_starts = [m.start() for m in re.finditer("<pre>", f.text)]
    all_ends = [m.start() for m in re.finditer("</pre>", f.text)]
    inputs = []
    outputs = []
    for i in range(len(all_starts)):
        if(i & 1):
            outputs.append((all_starts[i], all_ends[i]))
        else:
            inputs.append((all_starts[i], all_ends[i]))
    current_input_num = 1
    current_output_num = 1
    for i in range(len(inputs)):
        item = inputs[i]
        s = f.text[item[0]:item[1]].replace("<br />", "").replace("<pre>", "")
        if(len(s) and s[0] == '\n'):
            s = s[1:]
        if(len(s) and s[-1] == '\n'):
            s = s[:-1]
        print("Parsing input {0}{1}{2}".format(
            bcolors.BOLD, current_input_num, bcolors.ENDC))
        print("=================================")
        print("{0}{1}{2}".format(bcolors.OKBLUE, s, bcolors.ENDC))
        print("=================================")
        make_file("{0}{1}.in".format(path, current_input_num), s)
        current_input_num += 1

        item = outputs[i]
        s = f.text[item[0]:item[1]].replace("<br />", "").replace("<pre>", "")
        if(len(s) and s[0] == '\n'):
            s = s[1:]
        if(len(s) and s[-1] == '\n'):
            s = s[:-1]
        print("Parsing output {0}{1}{2}".format(
            bcolors.BOLD, current_output_num, bcolors.ENDC))
        print("=================================")
        print("{0}{1}{2}".format(bcolors.OKBLUE, s, bcolors.ENDC))
        print("=================================")
        make_file("{0}{1}.out".format(path, current_output_num), s)
        current_output_num += 1


def parse_contest(ID):
    LINK = "https://codeforces.com/contest/"
    LINK += str(ID)
    f = requests.get(LINK)
    search_link = "/contest/{0}/problem/".format(ID)
    all_starts = [m.start() for m in re.finditer(
        search_link, f.text)]
    problems = []
    for item in all_starts:
        cur_prob = ""
        cur_add = 0
        while(f.text[item+len(search_link)+cur_add] != '"'):
            cur_prob += f.text[item+len(search_link)+cur_add]
            cur_add += 1
        if((len(problems) and problems[-1] == cur_prob) == False):
            problems.append(cur_prob)
    for problem in problems:
        subprocess.Popen('mkdir {0}'.format(problem),
                         shell=True, stdout=subprocess.PIPE)
        subprocess.Popen('touch {0}/{1}.cpp'.format(
            problem, problem.lower()), shell=True, stdout=subprocess.PIPE)
        problem_link = "https://codeforces.com/contest/{0}/problem/{1}".format(
            ID, problem)
        print("{0}Parsing problem {1}{2}{3}".format(bcolors.HEADER,
                                                    bcolors.BOLD, problem, bcolors.ENDC))
        parse_problem(problem_link, "{0}/".format(problem))
    print("{0}Finished parsing contest{1}".format(
        bcolors.OKGREEN, bcolors.ENDC))


parse_type = sys.argv[1]
parse_type = parse_type.lower()
if(parse_type == 'o' or parse_type == "p" or parse_type == "1"):
    parse_problem(sys.argv[2])
else:
    parse_contest(sys.argv[2])
