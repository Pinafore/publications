
from collections import defaultdict
import sys
import argparse

kUNACCEPTABLE_OUTPUT = {"inbook": set(["url"]),
                        "inproceedings": set(["isbn", "series", "pages", "month", "address", "location", "editor", "tagline", "abstract", "publisher", "url", "doi", "organization"]),
                        "book": set(["isbn"]),
                        "misc": set([]),
                        "phdthesis": set(["url"]),
                        "mastersthesis": set(["url"]),
                        "techreport": set([]),
                        "article": set(["issn", "doi", "url", "abstract"])}

doi_fields = ["url", "doi", "eprint"]

def bracket_count(s):
    return sum(1 for x in s if x=="{") - sum(1 for x in s if x=="}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("old", type=str, help="Path to old bib file")
    parser.add_argument("new", type=str, help="Path to new bib file")
    parser.add_argument("--doi", action="store_true", help="Keep URLs/DOIs")
    args = parser.parse_args()

    output = defaultdict(list)
    key = ""
    in_open_field = False
    with open(args.old) as infile:
        for ii in infile:
            if ii.startswith("@"):
                kind = ii.split("{")[0][1:].lower()
                key = ii.split("{")[1].strip()[:-1]
                in_open_field = False
                if (key, kind) in output:
                    print("Duplicate key: %s" % key)
            elif in_open_field:
                output[(key, kind)][-1] += ii
                if bracket_count(ii) < 0:
                    in_open_field = False
                    bad = output[(key, kind)][-1].strip()
                    # print("Closing %s ... %s" % (bad[:20], bad[-20:]))
            elif ii.startswith("%"):
                continue
            elif "=" in ii:
                field = ii.split("=")[0].strip().lower()
                acceptable = (kind not in kUNACCEPTABLE_OUTPUT) or \
                    (field not in kUNACCEPTABLE_OUTPUT[kind])
                doi_field = field in doi_fields and args.doi
                if acceptable or doi_field:
                    output[(key, kind)].append(ii.strip())
                    if bracket_count(ii) > 0:
                        in_open_field = True
                else:
                    if key and False:
                        print("Skipping %s: %s" % (key, ii.strip()))
            else:
                if key and ii.strip() != "}" and ii.strip():
                    print("Non-bibtex %s: %s" % (key, ii.strip()))

    with open(args.new, 'w') as outfile:
        for key, kind in sorted(output, key=lambda x: x[0].lower()):
            spacing = "".join([" "] * (len(kind) + 2))
            outfile.write("\n\n@%s{%s,\n" % (kind, key))
            for jj in output[(key, kind)]:
                outfile.write("%s%s\n" % (spacing, jj.strip()))
            outfile.write("}")



