
# Script to create plots for your paper
import pandas as pd
import numpy as np
import pathlib
from scipy.stats import ttest_ind
from collections import defaultdict

from plotnine import *

palette = {2: ["#000000", "#CFB87C"],
           3: ["#000000", "#FACD00", "#DA1D2B"],
           4: ["#FACD00", "#CFB87C", "#b2df8a", "#33a02c"]}

def datadir(filename):
    return "../data/%s" % (filename)

def gfxdir(filename):
    return "auto_fig/%s" % (filename)

OUTPUTS = {
        'preco_f1':gfxdir('preco_f1.pdf'),
        'preco_mention':gfxdir('preco_mention.pdf'),
        'penalty': gfxdir('penalty.pdf'),
        'qbcoref_f1':gfxdir('qbcoref_f1.pdf'),
        'qbcoref_mention':gfxdir('qbcoref_mention.pdf'),
        'preco_simple_f1':gfxdir('preco_simple_f1.pdf'),
        'preco_samples':gfxdir('preco_samples.pdf'),
        'preco_error':gfxdir('preco_error.pdf'),
        'qbcoref_error':gfxdir('qbcoref_error.pdf')
        }

def base_plot(df, metric):
    g = ggplot(df, aes(x='total_spans', y=metric, color='strategy', linetype='linetype'))
    g += geom_point(size=0.2, alpha=0.3)
    g += theme_bw()
    g += theme(
            axis_title=element_text(size=20),
            axis_text = element_text(size=15),
            strip_text = element_text(size=20),
            legend_position = 'top', legend_title=element_text(size=20),
            legend_text=element_text(size=15), legend_key_size=20,
            )
    label = 'Avg. F1 Score' if metric == 'f1' else 'Mention Detection Accuracy'
    g += labs(color='Strategy', x='# of Spans', y=label)
    g += guides(fill=False, color=guide_legend(reverse=False), linetype=False)
    g += scale_color_hue(h=0.25, l=0.5, s=0.7)
    g += geom_smooth(size=1.0, span=0.8)
    max_docs = df.max_docs.max()
    g += facet_grid('max_docs ~ num_spans',
        labeller=labeller(
            cols = lambda x: f'{x} spans',
            rows = lambda x: f'{x} docs' if int(x) < max_docs else 'unconstrained'
            )
    )
    return g

def add_initial_point(df):
    f1_start = df[df.num_spans == 0]['f1'].values[0]
    mentions_start = df[df.num_spans == 0]['mentions'].values[0]
    df = df[df.num_spans != 0]
    runs = df.groupby(['strategy', 'num_spans', 'max_docs', 'seed'], as_index=False).first()
    runs.cycle = 0
    runs.f1 = f1_start
    runs.mentions = mentions_start
    df = df.append(runs, ignore_index=True)
    return df

def preprocess(df, initial=True):
    df.strategy = df.strategy.replace({'noise': 'random', 'random':'random-ment', 'li-ent': 'li-clust-ent'})
    STRATEGIES = [ 'clust-ent','cond-ent', 'joint-ent', 'ment-ent', 'random','random-ment']
    df = df[df.strategy.isin(STRATEGIES)]
    df.strategy = pd.Categorical(df.strategy, categories = STRATEGIES, ordered=True)
    # change max_docs to overall maximum docs to represent unconstrained sampling
    max_docs = df.max_docs.max()
    df.loc[df.max_docs == df.num_spans, 'max_docs'] = max_docs
    # creating starting point for each setting
    if initial:
        df = add_initial_point(df)
    # add column total spans
    df['total_spans'] = df.apply(lambda row: row['num_spans'] * row['cycle'], axis=1)
    df['linetype'] = df.apply(lambda row: 'random' in row['strategy'], axis=1)
    # df['zorder'] = df.apply(lambda row: STRATEGIES.index(row['strategy'])+10, axis=1)
    return df

def value(group, attribute):
    values = group[attribute].unique()
    if len(values) != 1:
        return None
    return values[0]

def get_max_cycles(group, df):
    num_spans = value(group, 'num_spans')
    max_docs = value(group, 'max_docs')
    max_cycles = df.loc[(df.num_spans == num_spans) & (df.max_docs == max_docs), 'cycle'].max()
    return max_cycles

