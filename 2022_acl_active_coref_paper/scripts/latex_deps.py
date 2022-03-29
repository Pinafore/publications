
import sys
from glob import glob

dependencies = set()

if __name__ == "__main__":
    for ii in sys.argv[1:]:
        for jj in open(ii):
            if "{" in jj and "}" in jj:
                for kk in jj.split("{")[1].split("}")[0].split(","):
                    if kk.startswith("style/") or kk.startswith("bib/"):
                        for ll in glob("%s*" % kk):
                            dependencies.add(ll)

    print(" ".join(dependencies))
