# Removes comments from LaTeX files

from glob import glob
import re
import sys

kCOMMENT = re.compile(r"(?<!\\)%.*\n")
kSTRIP = re.compile(r"\\.*comment{")
strippable = set(["\\hidetext{", "\\ignore{"])


def remove_command(command, text):
    # If the command isn't here, do nothing
    if not command in text:
        return text

    before, after = text.split(command, 1)
    num_close = 1
    while num_close > 0:
        mid, after = after.split("}", 1)
        num_close -= 1
        num_close += sum(1 for x in mid if x == '{')
        if before.endswith("\n") and after.startswith("\n"):
            after = after.strip()

    return before + after

if __name__ == "__main__":
    # gather set of strippable commands
    for ii in glob("%s/*" % sys.argv[1]) + \
            ["%s.tex" % sys.argv[1].split("/")[0]]:
        strippable = strippable | set(kSTRIP.findall(open(ii).read()))
    print(strippable)

    for ii in glob("%s/*" % sys.argv[1]) + \
            ["%s.tex" % sys.argv[1].split("/")[0]]:
        raw_file = open(ii).read().replace(r"\n%\n", r"\n")
        print("\n".join(kCOMMENT.findall(raw_file)[:5]))
        new_text = kCOMMENT.sub("", raw_file)

        strips_found = 1
        while strips_found > 0:
            strips_found = 0
            for jj in strippable:
                new_text = remove_command(jj, new_text)
                if jj in new_text:
                    strips_found += 1
            print("Strips %i" % strips_found)

        o = open(ii, 'w')
        o.write(new_text)
        o.close()

        print(ii, len(new_text))
