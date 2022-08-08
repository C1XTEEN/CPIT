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


array_len = input("Length of the array: ")
if('e' in array_len):
    begin_num = float(array_len[:array_len.index('e')])
    end_num = int(array_len[array_len.index('e')+1:])
    array_len = begin_num * (10**end_num)
else:
    array_len = float(array_len)

tp = input("int, ll, double? ")
tp = tp.strip().lower()
print(f"{bcolors.WARNING}Debug: Array Length = {array_len}{bcolors.ENDC}")
if(tp == "int"):
    print(f"{bcolors.WARNING}Debug: Multiplied by 4 (int){bcolors.ENDC}")
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}{array_len*4/(1e6)}{bcolors.ENDC} mb")
else:
    print(f"{bcolors.WARNING}Debug: Multiplied by 8 (ll){bcolors.ENDC}")
    print(f"{bcolors.BOLD}{bcolors.OKGREEN}{array_len*8/(1e6)}{bcolors.ENDC} mb")
