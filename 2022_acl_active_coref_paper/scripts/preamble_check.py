"""
This simple script helps me avoid desk rejects by having wrong latex preambles for *ACL conferences.
e.g., Font size being 10pt instead of 11pt.

Sample usage:
    python3 pinafore-papers/scripts/preamble_check.py \
        --style /Users/yoshinarifujinuma/Downloads/naaclhlt2019-latex/naaclhlt2019.tex \
        --draft /Users/yoshinarifujinuma/work/pinafore-papers/2019_naacl_disaster_bootstrap.tex
"""

import argparse


def extract_preambles(fname, preambles):
    for line in open(fname):
        if line.strip().startswith("\\usepackage") or line.startswith("\\documentclass"):
            preambles[line.strip()] = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Options')
    parser.add_argument("--style", type=str, default="", required=True, help="Style latex file (e.g., naaclhlt2019.tex)")
    parser.add_argument("--draft", type=str, default="", required=True, help="Draft latex file")
    args = parser.parse_args()

    preambles = {}
    extract_preambles(args.style, preambles)

    # Extract preambles from the style file
    for line in open(args.draft):
        if line.strip().startswith("\\usepackage") or line.startswith("\\documentclass"):
            preamble = line.strip()
            if preamble in preambles:
                preambles[preamble] = True

    for k, v in preambles.items():
        if not v:
            print("WARNING: Preamble '%s' is not in the draft" % k)
