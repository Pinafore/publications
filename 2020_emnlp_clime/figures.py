
# Script to create plots for your paper
import pandas as pd
import numpy as np
import os

from plotnine import *
from plotnine import stats

palette = {2: ["#000000", "#CFB87C"],
           3: ["#000000", "#FACD00", "#DA1D2B"],
           4: ["#FACD00", "#CFB87C", "#b2df8a", "#33a02c"]}

kROOT_DIR = os.path.join(os.getcwd(), "2020_emnlp_clime")

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)


from matplotlib.font_manager import FontProperties
#font_prop = FontProperties(fname=kROOT_DIR + '/data/Roboto-Regular.ttf', size=16)
#text_style = {'fontproperties': font_prop}

#LABELS = {'acc':'Accuracy', 'n_queries':'Number of Keywords',
          #'lang':'Language','time_elapsed':'Time (min)'}

#def dataframe(drop=True):
    #df = pd.read_csv(datadir('results.csv'))
    #if drop:
        #df.dropna(inplace=True)
    #df.rename(columns=LABELS, inplace=True)
    #return df



def plot_queries_accuracy():
    n_keywords = list(range(51)) + list(range(51))
    acc_ug = [53.0,63.3,57.6,57.1,56.1,56.7,56.0,57.1,58.1,58.0,66.8,64.2,65.5,63.2,68.5,68.8,67.9,68.8,68.0,68.3,70.0,70.7,69.9,70.6,70.0,72.6,71.9,73.6,73.1,72.5,72.0,73.0,72.6,72.2,73.4,74.3,73.9,74.9,73.6,76.1,73.8,74.0,75.6,72.8,74.4,71.7,71.7,72.2,69.0,69.7,69.7]
    acc_ti = [55.9,60.5,61.7,58.5,55.0,55.1,54.9,57.0,57.4,56.7,69.2,70.1,72.8,69.4,77.0,77.1,76.5,76.3,76.7,77.6,77.8,76.6,76.4,76.4,76.4,76.5,75.8,75.8,75.6,75.1,75.5,75.5,75.9,75.6,75.6,76.1,76.0,75.8,76.1,76.1,75.8,75.7,75.7,75.9,75.4,75.6,75.1,74.5,73.2,72.3,72.6]
    acc = acc_ug + acc_ti
    language = ['Uyghur' for i in range(51)] + ['Tigrinya' for i in range(51)]
    df = pd.DataFrame({
        'n_keywords': n_keywords,
        'accuracy': acc,
        'Language':language
    })
    colors={'Tigrinya': 'blueviolet', 'Uyghur':'lightpink'}
    g = ggplot(df, aes(x='n_keywords', y='accuracy', color='Language'))
    # g += geom_point(size=3)
    g += stat_smooth(method='loess')
    g += scale_y_continuous(name='Accuracy (%)', limits=(50, 80))
    g += scale_x_continuous(name='Number of Keywords')
    g += theme_classic(base_size=14, base_family='Arial')
    g += scale_color_manual(values=colors)
    #g += labs(color='Language')
    g += theme(legend_position=(.8, .25))
    #g += theme(legend_position='none')
    g.save(filename=gfxdir('acc_nquery.pdf'), format='pdf')


def plot_single_test_accuracy(df):
    df['method'] = pd.Categorical(df['method'], categories=df['method'].unique(),
                                  ordered=True)
    g = ggplot(df, aes(x='method', y='accuracy', fill='method'))
    g += facet_wrap('~model', nrow=2)
    g += geom_bar(stat='identity', width=.7)
    g += geom_text(aes(label='accuracy'), stat='identity', nudge_y=0.125,
                   va='bottom', format_string='{:.1f}%', size=6)
    g += coord_cartesian(ylim=(0, 90))
    g += theme_classic(base_size=10, base_family='Arial')
    g += theme(legend_position=(0.80,0.30))
    # g += theme(panel_spacing_x=0.25, panel_spacing_y=0.25)
    g += theme(axis_text_x=element_blank(), axis_ticks_major_x=element_blank(),
               axis_title_x=element_blank())
    g += theme(strip_text_x = element_text(margin={'t':5,'b':5}))
    # g += theme(strip_margin=0.2)
    # g += theme(axis_line_x=element_line(color='black'))
    g += labs(fill='Method', y="Accuracy")
    g += theme(aspect_ratio=4/5)
    # g += scale_fill_manual(['#CBE6F5', '#C5D9CA', '#F2DA63', '#F2B705'])
    g += scale_fill_manual(['#A2666F', '#F6A4A2', '#F45866', '#D5ECD8'])
    return g


