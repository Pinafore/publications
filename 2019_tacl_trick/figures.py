import os
import pickle
import difflib
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib
import json
matplotlib.use('agg')
from plotnine import (
    ggplot, aes, ggtitle,
    geom_bar, geom_density, geom_boxplot, geom_segment, geom_col, geom_hline, geom_point, geom_errorbarh,
    theme, theme_light, coord_flip, facet_grid, xlim, ylim,
    element_text, element_blank, element_rect, element_line,
    scale_fill_manual, scale_fill_brewer, xlab, ylab, geom_line, facet_wrap,
    scale_x_continuous, scale_y_continuous, scale_color_manual
)

data_dir = '2019_tacl_trick/data/rnn_question_buzz_pos.pickle'
fig_dir = '2019_tacl_trick/auto_fig/'


class theme_fs(theme_light):
    """
    A theme similar to :class:`theme_linedraw` but with light grey
    lines and axes to direct more attention towards the data.

    Parameters
    ----------
    base_size : int, optional
        Base font size. All text sizes are a scaled versions of
        the base font size. Default is 11.
    base_family : str, optional
        Base font family.
    """

    def __init__(self, base_size=11, base_family='DejaVu Sans'):
        theme_light.__init__(self, base_size, base_family)
        self.add_theme(theme(
            axis_ticks=element_line(color='#DDDDDD', size=0.5),
            panel_border=element_rect(fill='None', color='#838383',
                                      size=1),
            strip_background=element_rect(
                fill='#DDDDDD', color='#838383', size=1),
            strip_text_x=element_text(color='black'),
            strip_text_y=element_text(color='black', angle=-90),
            legend_key=element_blank(),
        ), inplace=True)


def gen_fig():
    X_title = 'Edit Iteration'
    Y_title = 'Position in Question'
    C_title = 'Type'

    stuff = pickle.load(open(data_dir, 'rb'))
    all_questions, all_buzzes = stuff[0], stuff[1]

    for k, (questions, buzzes) in enumerate(zip(all_questions, all_buzzes)):
        if len(buzzes) < 5:
            continue
        if all(x == 'NULL' for x in buzzes):
            continue
        print(k)
        length_buzzing_positions = {X_title: [], Y_title: [], C_title: []}
        for i, (q, b) in enumerate(zip(questions, buzzes)):
            length = len(q.split())
            length_buzzing_positions[X_title].append(i)
            length_buzzing_positions[Y_title].append(length)
            length_buzzing_positions[C_title].append('Question Length')
            if b == 'NULL':
                b = length
            length_buzzing_positions[X_title].append(i)
            length_buzzing_positions[Y_title].append(b)
            length_buzzing_positions[C_title].append('Buzzing Position')

        df = pd.DataFrame(length_buzzing_positions)
        p = (
            ggplot(df)
            + geom_path(aes(x=X_title, y=Y_title, color=C_title), size=2)
            + theme(
                legend_title=element_blank(),
                legend_position='top',
            )
        )
        p.save(os.path.join(fig_dir, '{}.pdf'.format(k)))


def load_ikuya_nips():
    with open('2019_tacl_trick/data/shared_task_results.json') as f:
        results = []
        all_results = json.load(f)
        for q in all_results:
            question = q['question']
            n_words = len(question.split())
            # ID for Ikuya system is 8
            _, position, correct = q['guesses']['8']
            position = int(position)
            correct = float(correct.strip() == 'True')
            results.append({'position': position, 'percent': position / n_words, 'correct': correct})
    results = sorted(results, key=lambda r: r['percent'])
    total = len(results)
    n_correct = 0
    x = []
    y = []
    for r in results:
        n_correct += r['correct']
        x.append(r['percent'])
        y.append(n_correct / total)
    df = pd.DataFrame({'x': x, 'y': y})
    df['model'] = 'Regular Test'
    return df


def relabel(l):
    if l == 'IR Adversarial':
        return 'IR Adversarial'
    elif l == 'RNN Adversarial':
        return 'RNN Adversarial'
    else:
        return l


def rerelabel(l):
    if l == 'Regular Test':
        return 'Test'
    elif l == 'IR Adversarial':
        return 'IR'
    elif l == 'RNN Adversarial':
        return 'RNN'
    else:
        return l


def ikuya_sys_plot():
    nips_df = load_ikuya_nips()
    with open('2019_tacl_trick/data/ikuya_cdf.json') as f:
        df = pd.DataFrame(json.load(f))
        df = pd.concat([df, nips_df])
        df['model'] = df['model'].map(relabel)
        model_dtype = CategoricalDtype(['Regular Test', 'IR Adversarial', 'RNN Adversarial'], ordered=True)
        df['model'] = df['model'].astype(model_dtype)
        p = (
            ggplot(df) + aes(x='x', y='y', color='model', xmin='x', xmax='x')
            + geom_point(size=1.0, shape='.')
            + xlab('Percent of Question Revealed')
            + ylab('Accuracy')
            + scale_y_continuous(breaks=np.linspace(0, 1, 6), limits=[0, 1])
            + theme(
                legend_position=(.335, .7),
                legend_background=element_blank(),#element_rect(alpha=1, fill='#EEEFEE', color='white'),                                
                #legend_key=element_rect(alpha=0),
                legend_box_margin=0, legend_title=element_blank()
            )
        )
    p.save('2019_tacl_trick/auto_fig/ikuya_cdf.pdf', width=3.5, height=2.5)


def round_1_plot():
    df = pd.read_csv('2019_tacl_trick/data/round_1.csv')
    model_dtype = CategoricalDtype(['DAN', 'RNN', 'IR'], ordered=True)
    df['Model'] = df['Model'].astype(model_dtype)

    # This following is a hack so that the legend widths are the same across plots
    def rename(x):
        if x == 'Round 1 - IR Adversarial':
            return 'Round 1 - IR Adversarial    '
        else:
            return x
    df['Dataset'] = df['Dataset'].map(rename)
    p = (
        ggplot(df)
        + aes(x='x', y='y', color='Dataset') + facet_wrap('Model', nrow=1)
        + geom_point(size=1.0, shape='o')
        + scale_y_continuous(breaks=np.linspace(0, 1, 6), limits=[0, 0.6])
        + scale_x_continuous(breaks=[0, .5, 1])
        + xlab('Percent of Question Revealed')
        + ylab('Accuracy')
        + ggtitle('Round 1 Attacks and Models')
        + theme(
            strip_text_x=element_text(margin={'t': 6, 'b': 6, 'l': 1, 'r': 5})
        )
        + scale_color_manual(values=['#FF3333', '#66CC00', '#3333FF', '#FFFF33'], name='Questions')
    )
    p.save('2019_tacl_trick/auto_fig/round_1_csv.pdf', width=7.0, height=1.7)


if __name__ == '__main__':
    ikuya_sys_plot()
    round_1_plot()
