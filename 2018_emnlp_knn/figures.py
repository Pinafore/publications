import os
from generate_colorize import prepare_colorize, latex_colorize

def table_2(output_dir):
    '''main saliency comparison table'''
    outfile = open(os.path.join(output_dir, 'table_2.tex'), 'w')
    outfile.write(
'''
\\begin{table*}[t]
\\centering
\\begin{tabular}{lp{0.6\\textwidth}}
\\toprule
\\textbf{Method} & \\textbf{Saliency Map} \\\\
\\midrule
'''
)
    text_1 = 'an intelligent fiction about learning through cultural clash'.split()
    rows = [
            ('Conformity', text_1, [0.5, 0.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
            ('Confidence', text_1, [0.5, 0.1, 0.7, 0.6, 0.5, 0.5, 0.5, 0.9]),
            ('Gradient', text_1, [0.5, 0.2, 0.8, 0.6, 0.5, 0.5, 0.5, 0.8]),
            ]

    for method, text, scores in rows:
        outfile.write('{} & {}. \\\\\n'.format(method, latex_colorize(text, scores)))
    outfile.write('\\midrule\n')

    row = [('<Schweiger>', 0.5),
           ('is', 0.5),
           ('talented', 0.3),
           ('and', 0.5),
           ('terribly', 0.5),
           ('charismatic', 0.3),
           # (', qualities', 0.5),
           # ('essential', 0.5),
           # ('to', 0.5),
           # ('both', 0.5),
           # ('movie', 0.5),
           # ('stars', 0.5),
           # ('and', 0.5),
           # ('social', 0.5),
           # ('<anarchists>', 0.5),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('Conformity & {}. \\\\\n'.format(
        latex_colorize(text, scores)))

    row = [('<Schweiger>', 0.65),
           ('is', 0.5),
           ('talented', 0.3),
           ('and', 0.5),
           ('terribly', 0.8),
           ('charismatic', 0.3),
           # (', qualities', 0.5),
           # ('essential', 0.5),
           # ('to', 0.5),
           # ('both', 0.5),
           # ('movie', 0.7),
           # ('stars', 0.5),
           # ('and', 0.5),
           # ('social', 0.5),
           # ('<anarchists>', 0.7),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('Confidence & {}. \\\\\n'.format(
        latex_colorize(text, scores)))

    row = [('<Schweiger>', 0.65),
           ('is', 0.5),
           ('talented', 0.3),
           ('and', 0.5),
           ('terribly', 0.9),
           ('charismatic', 0.3),
           # (', qualities', 0.5),
           # ('essential', 0.5),
           # ('to', 0.5),
           # ('both', 0.5),
           # ('movie', 0.7),
           # ('stars', 0.5),
           # ('and', 0.5),
           # ('social', 0.5),
           # ('<anarchists>', 0.7),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('Gradient & {}. \\\\\n'.format(
        latex_colorize(text, scores)))
    outfile.write('\\midrule\n')

    row = [('Diane', 0.5),
           ('Lane', 0.5),
           ('shines', 0.2),
           ('in', 0.5),
           ('unfaithful', 0.5),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('Conformity & {}. \\\\\n'.format(
        latex_colorize(text, scores)))
    row = [('Diane', 0.3),
           ('Lane', 0.6),
           ('shines', 0.3),
           ('in', 0.5),
           ('unfaithful', 0.7),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('Confidence & {}. \\\\\n'.format(
        latex_colorize(text, scores)))
    row = [('Diane', 0.4),
           ('Lane', 0.6),
           ('shines', 0.3),
           ('in', 0.5),
           ('unfaithful', 0.8),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('Gradient & {}. \\\\\n'.format(
        latex_colorize(text, scores)))
    outfile.write('\\bottomrule\n')

    outfile.write(
'''
\\end{tabular}
\\vspace{8pt}
\\begin{tabular}{c}
Color Legend\quad  \mybox{color2}{Positive Impact}\quad \mybox{color7}{Negative Impact}
\\end{tabular}
\\caption{Comparison of interpretation approaches on \\abr{sst} test
examples for the LSTM model. Blue indicates positive impact and red
indicates negative impact. Our method (\\textit{Conformity}
\loo{}) has higher precision, rarely assigning
importance to extraneous words such as ``about'' or ``movie''.}
\\label{table:saliency_maps}
\\end{table*}
'''
)


def table_3(output_dir):
    '''main saliency comparison table'''
    outfile = open(os.path.join(output_dir, 'table_3.tex'), 'w')
    outfile.write(
            '''
\\begin{table*}[t]
\\centering
\\begin{tabular}{llp{0.6\\textwidth}}
\\toprule
\\textbf{Prediction} & \\textbf{Input} & \\textbf{Saliency Map} \\\\
\\midrule
'''
)

    row = [('a', 0.5),
           ('young', 0.8),
           ('boy', 0.7),
           ('swims', 0.2),
           ('in', 0.4),
           ('his', 0.65),
           ('pool', 0.4),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('\multirow{2}{*}{Contradiction} & Premise & a young boy reaches for and touches the propeller of a vintage aircraft.  \\\\\n')
    outfile.write('& Hypothesis & {}. \\\\\n'.format(
        latex_colorize(text, scores)))
    outfile.write('\\midrule\n')

    row = [('the', 0.5),
           ('pets', 0.5),
           ('are', 0.5),
           ('sleeping', 0.2),
           ('on', 0.5),
           ('the', 0.5),
           ('grass', 0.5),
           ]
    text, scores = list(map(list, zip(*row)))
    outfile.write('\multirow{2}{*}{Contradiction} & Premise & a brown dog and a black dog in the edge of the ocean with a wave under them boats are on the water in the background.  \\\\\n')
    outfile.write('& Hypothesis & {}. \\\\\n'.format(
        latex_colorize(text, scores)))
    outfile.write('\\midrule\n')

    outfile.write('& Premise & man in a blue shirt standing in front of a structure painted with geometric designs.\\\\\n')
    text = 'a man is wearing a blue shirt'.split()
    scores = [0.5, 0.65, 0.5, 0.2, 0.5, 0.65, 0.5]
    outfile.write('Entailment & Hypothesis & {}.\\\\\n'.format(
        latex_colorize(text, scores)))

    text = 'a man is wearing a black shirt'.split()
    scores = [0.5, 0.65, 0.5, 0.2, 0.5, 0.65, 0.5]
    outfile.write('\\textcolor{red}{Entailment} & Hypothesis & ' + latex_colorize(text, scores) + '.\\\\\n')
    outfile.write('\\bottomrule\n')

    outfile.write(
'''
\\end{tabular}
\\vspace{8pt}
\\begin{tabular}{c}
Color Legend\quad  \mybox{color2}{Positive Impact}\quad \mybox{color7}{Negative Impact}
\\end{tabular}
\\caption{Interpretations generated with conformity \loo{} align with
annotation biases identified in \\abr{snli}. In the second example, the
model puts emphasis on the word ``sleeping'', disregarding other words
that could indicate the Neutral class. The final example diagnoses a
model's incorrect Entailment prediction (shown in red). Green
highlights indicate words that support the classification decision
made (shown in parenthesis), pink highlights indicate words that
support a different class.}
\\label{table:annotation_artifacts}
\\end{table*}
'''
)


if __name__ == '__main__':
    prepare_colorize('2018_emnlp_knn')
    table_2('2018_emnlp_knn/sections')
    table_3('2018_emnlp_knn/sections')
