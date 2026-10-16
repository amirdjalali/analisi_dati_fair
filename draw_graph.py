import plotly.express as px
import pandas as pd
from itertools import cycle, islice

def plot_repos_treemap(df, param="name", threshold=3):
    df[param] = df.apply(
        lambda r: r[param] if r["count"] > threshold else "Other", axis=1
    )
    df_grouped = df.fillna("").groupby([param])["count"].sum().reset_index()
    title=f"Repositories (threshold = {threshold})"
    shapes = ["/", "\\", "x", "-", "|", "+", "."]
    fig = px.treemap(
        df_grouped,
        path=[param],
        values="count",
        color=param,
        color_discrete_map={"Other": "lightgrey"}
    )
    n = len(fig.data[0].labels)
    shape_map = {"Other": "/"}
    seq = cycle(shapes)
    fig.data[0].marker.pattern.shape = [
        shape_map[lbl] if lbl in shape_map else next(seq)
        for lbl in fig.data[0].labels
    ]
    outline = "white 2px 0, white -2px 0, white 0 2px, white 0 -2px, white 1.5px 1.5px, white -1.5px 1.5px, white 1.5px -1.5px, white -1.5px -1.5px"
    fig.update_traces(
        marker_pattern_fillmode="overlay",
        marker_pattern_fgcolor="black",
        marker_pattern_size=6,
        marker_pattern_solidity=0.1,
        textfont=dict(color="black", shadow=outline)
    )
    filename = "repositories"
    df_grouped.to_csv(f"repo_plot.csv", index=False, encoding="utf-8")
    fig.write_image(f"{filename}.png", scale=2)
    fig.write_image(f"{filename}.svg")

    return fig

combined_counts = pd.read_csv("combined_counts.csv", encoding="utf-8")
repos_plot = plot_repos_treemap(combined_counts)
repos_plot.show()