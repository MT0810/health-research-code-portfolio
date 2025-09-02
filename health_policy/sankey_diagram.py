import os
import pandas as pd
import plotly.graph_objects as go

csv_path = "/Users/wangmengting/MT/MNC_Sanky.csv"

encodings_try = ["utf-8", "utf-8-sig", "gbk", "utf-16"]
for enc in encodings_try:
    try:
        df = pd.read_csv(csv_path, encoding=enc, engine="python")
        break
    except Exception:
        df = None
if df is None:
    raise RuntimeError("无法读取 CSV，请检查文件编码或分隔符。")

candidates = {
    "year": ["Year", "year", "年份"],
    "company": ["Company", "Sponsor", "公司", "MNC"],
    "phase": ["Phase", "phase", "阶段"],
}
def pick(col_keys):
    for c in col_keys:
        if c in df.columns:
            return c
    raise KeyError(f"列未找到，候选为：{col_keys}")

col_year   = pick(candidates["year"])
col_company= pick(candidates["company"])
col_phase  = pick(candidates["phase"])

df = df[[col_year, col_company, col_phase]].dropna()

yc = df.groupby([col_year, col_company]).size().reset_index(name="value")
cp = df.groupby([col_company, col_phase]).size().reset_index(name="value")

years    = [str(y) for y in sorted(df[col_year].unique())]
companies= list(df[col_company].dropna().unique())
phases   = list(df[col_phase].dropna().unique())

nodes = years + companies + phases
node_index = {name: i for i, name in enumerate(nodes)}

yc_sources = [node_index[str(y)] for y in yc[col_year]]
yc_targets = [node_index[c]     for c in yc[col_company]]
yc_values  = yc["value"].tolist()

cp_sources = [node_index[c]     for c in cp[col_company]]
cp_targets = [node_index[p]     for p in cp[col_phase]]
cp_values  = cp["value"].tolist()

sources = yc_sources + cp_sources
targets = yc_targets + cp_targets
values  = yc_values  + cp_values

fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=nodes,
        pad=18,
        thickness=14,
        line=dict(color="rgba(0,0,0,0)", width=0)
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
    )
)])
fig.update_layout(
    title="MNC Sankey",
    font=dict(size=12),
    width=1100,
    height=1100,
)
fig.show()
