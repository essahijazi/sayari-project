import os
import pandas as pd
import dash
from dash import html, dcc, Input, Output, dash_table
import plotly.express as px

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, "../data/sayari_summary.csv"))
df = pd.read_csv(csv_path)

visible_columns = [
    "Name", "PSA Count", "Sanctioned",
    "Politically Exposed Person", "Related Entities Count",
    "Risk Score", "Risk Level"
]

# Bar chart
risk_counts = df["Risk Level"].value_counts().reindex(
    ["Low", "Medium", "High"]
).fillna(0).reset_index()
risk_counts.columns = ["Risk Level", "Count"]

bar_fig = px.bar(
    risk_counts, x="Risk Level", y="Count", color="Risk Level",
    color_discrete_map={
        "Low": "#ffeb3b",
        "Medium": "#ff9800",
        "High": "#f44336"
    },
    title="Risk Level Distribution"
)

# Dash app
app = dash.Dash(__name__)
app.title = "Entity Risk Dashboard"

app.layout = html.Div([
    html.H1("Sayari Entity Risk Dashboard", style={"textAlign": "center"}),
    dcc.Graph(figure=bar_fig),
    html.Hr(),
    html.Div([
        html.Label("Search by Name:"),
        dcc.Input(id="search-input", type="text", placeholder="Enter name..."),
        dash_table.DataTable(
            id="risk-table",
            columns=[
                {"name": col, "id": col, "type": "text"} for col in visible_columns
            ],
            data=df[visible_columns].to_dict("records"),
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "fontFamily": "Arial", "fontSize": 12},
            style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
            page_size=10,
            sort_action="none",
            filter_action="none"
        )
    ])
])

@app.callback(
    Output("risk-table", "data"),
    Input("search-input", "value")
)
def filter_table(search_value):
    if not search_value:
        return df[visible_columns].to_dict("records")
    filtered = df[df["Name"].str.contains(search_value, case=False, na=False)]
    return filtered[visible_columns].to_dict("records")

if __name__ == "__main__":
    app.run(debug=True)
