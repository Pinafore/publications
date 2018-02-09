
import pandas as pd
import numpy as np

from plotnine import *

kROOT_DIR = "2015_naacl_qb_coref"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)

palette = ["#000000", "#CFB87C"]

active_data = pd.read_csv(datadir("active.csv"))
density_data = pd.read_csv(datadir("density.csv"))
compare_data = pd.read_csv(datadir("compare.csv"))

active = (ggplot(active_data, aes(color='Method', y='Precision', x='Iteration')) + geom_point() + stat_smooth(method='lm') + theme(legend_position="top") + scale_fill_manual(values=palette) + scale_colour_manual(values=palette))

density = (ggplot(density_data, aes(color='Data', size='Data', x='Tokens', y='Count', linetype='Coref')) + geom_line() + scale_size_discrete(range = (0.75, 1.5)) + scale_colour_manual(values=palette))

compare = (ggplot(compare_data, aes(x='Formula', y='Score', linetype='Coreference', fill='Coreference')) + facet_grid("Metric ~ Mentions") + geom_bar(stat="identity", position="dodge") + xlab("") + theme(legend_position="top") + scale_fill_manual(values=palette))

active.save(gfxdir("active.pdf"), scale=0.6, height=6, width=8)
density.save(gfxdir("density.pdf"), scale=0.6, height=6, width=8)
compare.save(gfxdir("compare.pdf"), scale=0.6, height=6, width=16)
