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
nlp = spacy.load('en_core_web_lg')

with open('val_rplc-1st-pro-with-title.txt') as f:
    autopronouns = pd.read_table(f, header=None)  

with open('val.json') as f:
    val = pd.read_json(f)
    
with open('val_brnn_glv.txt') as f:
    sts = pd.read_table(f)  
    
comparison_pd = pd.concat([autopronouns, val, sts], axis = 1)

quac_length = sum([len(q.split()) for q in comparison_pd['Question']])/len(comparison_pd)
rewrite_length = sum([len(q.split()) for q in comparison_pd['Reference']])/len(comparison_pd)
baseline_length = sum([len(q.split()) for q in comparison_pd[0]])/len(comparison_pd)
s2s_length = sum([len(q.split()) for q in comparison_pd['s2s']])/len(comparison_pd)

print('Lengths', quac_length, rewrite_length, baseline_length, s2s_length)

def extract_keywords(text):
    doc = nlp(text)
    return [word.text.lower() for word in doc if word.pos_ == 'PROPN'] #or word.pos_ == 'NOUN'  ]

quac_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd['Question']])/ len(comparison_pd['Question'])
rewrite_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd['Reference']])/ len(comparison_pd['Reference'])
baseline_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd[0]])/ len(comparison_pd[0])
s2s_propnouns = sum([len(extract_keywords(q)) for q in comparison_pd['s2s']])/ len(comparison_pd['s2s'])

print('Prop nouns', quac_propnouns, rewrite_propnouns, baseline_propnouns, s2s_propnouns)

def extract_keywords(text):
    doc = nlp(text)
    return [word.text.lower() for word in doc if word.pos_ == 'PRON']

quac_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd['Question']])/ len(comparison_pd['Question'])
rewrite_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd['Reference']])/ len(comparison_pd['Reference'])
baseline_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd[0]])/ len(comparison_pd[0])
s2s_pronouns = sum([len(extract_keywords(q)) for q in comparison_pd['s2s']])/ len(comparison_pd['s2s'])
print('Pronouns', quac_pronouns, rewrite_pronouns, baseline_pronouns, s2s_pronouns)

[quac_length, quac_propnouns, quac_pronouns]

storage = pd.DataFrame(columns=('Category', 'Count', 'Type'))

storage.loc[0] = ("1. Original", quac_length, "Num. Tokens")
storage.loc[1] = ("1. Original", quac_propnouns, "Prop. Nouns")
storage.loc[2] = ("1. Original", quac_pronouns, "Pronouns")

storage.loc[3] = ("4. Reference Rewrite", rewrite_length, "Num. Tokens")
storage.loc[4] = ("4. Reference Rewrite", rewrite_propnouns, "Prop. Nouns")
storage.loc[5] = ("4. Reference Rewrite", rewrite_pronouns, "Pronouns")

storage.loc[6] = ("3. Seq2Seq", s2s_length, "Num. Tokens")
storage.loc[7] = ("3. Seq2Seq", s2s_propnouns, "Prop. Nouns")
storage.loc[8] = ("3. Seq2Seq", s2s_pronouns, "Pronouns")

storage.loc[9] = ("2. Pronoun Replace", baseline_length, "Num. Tokens")
storage.loc[10] = ("2. Pronoun Replace", baseline_propnouns, "Prop. Nouns")
storage.loc[11] = ("2. Pronoun Replace", baseline_pronouns, "Pronouns")

plot = (ggplot(storage) +
 aes( x= 'Type', y='Count',fill = 'Category')
+theme_light()
+ theme(panel_grid =element_blank())
 +geom_col(position = 'dodge')
 +labs( x= "",)
+ theme(text=element_text(size=18),  legend_text=element_text(size=14), legend_position='top'))

plot.save('f2_plotnine.pdf')