def pairwise_penalty(df, threshold = 2.776):
    penalty = defaultdict(int)
    # divide into runs (excluding seed divisions) to find whether alg i beats alg j
    runs = df.groupby(['data','num_spans', 'max_docs', 'cycle'], as_index=False)
    for name, group in runs:
        strategies = group.groupby(['strategy'], as_index=False)
        max_cycles = get_max_cycles(group, df)
        for _, s1 in strategies:
            for _, s2 in strategies:
                t = ttest_ind(s1['f1'], s2['f1']).statistic
                if t > threshold:
                    pair = (value(s1, 'strategy'), value(s2, 'strategy'))
                    penalty[pair] = penalty[pair] + 1 / max_cycles
                elif t < -threshold:
                    pair = (value(s2, 'strategy'), value(s1, 'strategy'))
                    penalty[pair] = penalty[pair] + 1 / max_cycles
                else:
                    pair1 = (value(s1, 'strategy'), value(s2, 'strategy'))
                    penalty[pair1] = penalty[pair1]
                    pair2 = (value(s2, 'strategy'), value(s1, 'strategy'))
                    penalty[pair2] = penalty[pair2]
    lst_penalty = [
            {'i': pair[0], 'j': pair[1], 'penalty': penalty[pair]} for pair in penalty
            ]
    df_penalty = pd.DataFrame(lst_penalty)
    # get column-wise averages
    df_overall = df_penalty.groupby('j', as_index=False).mean()
    df_overall['i'] = ''
    df_overall['height'] = 0.8
    df_penalty['height'] = 1
    df_penalty = df_penalty.append(df_overall, ignore_index=True)

    return df_penalty

def penalty_map(df):
    # midpoint = df.penalty.max() / 2
    midpoint = df.penalty.mean()
    g = ggplot(df, aes(x='j', y='i', fill='penalty'))
    g += geom_tile(aes(height='height', width=1))
    g += geom_text(aes(label='penalty'), color='black', format_string='{:.2f}', size=20)
    g += theme_minimal()
    g += theme(
            axis_title_x=element_blank(), axis_title_y=element_blank(),
            axis_text = element_text(size=20, angle=15),
            legend_position = 'top', legend_title=element_text(size=20),
            legend_text=element_text(size=20), legend_key_size=20,
            )
    g += scale_fill_gradient2(low='#f6f5f5', mid='#d3e0ea', high='#1687a7', midpoint=midpoint)
    g.save(filename=OUTPUTS['penalty'])


def plot_simple_f1():
    df = pd.read_csv(datadir('results_preco.csv'))
    df = preprocess(df)
    df = df[(df.total_spans <= 300)]
    df = df[(df.num_spans==50) & (df.max_docs==1)]
    g = ggplot(df, aes(x='total_spans', y='f1', color='strategy', linetype='linetype'))
    g += geom_point(size=1.0, alpha=0.5)
    g += geom_smooth(size=2.0, span=0.8)
    g += theme_bw()
    g += theme(legend_position='top')
    g += labs(color='Strategy', x='No. of Spans', y='Avg. F1 Score')
    g += ylim(0.4,0.75)
    g += guides(fill=False, linetype=False)
    g += scale_color_hue(h=0.25, l=0.5, s=0.7)
    g += theme(
            axis_title=element_text(size=25),
            axis_text = element_text(size=20),
            legend_position = 'top', legend_title=element_text(size=20),
            legend_text=element_text(size=15), legend_key_size=20,
            )
    g.save(filename=OUTPUTS['preco_simple_f1'])

def plot_simple_f1_sequence(i):
    df = pd.read_csv(datadir('results_preco.csv'))
    df = preprocess(df)
    df = df[(df.total_spans <= 300)]
    df = df[(df.num_spans==50) & (df.max_docs==1)]
    STRATEGIES = [ 'ment-ent','clust-ent', 'cond-ent', 'joint-ent', 'random','random-ment']
    df = df[df.strategy.isin(STRATEGIES[:i])]
    g = ggplot(df, aes(x='total_spans', y='f1', color='strategy', linetype='linetype'))
    g += geom_point(size=1.0, alpha=0.5)
    g += geom_smooth(size=3.0, span=0.8, alpha=0.1)
    g += theme_bw()
    g += theme(legend_position='top')
    g += ylim(0.4,0.75)
    g += labs(color='Strategy', x='No. of Spans', y='Avg. F1 Score')
    g += guides(fill=False, linetype=False)
    colors = ['orchid', 'salmon', 'skyblue', 'lightgreen', 'lightslategrey', 'navy']
    g += scale_color_manual(values = colors)
    g += theme(
            axis_title=element_text(size=25),
            axis_text = element_text(size=20),
            legend_position = 'top', legend_title=element_text(size=20),
            legend_text=element_text(size=15), legend_key_size=20,
            )
    g.save(filename = gfxdir(f'preco_simple_f1_{i}.pdf'))

