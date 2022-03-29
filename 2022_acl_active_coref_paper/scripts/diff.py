import os
import sys

if __name__ == "__main__":
    compare = ""
    if len(sys.argv) == 2:
        paper = sys.argv[1]
        command = 'git log --author "`git config user.name`"' + \
            ' -n 1 --pretty=oneline --abbrev-commit %s* %s' % \
            (paper, paper)
        last_commit = os.popen(command).read().split()[0]
    elif len(sys.argv) == 3:
        paper = sys.argv[1]
        last_commit = sys.argv[2]
    elif len(sys.argv) == 4:
        paper = sys.agrv[1]
        last_commit = sys.argv[2]
        compare = sys.agrv[3]
    else:
        print("USAGE: diff.py paper [old_version] [new_version]")
        print("\t if no versions are given, compares head to your last commit")
        print("\t if only one version is given, compares head to that version")

    print("Your last commit on %s was %s" % (paper, last_commit))

    command = "./scripts/git-latexdiff --main " + \
        "%s.tex -b -o %s.diff.pdf --ignore-latex-errors -v %s" % \
        (paper, paper, last_commit)
    if compare != "":
        command = "%s %s" % (command, compare)

    print(command)
    print(os.popen(command).read())
