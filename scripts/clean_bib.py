
from collections import defaultdict
import sys

kUNACCEPTABLE_OUTPUT = {"inbook": set(["url"]),
                        "inproceedings": set(["isbn", "series", "pages", "month", "address", "location", "editor", "tagline", "abstract", "publisher", "url", "doi", "organization"]),
                        "book": set(["isbn"]),
                        "misc": set([]),
                        "phdthesis": set(["url"]),
                        "mastersthesis": set(["url"]),
                        "techreport": set([]),
                        "article": set(["issn", "doi", "url", "abstract"])}

def bracket_count(s):
    return sum(1 for x in s if x=="{") - sum(1 for x in s if x=="}")
    
if __name__ == "__main__":
    output = defaultdict(list)
    key = ""
    in_open_field = False
    with open(sys.argv[1]) as infile:
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
                if ii.split("=")[0].strip().lower() not in kUNACCEPTABLE_OUTPUT[kind]:
                    output[(key, kind)].append(ii.strip())
                    if bracket_count(ii) > 0:
                        in_open_field = True
                else:
                    if key and False:
                        print("Skipping %s: %s" % (key, ii.strip()))
            else:
                if key and ii.strip() != "}" and ii.strip():
                    print("Non-bibtex %s: %s" % (key, ii.strip()))

    with open(sys.argv[2], 'w') as outfile:                    
        for key, kind in sorted(output, key=lambda x: x[0].lower()):
            spacing = "".join([" "] * (len(kind) + 2))
            outfile.write("\n\n@%s{%s,\n" % (kind, key))
            for jj in output[(key, kind)]:
                outfile.write("%s%s\n" % (spacing, jj.strip()))
            outfile.write("}")
                
            
                