def process_counts(df):
    all_counts = []
    for i, row in df.iterrows():
        for span_type in ['entities', 'non-entities', 'pronouns', 'singletons']:
            counts = {'strategy': row['strategy'], 'cycle': str(row['cycle'])}
            counts['span_type'] = span_type
            counts['count'] = row[span_type]
            if counts['span_type'] == 'entities':
                counts['span_type'] = 'entity mentions'

            elif counts['span_type'] == 'non-entities':
                counts['span_type'] = 'non-entities'
            all_counts.append(counts)
    return all_counts


def plot_samples_bar():
    df = pd.read_csv(datadir('results_preco.csv'))
    df = preprocess(df)
    df = df[(df.total_spans <= 200)]
    df = df[(df.num_spans==50) & (df.max_docs==1) & (df.cycle != 0) & (df.seed == 67)]
    df = df[df.strategy!='li-clust-ent'] # for slides
    counts = process_counts(df)
    df_counts = pd.DataFrame(counts)
    g = ggplot(df_counts, aes(x='cycle', y='count', fill='span_type',))
    g += theme_bw()
    g += geom_col(stat='identity', position='dodge')
    g += labs(fill='Span Type', x='Cycle')
    g += facet_wrap('strategy', nrow=2) # for slides
    g += theme(
            axis_title_x=element_text(size=30),
            axis_text = element_text(size=25),
            axis_title_y = element_blank(),
            strip_text = element_text(size=25),
            legend_position = 'top', legend_title=element_text(size=25),
            legend_text=element_text(size=20), legend_key_size=10,
            )
    g.save(filename=OUTPUTS['preco_samples'], width=9, height=7) # for slides


def plot_preco():
    def make_plot(metric, df):
        g = base_plot(df,metric)
        if metric == 'f1':
            g += ylim(0.4,0.75)
        else:
            g += ylim(0.35,0.85)
        return g
    # full_f1 = 0.860
    data_fp = datadir('results_preco.csv')
    df = pd.read_csv(data_fp)
    df = preprocess(df, initial=True)
    df = df[(df.total_spans <= 300)]
    df = df[df.num_spans > 10]

    g_f1 = make_plot('f1', df)
    g_f1.save(filename=OUTPUTS['preco_f1'], width=6, height=9) # for slides
    return df

def plot_preco_sequence(i):
    data_fp = datadir('results_preco.csv')
    df = pd.read_csv(data_fp)
    df = preprocess(df, initial=True)
    df = df[(df.total_spans <= 300)]
    df = df[df.num_spans > 20]
    df = df[df.max_docs != 5]
    STRATEGIES = [ 'ment-ent','clust-ent', 'cond-ent', 'joint-ent', 'random','random-ment']
    df = df[df.strategy.isin(STRATEGIES[:i])]
    g = ggplot(df, aes(x='total_spans', y='f1', color='strategy', linetype='linetype'))
    g += geom_point(size=0.2, alpha=0.3)
    g += theme_bw()
    g += theme(
            axis_title=element_text(size=20),
            axis_text = element_text(size=15),
            strip_text = element_text(size=20),
            legend_position = 'right', legend_title=element_text(size=20),
            legend_text=element_text(size=15), legend_key_size=20,
            )
    label = 'Avg. F1 Score'
    g += labs(color='Strategy', x='# of Spans', y=label)
    g += guides(fill=False, color=guide_legend(reverse=False), linetype=False)
    colors = ['orchid', 'salmon', 'skyblue', 'lightgreen', 'lightslategrey', 'navy']
    g += scale_color_manual(values = colors)
    g += geom_smooth(size=3.0, span=0.8, alpha=0.1)
    max_docs = df.max_docs.max()
    g += facet_wrap('max_docs',
            labeller=lambda x: f'{x} docs' if int(x) < max_docs else 'unconstrained',
            nrow=1
            )
    g += ylim(0.4,0.75)
    g.save(filename=gfxdir(f'preco_f1_{i}.pdf'), width=12, height=4)




