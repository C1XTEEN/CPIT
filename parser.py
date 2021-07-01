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


LINK = "https://codeforces.com/contest/50/problem/A"


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
        print(f.text[all_starts[i]:all_ends[i]])
    for i in range(len(all_starts)):
        if(i & 1):
            outputs.append((all_starts[i], all_ends[i]))
        else:
            inputs.append((all_starts[i], all_ends[i]))
    current_input_num = 1
    current_output_num = 1
    for item in inputs:
        s = f.text[item[0]:item[1]].replace("<br />", "").replace("<pre>", "")
        if(len(s) and s[0] == '\n'):
            s = s[1:]
        if(len(s) and s[-1] == '\n'):
            s = s[:-1]
        make_file("{0}.in".format(current_input_num), s)
        current_input_num += 1
    for item in outputs:
        s = f.text[item[0]:item[1]].replace("<br />", "").replace("<pre>", "")
        if(len(s) and s[0] == '\n'):
            s = s[1:]
        if(len(s) and s[-1] == '\n'):
            s = s[:-1]
        make_file("{0}.out".format(current_output_num), s)
        current_output_num += 1


parse_problem(LINK)
