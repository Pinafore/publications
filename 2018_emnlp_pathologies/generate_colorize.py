import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

color_name = 'color{}'
define_color = '\definecolor{{{}}}{{HTML}}{{{}}}'
box = '\\mybox{{{}}}{{\strut{{{}}}}}'


def latex_colorize(text, weights):
    s = ''
    for w, x in zip(text, weights):
        color = np.digitize(x, np.arange(0, 1, 0.1)) - 1
        s += ' ' + box.format(color_name.format(color), w)
    return s


def prepare_colorize():
    with open('2018_emnlp_pathologies/colorize.tex', 'w') as f:
        cmap = plt.cm.get_cmap('Reds')
        for i, x in enumerate(np.arange(0, 1, 0.1)):
            rgb = matplotlib.colors.rgb2hex(cmap(x)[:3])
            # convert to upper to circumvent xcolor bug
            rgb = rgb[1:].upper() if x > 0 else 'FFFFFF'
            f.write(define_color.format(color_name.format(i), rgb))
            f.write('\n')
        f.write('''\\newcommand*{\mybox}[2]{\\tikz[anchor=base,baseline=0pt,rounded corners=0pt, inner sep=0.2mm] \\node[fill=#1!60!white] (X) {#2};}''')
        f.write('\n')
        f.write('''\\newcommand*{\mybbox}[2]{\\tikz[anchor=base,baseline=0pt,inner sep=0.2mm,] \\node[draw=black,thick,fill=#1!60!white] (X) {#2};}''')


def figure_4():
    words_weights = []
    words_weights.append([
        ("What", 0.1),
        ("company", 0.1),
        ("won", 0.1),
        ("free", 0.1),
        ("advertisement", 0.7),
        ("due", 0.1),
        ("to", 0.1),
        ("QuickBooks", 0.1),
        ("\\underline{contest}", 0.0),
        ("?", 0.1),
        ])
    words_weights.append([
        ("What", 0.1),
        ("company", 0.1),
        ("won", 0.1),
        ("free", 0.1),
        ("advertisement", 0.7),
        ("due", 0.1),
        ("to", 0.1),
        ("\\underline{QuickBooks}", 0.0),
        ("?", 0.1),
        ])
    words_weights.append([
        ("What", 0.3),
        ("company", 0.0),
        ("won", 0.1),
        ("free", 0.1),
        ("\\underline{advertisement}", 0.0),
        ("due", 0.1),
        ("to", 0.1),
        ("?", 0.5),
        ])
    words_weights.append([
        ("What", 0.1),
        ("\\underline{company}", 0.0),
        ("won", 0.1),
        ("free", 0.1),
        ("due", 0.1),
        ("to", 0.1),
        ("?", 0.5),
        ])
    words_weights.append([
        ("What", 0.1),
        ("won", 0.4),
        ("\\underline{free}", 0.0),
        ("due", 0.1),
        ("to", 0.0),
        ("?", 0.5),
        ])
    words_weights.append([
        ("What", 0.1),
        ("won", 0.1),
        ("due", 0.1),
        ("to", 0.1),
        ("\\underline{?}", 0.0),
        ])
    words_weights.append([
        ("What", 0.1),
        ("won", 0.4),
        ("due", 0.1),
        ("\\underline{to}", 0.0),
        ])
    words_weights.append([
        ("What", 0.4),
        ("won", 0.3),
        ("\\underline{due}", 0.1),
        ])
    words_weights.append([
        ("What", 0.3),
        ("\\underline{won}", 0.1),
        ])
    words_weights.append([
        ("What", 0.2),
        ])
    
    with open('2018_emnlp_pathologies/sections/figure_4.tex', 'w') as f:
        for ww in words_weights:
            words, weights = list(map(list, zip(*ww)))
            f.write(latex_colorize(words, weights)+'\\\\\n')


if __name__ == '__main__':
    prepare_colorize()
    figure_4()