def plot_qbcoref():
    def make_plot(metric):
        g = base_plot(df, metric)
        if metric == 'f1':
            g += ylim(0.3,0.65)
        else:
            g += ylim(0.35,0.85)
        g += guides(color=False)
        # g += labs(y='')
        return g
    # full_f1 = 0.795
    data_fp = datadir('results_qbcoref.csv')
    df = pd.read_csv(data_fp)
    df = preprocess(df)
    # df = df[df.max_docs == 1]
    df = df[df.num_spans <= 40]

    g_f1 = make_plot('f1')
    g_f1.save(filename=OUTPUTS['qbcoref_f1'], width=6, height=9)
    g_mention = make_plot('mentions')
    g_mention.save(filename=OUTPUTS['qbcoref_mention'], width=6, height=9)
    return df

def plot_userstudy(i):
    def preprocess_data(fp, day, session):
        df = pd.read_json(fp, lines=True)
        df['session'] = session
        df['day'] = day
        # mark start of new document
        df['switch'] = df.apply(lambda row: row.query_index == 0, axis=1)
        # seconds to minutes
        df['total_time'] = df.apply(lambda row: row.total_time / 60, axis=1)
        df = df.round({'total_time':2})
        # read
        df['read'] = df.apply(lambda row: 'FewDocs' if session == 1 else 'ManyDocs', axis=1)
        return df

    def plot_sessions(full, i):
        suffix = '_full' if full else '_reduced'
        # line_size = 3 if full else 1.5
        dot_size = 0.5 if full else 1
        df1_1 = preprocess_data(datadir(f'session1{suffix}.jsonl'), 1, 1)
        df1_2 = preprocess_data(datadir(f'session2{suffix}.jsonl'), 1, 2)
        df = pd.concat([df1_1, df1_2], ignore_index=True)
        users = ['user1', 'user2', 'user3']
        df = df[df.user.isin(users[:i])]

        df_switches = df[df.switch]
        g = ggplot(df, aes(x='total_time', y='total_spans', color='user'))
        g += geom_line(aes(linetype='factor(read)'), size=2)
        g += geom_point(df_switches, size=dot_size, color='black')
        g += theme_bw()
        g += scale_color_manual(values=['dodgerblue', 'plum', 'palegreen'])
        g += labs(y='No. of Labeled Spans', x='Total Labeling Time (min.)', linetype='Session')
        g += guides(color=False)
        g += theme(legend_position='top')
        g += theme(
                axis_title = element_text(size=15),
                axis_text = element_text(size=15),
                legend_position = 'top', legend_title=element_text(size=15),
                legend_text=element_text(size=15), legend_key_size=30
                )

        g.save(filename=gfxdir(f'userstudy{suffix}_{i}.pdf'))

    plot_sessions(False, i)


def plot_errors():
    def plot_errors_df(df):
        df_dicts = df.to_dict("records")
        new_df_dicts = []
        for entry in df_dicts:
            model = entry.pop('model')
            for x in entry:
                new_entry = {'model':model, 'error_type':x ,'num_errors':entry[x]}
                new_df_dicts.append(new_entry)
        df = pd.DataFrame(new_df_dicts)
        df.num_errors = df.num_errors.div(1000)
        df.error_type.replace({
            'conflated_entity':'conflated entity',
            'divided_entity':'divided entity',
            'extra_entity':'extra entity',
            'extra_mention':'extra mention',
            'missing_mention':'missing mention',
            'missing_entity':'missing entity',
            }, inplace=True
        )
        g = ggplot(df, aes(x='model', y='num_errors', fill='model',))
        g += theme_bw()
        # g += geom_col(stat='identity', position='dodge')
        g += geom_col(stat='identity')
        g += labs(y='No. of Errors (K)')
        g += coord_flip()
        g += guides(fill=False)
        g += facet_wrap('error_type', scales = 'free_x', nrow=3)
        g += theme(
                axis_text_x=element_text(rotation=0, size=20),
                axis_text_y=element_text(size=20),
                axis_title_y=element_blank(),
                axis_title_x=element_text(size=30),
                strip_text = element_text(size=25),
                subplots_adjust={'hspace': 0.4}
                )
        return g
    df_preco = pd.read_csv(datadir('error_preco.csv'))
    g_preco = plot_errors_df(df_preco)
    g_preco.save(filename=OUTPUTS['preco_error'], width=8, height=12)






if __name__ == "__main__":
    for i in range(1,7):
        plot_simple_f1_sequence(i)
        plot_preco_sequence(i)
    for i in range(1,4):
        plot_userstudy(i)

