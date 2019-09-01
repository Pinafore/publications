import pandas as pd
from pandas.api.types import CategoricalDtype
from plotnine import *


def read_ratio_data(fname, languages, models):
    file = open(fname, 'r')
    pmis = []
    for lang in languages:
        for _ in range(120):
            file.readline()
        temp_pmis = []
        for _ in range(len(models)):
            temp_pmis.append([])
        for x in range(10):
            seg = file.readline().strip().split('\t')
            for i in range(len(models)):
                temp_pmis[i].append(float(seg[i]))
        pmis.append(temp_pmis)
        for _ in range(70):
            file.readline()
    file.close()
    return pmis


def draw_ratio_figures():
    languages = ['Arabic', 'Chinese', 'Spanish', 'Farsi', 'Russian']
    models = ['LDA', 'tLDA', 'MTM', 'MTM-TFIDF']
    paco_pmis = read_ratio_data('2019_emnlp_mtm/data/paco_ratio.txt', languages, models)
    inco_pmis = read_ratio_data('2019_emnlp_mtm/data/inco_ratio.txt', languages, models)

    d = {}
    d['Topic Coherence'] = []
    d['Models'] = []
    d['Languages'] = []
    d['Target Language Corpora Size Ratios'] = []
    d['Type'] = []
    for i, lang in enumerate(languages):
        for j, model in enumerate(models):
            d['Topic Coherence'].extend(paco_pmis[i][j])
            d['Target Language Corpora Size Ratios'].extend([(k + 1) * 10 for k in range(10)])
            d['Models'].extend([model for _ in range(10)])
            d['Languages'].extend([lang for _ in range(10)])
            d['Type'].extend(['PACO' for _ in range(10)])

            d['Topic Coherence'].extend(inco_pmis[i][j])
            d['Target Language Corpora Size Ratios'].extend([(k + 1) * 10 for k in range(10)])
            d['Models'].extend([model for _ in range(10)])
            d['Languages'].extend([lang for _ in range(10)])
            d['Type'].extend(['INCO' for _ in range(10)])

    df = pd.DataFrame(data=d)
    # print(df)

    model_cat = CategoricalDtype(categories=models, ordered=True)
    df['Models_Cat'] = df['Models'].astype(str).astype(model_cat)

    p = ggplot(aes(x='Target Language Corpora Size Ratios'), data=df) \
        + geom_point(aes(y='Topic Coherence', color='Models_Cat', shape='Models_Cat')) \
        + geom_line(aes(y='Topic Coherence', color='Models_Cat')) \
        + facet_grid(('Languages', 'Type'), scales='free_y', labeller=labeller(multi_line=False)) \
        + theme(legend_position=(0.5, 0.95), legend_direction='horizontal', legend_box_margin=0,
                legend_title=element_blank(), figure_size=(4, 5), panel_spacing_x=.03,
                panel_spacing_y=.05)  # Original Size (6.4, 4.8)
    p.save('2019_emnlp_mtm/auto_fig/ratio_vertical.pdf')


def plus(list1, list2):
    if len(list1) != len(list2):
        return []
    res = []
    for i in range(len(list1)):
        res.append(list1[i] + list2[i])
    return res


def minus(list1, list2):
    if len(list1) != len(list2):
        return []
    res = []
    for i in range(len(list1)):
        res.append(list1[i] - list2[i])
    return res


def read_cv_data(fname, languages, models):
    file = open(fname, 'r')
    pmis = []
    ses = []
    for _ in languages:
        for _ in range(10):
            file.readline()
        temp_pmis = []
        temp_ses = []
        for _ in range(len(models)):
            temp_pmis.append([])
            temp_ses.append([])
        for x in range(10):
            seg = file.readline().strip().split('\t')
            for i in range(len(models)):
                temp_pmis[i].append(float(seg[i]))
                temp_ses[i].append(float(seg[i + len(models)]))
        pmis.append(temp_pmis)
        ses.append(temp_ses)
    file.close()
    return pmis, ses


