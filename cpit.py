import sys
from parser import parse_problem, parse_contest
from checker import test_code
from rating import get_difficulty
from mb import get_mem

if __name__ == "__main__":
    if sys.argv[1] == "parse":
        parse_type = sys.argv[2]
        parse_type = parse_type.lower()
        if(parse_type == 'o' or parse_type == "p" or parse_type == "1"):
            parse_problem(sys.argv[3])
        else:
            parse_contest(sys.argv[3])
    elif sys.argv[1] == "checker":
        executable = sys.argv[2]
        test_code(executable)
    elif sys.argv[1] == "rating":
        get_difficulty()
    elif sys.argv[1] == "mem":
        get_mem()