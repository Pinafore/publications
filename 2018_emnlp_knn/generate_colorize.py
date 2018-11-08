import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

color_name = 'color{}'
define_color = '\definecolor{{{}}}{{HTML}}{{{}}}'
box = '\\mybox{{{}}}{{{}}}'


def latex_colorize(text, weights):
    s = ''
    for w, x in zip(text, weights):
        w = w.replace('<', '$<$').replace('>', '$>$')
        color = max(0, np.digitize(x, np.arange(0, 1, 0.1)) - 1)
        s += ' ' + box.format(color_name.format(color), w)
    return s


def prepare_colorize(file_dir):
    with open(os.path.join(file_dir, 'colorize.tex'), 'w') as f:
        f.write('\\usepackage{tikz}\n')
        f.write('\\usepackage{xcolor}\n')
        cmap = plt.cm.get_cmap('bwr')
        for i, x in enumerate(np.arange(0, 1, 0.1)):
            rgb = matplotlib.colors.rgb2hex(cmap(x)[:3])
            # convert to upper to circumvent xcolor bug
            f.write(define_color.format(color_name.format(i), rgb[1:].upper()))
            f.write('\n')
        f.write('''\\newcommand*{\mybox}[2]{\\tikz[anchor=base,baseline=0pt,rounded corners=0pt, inner sep=0.2mm] \\node[fill=#1] (X) {#2};}''')
