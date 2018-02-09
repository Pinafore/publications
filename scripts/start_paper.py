# Usage: python scripts/start_paper.py 20YY_VENUE_NAME
# Creates directory and skeleton for your paper

import sys
import os

kSECTIONS = ["abstract", "intro"]
kSUBDIR = ["data", "figures", "sections"]

kLATEX_TEMPLATE = """
\\documentclass{article}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Put these commands before you \\begin{document}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\newif\\ifcomment\\commenttrue
%\\newif\\ifcomment\\commentfalse
\\input{style/preamble}

\\newcommand{\\latexfile}[1]{\\input{~~NAME~~/sections/#1}}
\\newcommand{\\figfile}[1]{~~NAME~~/figures/#1}
\\newcommand{\\autofig}[1]{~~NAME~~/auto_fig/#1}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\\begin{document}

~~SECTIONS~~

This paper~\\cite{Nguyen:Boyd-Graber:Lund:Seppi:Ringger-2015} should be cited more.

\\bibliographystyle{plain}
\\bibliography{bib/journal-full,bib/jbg}

\\end{document}


"""

kR_TEMPLATE = """
# Script to create plots for your paper
import pandas as pd
import numpy as np

from plotnine import *

palette = {2: ["#000000", "#CFB87C"],
           3: ["#000000", "#FACD00", "#DA1D2B"],
           4: ["#FACD00", "#CFB87C", "#b2df8a", "#33a02c"]}

kROOT_DIR = "~~NAME~~"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)

"""

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


if __name__ == "__main__":
    paper_name = sys.argv[1]
    mkdir(paper_name)
    for ii in kSUBDIR:
        mkdir("%s/%s" % (paper_name, ii))

    o = open("%s.tex" % paper_name, 'w')
    sections = "\n".join("\\latexfile{%02i-%s}" % (ii * 10, jj) for ii, jj
                         in enumerate(kSECTIONS))
    o.write(kLATEX_TEMPLATE.replace("~~NAME~~", paper_name).replace("~~SECTIONS~~", sections))
    o.close()

    for ii, jj in enumerate(kSECTIONS):
        o = open("%s/sections/%02i-%s.tex" % (paper_name, ii*10, jj), 'w')
        o.write("%% %s" % jj)
        o.close()

    o = open("%s/figures.py" % paper_name, 'w')
    o.write(kR_TEMPLATE.replace("~~NAME~~", paper_name))
    o.close()