def draw_cv_figures():
    languages = ['Arabic', 'Chinese', 'Spanish', 'Farsi', 'Russian']
    models = ['LDA', 'ptLDA', 'MTM', 'MTM-TFIDF']
    paco_pmis, paco_ses = read_cv_data('2019_emnlp_mtm/data/paco-cv.txt', languages, models)
    inco_pmis, inco_ses = read_cv_data('2019_emnlp_mtm/data/inco-cv.txt', languages, models)

    d = {}
    d['Topic Coherence'] = []
    d['Errors'] = []
    d['Top Words'] = []
    d['Models'] = []
    d['Sizes'] = []
    d['Min'] = []
    d['Max'] = []
    d['Languages'] = []
    d['Type'] = []
    for i, lang in enumerate(languages):
        for j, model in enumerate(models):
            d['Topic Coherence'].extend(paco_pmis[i][j])
            d['Errors'].extend(paco_ses[i][j])
            d['Top Words'].extend([(k + 1) * 10 for k in range(10)])
            d['Models'].extend([model for _ in range(10)])
            d['Sizes'].extend([20.0 for _ in range(10)])
            d['Min'].extend(minus(paco_pmis[i][j], paco_ses[i][j]))
            d['Max'].extend(plus(paco_pmis[i][j], paco_ses[i][j]))
            d['Languages'].extend([lang for _ in range(10)])
            d['Type'].extend(['PACO' for _ in range(10)])

            d['Topic Coherence'].extend(inco_pmis[i][j])
            d['Errors'].extend(inco_ses[i][j])
            d['Top Words'].extend([(k + 1) * 10 for k in range(10)])
            d['Models'].extend([model for _ in range(10)])
            d['Sizes'].extend([20.0 for _ in range(10)])
            d['Min'].extend(minus(inco_pmis[i][j], inco_ses[i][j]))
            d['Max'].extend(plus(inco_pmis[i][j], inco_ses[i][j]))
            d['Languages'].extend([lang for _ in range(10)])
            d['Type'].extend(['INCO' for _ in range(10)])

    df = pd.DataFrame(data=d)
    # print(df)

    model_cat = CategoricalDtype(categories=models, ordered=True)
    df['Models_Cat'] = df['Models'].astype(str).astype(model_cat)

    p = ggplot(aes(x='Top Words'), data=df) \
        + geom_point(aes(y='Topic Coherence', color='Models_Cat', shape='Models_Cat')) \
        + geom_line(aes(y='Topic Coherence', color='Models_Cat')) \
        + facet_grid(('Languages', 'Type'), scales='free_y', labeller=labeller(multi_line=False)) \
        + theme(legend_position=(0.5, .95), legend_direction='horizontal', legend_box_margin=0,
                legend_title=element_blank(), figure_size=(4, 5), panel_spacing_x=.03, panel_spacing_y=.05)
    p.save('2019_emnlp_mtm/auto_fig/cv_vertical.pdf')


def draw_classification_bar_chart(dataset, languages, ha, nudge_y, upper, breaks):
    data = []
    with open('2019_emnlp_mtm/data/' + dataset + '.txt', 'r') as f:
        for line in f:
            segments = line.strip().split('\t')
            temp = []
            for segment in segments:
                temp.append(round(float(segment), 1))
            data.append(temp)

    models = ['MCTA', 'MTAnchor', 'LDA', 'ptLDA', 'MTM', 'MTM+TOP', 'MTM+TF-IDF', 'MTM+TF-IDF+TOP']
    models = models[::-1]
    tasks = ['Intra-Lingual', 'Cross-Lingual']
    d = {}
    d['Models'] = []
    d['Languages'] = []
    d['Task'] = []
    d['F1'] = []
    for i in range(len(models)):
        for j in range(len(tasks)):
            for k in range(len(languages)):
                d['Models'].append(models[len(models) - i - 1])
                d['Languages'].append(languages[k])
                d['Task'].append(tasks[j])
                d['F1'].append(data[i][j * len(tasks) + k])

    df = pd.DataFrame(data=d)
    # print(df)

    model_cat = CategoricalDtype(categories=models, ordered=True)
    df['Models_Cat'] = df['Models'].astype(str).astype(model_cat)
    task_cat = CategoricalDtype(categories=tasks, ordered=True)
    df['Task_Cat'] = df['Task'].astype(str).astype(task_cat)
    language_cat = CategoricalDtype(categories=languages, ordered=True)
    df['Languages_Cat'] = df['Languages'].astype(str).astype(language_cat)

    p = ggplot(aes(x='Models_Cat', y='F1'), data=df) \
        + geom_bar(stat='identity', fill="#FFD520", colour="#500000", size=0.5, show_legend=False) \
        + coord_flip() \
        + scale_y_continuous(limits=(0.0, upper), breaks=breaks) \
        + geom_text(aes(label='F1'), ha=ha, nudge_y=nudge_y) \
        + facet_grid(('Languages_Cat', 'Task_Cat'), labeller=labeller(multi_line=False)) \
        + theme(axis_title_y=element_blank(), axis_title_x=element_blank(), panel_spacing_x=.03, panel_spacing_y=.05, figure_size=(4, 5))
    p.save('2019_emnlp_mtm/auto_fig/' + dataset + '.pdf')


draw_ratio_figures()
draw_cv_figures()
draw_classification_bar_chart('lorelei', ['English', 'Sinhalese'], 'right', 15, 60, [0, 20, 40, 60])
draw_classification_bar_chart('wiki', ['English', 'Chinese'], 'right', 30, 125, [0, 25, 50, 75, 100])