def plot_test_accuracy():
    fig_height = 2.4
    fig_width = 4.8
    df1 = pd.DataFrame({
        'method': ['Base', 'Active', 'CLIME', 'A+C'],
        'accuracy': [55.2, 60.2, 62.0, 63.4],
        'model': ['Sinhalese, CCA\n25 users, 45 min. (avg)' for i in range(4)]
    })
    # plot_single_test_accuracy(df).save(filename=gfxdir('si_cca.pdf'), height=fig_height, width=fig_width, format='pdf')
    df2 = pd.DataFrame({
        'method': ['Base', 'Active', 'CLIME', 'A+C'],
        'accuracy': [53.0, 69.7, 69.9, 73.2],
        'model': ['Uyghur, CCA\n1 user, 27 min. (avg)' for i in range(4)]
    })
    # plot_single_test_accuracy(df).save(filename=gfxdir('ug_cca.pdf'), height=fig_height, width=fig_width, format='pdf')
    df3 = pd.DataFrame({
        'method': ['Base', 'Active', 'CLIME', 'A+C'],
        'accuracy': [55.9, 57.5, 73.0, 77.1],
        'model': ['Tigrinya, CCA\n1 user, 34 min. (avg)' for i in range(4)]
    })
    # plot_single_test_accuracy(df).save(filename=gfxdir('ti_cca.pdf'), height=fig_height, width=fig_width, format='pdf')
    df4 = pd.DataFrame({
        'method': ['Base', 'Active', 'CLIME', 'A+C'],
        'accuracy': [54.3, 56.3, 62.6, 73.2],
        'model': ['Ilocano, RCSLS\n10 users, 40 min. (avg)' for i in range(4)]
    })
    # plot_single_test_accuracy(df).save(filename=gfxdir('il_rcsls.pdf'), height=fig_height, width=fig_width, format='pdf')
    df5 = pd.DataFrame({
        'method': ['Base', 'Active', 'CLIME', 'A+C'],
        'accuracy': [53.6, 60.9, 56.0, 63.7],
        'model': ['Sinhalese, RCSLS\n25 users, 40 min. (avg) ' for i in range(4)]
    })
    # plot_single_test_accuracy(df).save(filename=gfxdir('si_rcsls.pdf'), height=fig_height, width=fig_width, format='pdf')
    df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
    plot_single_test_accuracy(df).save(filename=gfxdir('acc.pdf'))

def plot_multi_accuracy():
    df = pd.DataFrame({
        'method': range(4),
        'accuracy': [55.2, 60.1, 60.2, 60.7],
        'se': [0, 2.1, 5.0, 4.3]
    })
    # g = ggplot(df, aes(x='session', y='acc'))
    # g += geom_line()
    # g += geom_point(size=3)
    # g += geom_errorbar(aes(ymin='acc - se', ymax='acc + se'), width=0.2)
    # g += geom_text(aes(label='acc'),nudge_y=1)
    # g += stat_smooth(method='lm')
    # g += scale_y_continuous(name='Accuracy (%)', limits=(50, 70))
    # g += scale_x_continuous(name='Number of Sessions')
    # g += theme_classic(base_size=14, base_family='Arial')
    # g += scale_fill_manual(values=colors)
    # g += theme(legend_position='none')
    # g.save(filename=gfxdir('multi.pdf'))

    df['method'] = pd.Categorical(df['method'], categories=df['method'],
                                  ordered=True)
    g = ggplot(df, aes(x='method', y='accuracy', fill='method'))
    g += geom_bar(stat='identity', width=.7)
    g += geom_text(aes(label='accuracy'), stat='identity', nudge_y=0.125,
                   va='bottom', format_string='{:.1f}%', size=14)
    g += coord_cartesian(ylim=(0, 75))
    g += theme_classic(base_size=14, base_family='Arial')
    g += theme(legend_position='none')
    g += theme(axis_text_x=element_text(vjust=1))

    g += theme(axis_title_x=element_text())
    g += labs(x='\nNumber of Sessions', y='Accuracy')
    g += scale_fill_manual(['#D6EAF8', '#85C1E9', '#3498DB', '#2874A6'])
    g.save(filename=gfxdir('multi.pdf'))

def plot_time():
    models= {
        'med_il':'Ilocano',
        'med_si':'Sinhalese\n(RCSLS)',
        'med_si_cca':'Sinhalese\n(CCA)',
        'med_ti': 'Tigrinya',
        'med_ug': 'Uyghur'
    }
    df = pd.read_csv(datadir('time.csv'))
    df['model'].replace(to_replace=models, inplace=True)
    g = ggplot(df, aes(x='model', y='time'))
    g += geom_point()
    # g += geom_hline(stat='summary', fun_y=np.mean)
    # g += stat_summary(fun_y=np.mean, inherit_aes=True)
    # g += geom_pointrange(ymin=np.amin, ymax=np.amax)
    g += geom_boxplot()
    g += coord_cartesian(ylim=(0, 70))
    g += theme_classic()
    g += theme(axis_title_x=element_blank())
    g += labs(y='Time (min.)')
    g += scale_x_discrete(values=models)
    g.save(filename=gfxdir('time.pdf'))

if __name__ == '__main__':
    plot_test_accuracy()
    plot_queries_accuracy()
    plot_multi_accuracy()
    # plot_time()

