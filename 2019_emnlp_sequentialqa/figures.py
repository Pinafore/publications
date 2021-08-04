import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import spacy
from plotnine import *
from collections import Counter
import pandas as pd
#Spacy large model is NOTABLY better at pronoun detection than the small one

# Script to create plots for your paper
import pandas as pd
import numpy as np

from plotnine import *

palette = {2: ["#000000", "#CFB87C"],
           3: ["#000000", "#FACD00", "#DA1D2B"],
           4: ["#FACD00", "#CFB87C", "#b2df8a", "#33a02c"]}

kROOT_DIR = "2019_emnlp_sequentialqa"

def datadir(filename):
    return "%s/data/%s" % (kROOT_DIR, filename)

def gfxdir(filename):
    return "%s/auto_fig/%s" % (kROOT_DIR, filename)

def _extract_keywords(text, tag):
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(text)
    return [word.text.lower() for word in doc if word.pos_ == tag] #or word.pos_ == 'NOUN'  ]
    
def extract_keywords(text, tag, cachefile=''):
    if cachefile:
        filename = datadir("%s.%s" % (cachefile, tag))
        try:
            with open(filename) as infile:
                return infile.read().split("\n")
        except IOError:
            words = _extract_keywords(text, tag)
            with open(filename, 'w') as outfile:
                print("Caching POS tags to %s" % filename)
                for ii in words:
                    outfile.write("%s\n" % ii)
            return words
    else:
        return _extract_keywords(text, tag)
            

if __name__ == "__main__":
    with open(datadir('val_rplc-1st-pro-with-title.txt')) as f:
        autopronouns = pd.read_table(f, header=None)  

    with open(datadir('val.json')) as f:
        val = pd.read_json(f)
    
    with open(datadir('val_brnn_glv.txt')) as f:
        sts = pd.read_table(f)  
    
    comparison_pd = pd.concat([autopronouns, val, sts], axis = 1)

    quac_length = sum([len(q.split()) for q in comparison_pd['Question']])/len(comparison_pd)
    rewrite_length = sum([len(q.split()) for q in comparison_pd['Reference']])/len(comparison_pd)
    baseline_length = sum([len(q.split()) for q in comparison_pd[0]])/len(comparison_pd)
    s2s_length = sum([len(q.split()) for q in comparison_pd['s2s']])/len(comparison_pd)

    print('Lengths', quac_length, rewrite_length, baseline_length, s2s_length)

    counts = {}
    for dataset_name, dataset in [("Original", comparison_pd['Question']),
                                      ("Reference", comparison_pd['Reference']),
                                      ("Pronoun Sub", comparison_pd[0]),
                                      ("Seq2Seq", comparison_pd['s2s'])]:
        dataset_examples = len(dataset)
        counts[("Average Length", dataset_name)] = sum(len(x.split()) for x in dataset) / dataset_examples
        for tag, tag_description in [("PROPN", "Proper Noun Ratio"), ("PRON", "Pronoun Ratio")]:
            counts[(tag_description, dataset_name)] = len(extract_keywords("\n".join(x for x in dataset), tag, dataset_name)) / dataset_examples

    print(counts)
    datasets = []
    ratios = []
    tags = []
    for tag, dataset_name in counts:
        tags.append(tag)
        datasets.append(dataset_name)
        ratios.append(counts[(tag, dataset_name)])

    ratio_frame = pd.DataFrame(list(zip(tags, datasets, ratios)),
                               columns=["Tag", "Dataset", "Val"])

    print(ratio_frame.head())

    length_and_ratio = (ggplot(aes(x='Dataset', y='Val'), data=ratio_frame) +
                            geom_bar(stat='identity') + # coord_flip() +
                            facet_grid("Tag~", scales="free")) + theme(axis_title_y=element_blank(), axis_title_x=element_blank(), figure_size=(4, 5))
    # quac_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd['Question']])/ len(comparison_pd['Question'])
    # rewrite_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd['Reference']])/ len(comparison_pd['Reference'])
    # baseline_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd[0]])/ len(comparison_pd[0])
    # s2s_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd['s2s']])/ len(comparison_pd['s2s'])

    # print('Prop nouns', quac_propnouns, rewrite_propnouns, baseline_propnouns, s2s_propnouns)


    # quac_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd['Question']])/ len(comparison_pd['Question'])
    # rewrite_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd['Reference']])/ len(comparison_pd['Reference'])
    # baseline_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd[0]])/ len(comparison_pd[0])
    # s2s_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd['s2s']])/ len(comparison_pd['s2s'])
    # print('Pronouns', quac_pronouns, rewrite_pronouns, baseline_pronouns, s2s_pronouns)

    # [quac_length, quac_propnouns, quac_pronouns]

    # storage = pd.DataFrame(columns=('Category', 'Count', 'Type'))

    # storage.loc[0] = ("1. Original", quac_length, "Num. Tokens")
    # storage.loc[1] = ("1. Original", quac_propnouns, "Prop. Nouns")
    # storage.loc[2] = ("1. Original", quac_pronouns, "Pronouns")

    # storage.loc[3] = ("4. Reference Rewrite", rewrite_length, "Num. Tokens")
    # storage.loc[4] = ("4. Reference Rewrite", rewrite_propnouns, "Prop. Nouns")
    # storage.loc[5] = ("4. Reference Rewrite", rewrite_pronouns, "Pronouns")

    # storage.loc[6] = ("3. Seq2Seq", s2s_length, "Num. Tokens")
    # storage.loc[7] = ("3. Seq2Seq", s2s_propnouns, "Prop. Nouns")
    # storage.loc[8] = ("3. Seq2Seq", s2s_pronouns, "Pronouns")

    # storage.loc[9] = ("2. Pronoun Replace", baseline_length, "Num. Tokens")
    # storage.loc[10] = ("2. Pronoun Replace", baseline_propnouns, "Prop. Nouns")
    # storage.loc[11] = ("2. Pronoun Replace", baseline_pronouns, "Pronouns")

    # plot = (ggplot(storage) 
    #         + aes( x= 'Type', y='Count',fill = 'Category') 
    #         + theme_light()  
    #         + theme(panel_grid =element_blank()) 
    #         + geom_col(position = 'dodge') 
    #         + labs( x= "",) 
    #         + theme(text=element_text(size=18),  legend_text=element_text(size=14), legend_position='top'))

    length_and_ratio.save(gfxdir('length_and_ratio.pdf'))
