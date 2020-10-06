from plotnine import *
import pandas as pd
import argparse
import numpy as np

kROOT_DIR = "2020_emnlp_alps"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)

# TODO: fix bug if not every task has data over the same set of methods and
# seeds
RANKINGS = {
    "mlmKM": "ALPS",
    "rand-badge":"BADGE",
    "rand-entropy":"Entropy",
    "rand":"Random",
    "embedKM":"BERT-KM",
    "embedKM-FTembedKM":"FT-BERT-KM",
    "maskedmlmKM": "masked-ALPS",
    "mlmKMs1.0":"ALPS-tokens-1.0",
    "mlmKMs0.1":"ALPS-tokens-0.1",
    "mlmKMs0.2":"ALPS-tokens-0.2",
    "mlmKP":"ALPS-KMPP",
    "OSmlmKM":"ALPS-OS"
}


DATA = {
    "sst-2": "SST-2",
    "agnews": "AG News",
    "pubmed": "PubMed",
    "imdb":"IMDB",
    "wos": "WOS",
    "hate": "Hate-Speech"
}

def seq_cls(df, rankings, order=None):
    print('Plotting seq cls results')

    df = df[df["ranking"].isin(rankings)]
    df_base = df[df.ranking=='base'].copy()
    df = df[df.ranking!='base']
    if order is not None:
        ORDER = order
        df['ranking'] = pd.Categorical(df['ranking'], categories=ORDER, ordered=True)
    g = ggplot(df, aes(x='size', y='score', color='ranking'))
    g += geom_smooth(size=0.7, span=0.70)
    g += geom_hline(df_base, aes(yintercept='score'), linetype='dashed')
    g += facet_wrap('~task', nrow=1, labeller=DATA)
    g += theme_bw()
    g += theme(legend_position='top')
    g += labs(color='Strategy', x='Number of Labeled Sequences', y='F1 Score' )
    g += scale_x_continuous(breaks=range(0,1200,200))
    g += scale_y_continuous(breaks=np.arange(0,1.2,0.2))
    return g

def add_zeros(df):
    runs = df.dropna().groupby(['task', 'seed','ranking']).first().copy()
    runs['score'] = 0
    runs['size'] = 0
    runs.reset_index(inplace=True)
    df = df.append(runs, ignore_index=True)
    return df


def add_warmstart(df):
    # for warmstart methods (e.g. entropy), add initial random sampling result
    coldstarts = {}
    warmstarts = []
    # iterate over methods
    for method in df['ranking'].unique():
        if method == 'base':
            continue
        elif '-' in method:
        # add warmstart methods to list
            warmstarts.append(method)
        else:
            # make copy of coldstart accuracy for first iteration
            df_method = df[(df['ranking'] == method)]
            #  entry of the smallest batch size for particular run
            df_min = df_method.loc[df_method.groupby(['task', 'seed'])['size'].idxmin()].copy()
            coldstarts[method] = df_min
    for method in warmstarts:
        cs, ws = method.split('-')
        df_cs = coldstarts[cs].assign(ranking = method)
        # TODO: avoid adding coldstart points to methods/task with no data
        df = df.append(df_cs, ignore_index = True)
    # remove coldstart DP points (will mess up loess curve)
    df = df[~df["ranking"].str.contains(r".*DP$", regex=True)]
    return df

def replace_ranking(df):
    df['ranking'].replace(to_replace=RANKINGS, inplace=True)


def preprocess(df):
    df = add_warmstart(df)
    df = add_zeros(df)
    replace_ranking(df)
    return df

def final_results():
    # final results
    df_test = pd.read_csv(datadir('results_test.csv'))
    df_test = preprocess(df_test)
    rankings = ["base","BADGE","ALPS","Random","Entropy","BERT-KM","FT-BERT-KM"]
    order = ['Random', 'Entropy', 'BERT-KM', 'FT-BERT-KM' ,'BADGE','ALPS']
    g = seq_cls(df_test, rankings, order)
    g.save(filename=gfxdir("seqcls.pdf"), width=12, height=4)


def km_vs_kpp():
    df_val = pd.read_csv(datadir('results_val.csv'))
    df_val = preprocess(df_val)
    tasks = ["imdb","pubmed"]
    df_val = df_val[df_val["task"].isin(tasks)]
    rankings = ["base", "ALPS", "ALPS-KMPP" ]
    g = seq_cls(df_val,  rankings)
    g.save(filename=gfxdir('km_kp_seqcls.pdf'))


def analysis():
    df = pd.read_csv(datadir('analysis.csv'))
    replace_ranking(df)
    ORDER = ['Random', 'Entropy', 'BERT-KM', 'FT-BERT-KM' ,'BADGE','ALPS']
    df['ranking'] = pd.Categorical(df['ranking'], categories=ORDER, ordered=True)
    g = ggplot(df, aes(x='diversity', y='uncertainty', shape='ranking', fill='iteration'))
    g += geom_jitter(size=5)
    g += theme_bw()
    g += theme(text=element_text(size=14),legend_position='top')
    g += labs(x="Diversity", y="Uncertainty", shape="Strategy")
    g += scale_fill_gradient(low="#F4ECF7", high="#6C3483")
    g += guides(fill=False)
    g += facet_wrap("~task", nrow=2, scales="free_y", labeller=DATA)
    g += theme(aspect_ratio=1.2/2)
    g.save(filename=gfxdir('analysis.pdf'))

if __name__ == "__main__":
    final_results()
    km_vs_kpp()
    analysis()

