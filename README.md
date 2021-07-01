# CP-CLI
## What it does
Command line interface for competitive programming

Allows you to download input/output from Codeforces, automatically run code against .in and .out samples files, and gives you the verdict

## How to use it
Alias:
```
alias runcode = python3 checker.py
alias cfparse = python3 parser.py
```

```
runcode [executable]
// runs code with executable against in and out files in directory
```

```
cfparse [1, o, or p] problem_link
// parses a problem link
cfparse [c] contest_id
// parses all problems in the contest
```
