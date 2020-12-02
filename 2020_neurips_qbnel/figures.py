
# Script to create plots for your paper
import pandas as pd
import numpy as np

from plotnine import *

palette = {2: ["#000000", "#CFB87C"],
           3: ["#000000", "#FACD00", "#DA1D2B"],
           4: ["#FACD00", "#CFB87C", "#b2df8a", "#33a02c"]}

kROOT_DIR = "2020_emnlp_qbnel"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)

