import os
import pandas as pd
import plotnine as p9

ROOT = '2020_acl_refine_clwe'
FONT_SIZE = 20


def data_file(filename):
    return os.path.join(ROOT, 'data', filename)


def output_file(filename):
    return os.path.join(ROOT, 'auto_fig', filename)


def plot_bli(clwe, train_table, test_table, output, ylim):
    df_train = pd.read_csv(data_file(train_table))
    for i in range(df_train.shape[0]):
        df_train.at[i, 'refine'] += ' (train)'
    df_test = pd.read_csv(data_file(test_table))
    for i in range(df_test.shape[0]):
        df_test.at[i, 'refine'] += ' (test)'
    df = pd.concat((df_train, df_test))
    df = df[df.clwe == clwe]
    df = df.assign(
        refine=pd.Categorical(df['refine'], ['Original (train)', 'Original (test)', '+retrofit (train)', '+retrofit (test)', '+synthetic (train)', '+synthetic (test)']),
        language=pd.Categorical(df['language'], ['DE', 'ES', 'FR', 'IT', 'JA', 'RU', 'ZH', 'AVG'])
    )
    g = p9.ggplot(df, p9.aes(x='language', y='accuracy', fill='refine'))
    g += p9.geom_bar(position='dodge', stat='identity', width=.8)
    g += p9.coord_cartesian(ylim=ylim)
    g += p9.scale_fill_manual(['#999999', '#CCCCCC', '#EA5F94', '#E9A4BA', '#FFB14E', '#FFD700'])
    g += p9.theme_void(base_size=FONT_SIZE, base_family='Arial')
    g += p9.theme(
        plot_background=p9.element_rect(fill='white'),
        panel_grid_major_y=p9.element_line(),
        axis_text_x=p9.element_text(margin={'t': 10}),
        axis_text_y=p9.element_text(margin={'r': 8}),
        legend_position=(.7, 1),
        legend_direction='horizontal',
        legend_title=p9.element_blank(),
        legend_text=p9.element_text(size=FONT_SIZE),
        legend_box_margin=0,
        figure_size=(24, 3)
    )
    g.save(filename=output_file(output))


def plot_downstream(clwe, table, output, ylim):
    df = pd.read_csv(data_file(table))
    df = df[df.clwe == clwe]
    df = df.assign(
        refine=pd.Categorical(df['refine'], ['Original', '+retrofit', '+synthetic']),
        language=pd.Categorical(df['language'], ['DE', 'ES', 'FR', 'IT', 'JA', 'RU', 'ZH', 'AVG'])
    )
    g = p9.ggplot(df, p9.aes(x='language', y='accuracy', fill='refine'))
    g += p9.geom_bar(position='dodge', stat='identity', width=.8)
    g += p9.coord_cartesian(ylim=ylim)
    g += p9.scale_fill_manual(['#999999', '#EA5F94', '#FFB14E'])
    g += p9.theme_void(base_size=FONT_SIZE, base_family='Arial')
    g += p9.theme(
        plot_background=p9.element_rect(fill='white'),
        panel_grid_major_y=p9.element_line(),
        axis_text_x=p9.element_text(margin={'t': 10}),
        axis_text_y=p9.element_text(margin={'r': 8}),
        legend_position=(.7, .9),
        legend_direction='horizontal',
        legend_title=p9.element_blank(),
        legend_text=p9.element_text(size=FONT_SIZE),
        legend_box_margin=0,
        figure_size=(12, 3)
    )
    g.save(filename=output_file(output))


def main():
    for clwe in ['PROC', 'CCA', 'RCSLS']:
        plot_bli(clwe, 'bli-train.csv', 'bli-test.csv', 'bli-{}.pdf'.format(clwe.lower()), (40, 100))
        plot_downstream(clwe, 'cldc.csv', 'cldc-{}.pdf'.format(clwe.lower()), (40, 100))
        plot_downstream(clwe, 'cldp.csv', 'cldp-{}.pdf'.format(clwe.lower()), (20, 80))


if __name__ == '__main__':
    main()
