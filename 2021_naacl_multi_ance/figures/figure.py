import json
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style('white')

df = pd.read_csv("multi-ance-ablation.csv")

print(df['Beamsize'])
print(df['PassageEM'])
df['Beamsize'] = df['Beamsize']

plt.gcf()
fig, ax = plt.subplots(figsize=(5, 3))

edge_df = pd.DataFrame(
    {'Beamsize': df['Beamsize'],
     'PassageEM': df['PassageEM'],
     }).sort_values(by=['Beamsize']).reset_index()  # .sort_values(
# by='count').reset_index()
edge_df.plot.line(x='Beamsize', y='PassageEM', ax=ax,
                  legend=False, fontsize=12, marker='o')
# edge_df.plot.bar(x='Edge', y='EdgeAccu', ax=ax,
#                   legend=False, fontsize=12)

plt.xlabel("Beam Size", fontsize=18)
plt.yticks(np.arange(75, 80, 1))
plt.ylabel("Passage EM", fontsize=18)
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
# plt.show()
sns.despine()

plt.savefig("beamEM1.pdf")

