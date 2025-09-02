import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

plt.rcParams['font.family'] = 'Helvetica'

feature_groups = {
    'Accuracy': [
        'Intrinsic', 'SSI', 'Robustness', 'Generalization', 'Conciseness', 'Up-to-dateness', 'Groundedness'
    ],
    'Trustworthiness': [
        'Safety and Security', 'Privacy', 'Bias', 'Interpretability'
    ],
    'Empathy': [
        'Emotional Support', 'Health Literacy', 'Fairness', 'Personalization'
    ],
    'Performance': [
        'Memory Efficiency', 'FLOP', 'Token Limit', 'Number of Parameters'
    ]
}
group_titles = list(feature_groups.keys())
outcome_order = [
    'Patient Satisfaction', 'Perceived Comprehension', 'Anxiety Scores', 'Depression Scores',
    'Pain Perception', 'Functional Recovery', 'Communication Preference', 'Educational Coverage'
]

df = pd.read_csv
df['Mentioned-Both'] = pd.to_numeric(df['Mentioned-Both'], errors='coerce').fillna(0).astype(int)
df['Intervention'] = df['Intervention'].apply(lambda x: x.split(' ', 1)[1] if ' ' in x else x)

colors = ['#F5F5F5', '#D1C4E9', '#7E57C2']
cmap = ListedColormap(colors)
norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

all_feats = []
data_matrix = []
for idx, group in enumerate(group_titles):
    feats = feature_groups[group]
    for feat in feats:
        all_feats.append(feat)
        row = []
        for outcome in outcome_order:
            val = df[(df['Intervention'] == feat) & (df['Outcome'] == outcome)]['Mentioned-Both']
            row.append(int(val.values[0]) if not val.empty else 0)
        data_matrix.append(row)
    if idx != len(group_titles) - 1:
        # 插入空行
        all_feats.append('')
        data_matrix.append([np.nan]*len(outcome_order))
data_matrix = np.array(data_matrix, dtype=float)

cell_height = 0.47
cell_width = 1.6
n_rows = len(all_feats)
n_cols = len(outcome_order)
fig_height = n_rows * cell_height + 2.5
fig_width = n_cols * cell_width + 2.5
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.axis('off')

for i in range(n_rows):
    for j in range(n_cols):
        if not np.isnan(data_matrix[i, j]):
            v = data_matrix[i, j]
            if v == 0:
                color = colors[0]
            elif v == 1:
                color = colors[1]
            elif v == 2:
                color = colors[2]
            rect = plt.Rectangle((j, n_rows-1-i), 1, 1, facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(rect)
            ax.text(j+0.5, n_rows-1-i+0.5, int(v), ha='center', va='center', color='black', fontsize=9, fontname='Helvetica')
        else:
            pass

for i in range(n_rows+1):
    if i == 0 or i == n_rows or all_feats[i-1] == '' or (i < n_rows and all_feats[i] == ''):
        ax.plot([0, n_cols], [n_rows-i, n_rows-i], color='black', linewidth=1)
    else:
        ax.plot([0, n_cols], [n_rows-i, n_rows-i], color='black', linewidth=1)

for j in range(n_cols+1):
    for i in range(n_rows):
        if all_feats[i] != '':
            ax.plot([j, j], [n_rows-1-i, n_rows-i], color='black', linewidth=1)

ax.set_yticks([n_rows-1-i+0.5 for i in range(n_rows) if all_feats[i] != ''])
ax.set_yticklabels([all_feats[i] for i in range(n_rows) if all_feats[i] != ''], fontsize=10, fontname='Helvetica')

ax.set_xticks([j+0.5 for j in range(n_cols)])
ax.set_xticklabels([o.replace(' ', '\n') for o in outcome_order], fontsize=9, fontname='Helvetica')
ax.xaxis.set_ticks_position('bottom')
ax.tick_params(axis='x', which='both', length=0)

cax = fig.add_axes([0.92, 0.82, 0.06, 0.018]) 
import matplotlib as mpl
cb1 = mpl.colorbar.ColorbarBase(
    cax, cmap=cmap, norm=norm, orientation='horizontal',
    ticks=[0, 1, 2]
)
cb1.set_ticklabels(['0', '1', '2'])
cb1.set_label('Mentioned Frequency', fontsize=9, fontname='Helvetica', labelpad=6)

plt.savefig('feature_outcome_heatmap_structured.pdf', format='pdf')
plt.show()
