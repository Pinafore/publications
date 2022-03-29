import pandas as pd
import numpy as np
import pathlib
import figures

def datadir(filename):
    return "data/%s" % (filename)

def display_table(dataset):
    df = pd.read_csv(datadir(f'results_{dataset}.csv'))
    df = figures.preprocess(df)
    if dataset == 'preco':
        m = 50
    elif dataset == 'qbcoref':
        m = 40
    df = df[df.num_spans == 20]
    df = df[['strategy', 'max_docs', 'total_spans', 'f1', 'mentions']]
    df = df[df.total_spans.isin([100, 200, 300 ])]
    df = df[df.max_docs.isin([1,m])]
    df['max_docs'] = df['max_docs'].map({m: 'unconstrained', 1: '1'})
    groups = df.groupby(['total_spans', 'max_docs', 'strategy'])

    def mean_std(x):
        mean = np.mean(x)
        std = np.std(x, ddof=1)
        return f'{mean:.2f} $\pm$ {std:.2f}'
    output = groups[['f1', 'mentions']].agg(lambda x: mean_std(x))
    output.index.set_names({
                'total_spans':'Total No. of Labeled Spans', 'max_docs':'$m$',
                'strategy':'Strategy',
                }, inplace=True)

    output.rename(columns={
                'f1': 'Avg. F1', 'mentions': 'Mention Accuracy'
                }, inplace=True)
    output.to_latex(f'sections/results_{dataset}.tex', escape=False)


# display_table('preco')
display_table('qbcoref')
