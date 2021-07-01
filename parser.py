import requests
import re
import subprocess


def raw(string: str, replace: bool = False) -> str:
    """Returns the raw representation of a string. If replace is true, replace a single backslash's repr \\ with \."""
    r = repr(string)[1:-1]  # Strip the quotes from representation
    if replace:
        r = r.replace('\\\\', '\\')
    return r


def make_file(file_name, content):
    subprocess.Popen('touch {0}'.format(
        file_name), shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('echo "{1}" >> {0}'.format(
        file_name, content), shell=True, stdout=subprocess.PIPE)


LINK = "https://codeforces.com/problemset/problem/1538/G"


def parse_problem(LINK):
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
            outputs.append((all_starts[i]+6, all_ends[i]-1))
        else:
            inputs.append((all_starts[i]+6, all_ends[i]-1))
    current_input_num = 1
    current_output_num = 1
    for item in inputs:
        make_file("{0}.in".format(current_input_num), f.text[item[0]:item[1]])
        current_input_num += 1
    for item in outputs:
        make_file("{0}.out".format(current_output_num),
                  f.text[item[0]:item[1]])
        current_output_num += 1


parse_problem(LINK)
