import pandas as pd
import os
import folium
import webbrowser
from branca.element import Template, MacroElement

class RiskMapVisualizer:
    def __init__(self, csv_file: str = "../data/sayari_summary.csv", html_output: str = "../static/risk_map.html"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_file = os.path.abspath(os.path.join(base_dir, csv_file))
        self.html_output = os.path.abspath(os.path.join(base_dir, html_output))
        self.color_map = {
            "High": "darkred",
            "Medium": "darkorange",
            "Low": "gold"
        }
        self.map = None
        self.entity_df = None

    def load_and_filter_data(self):
        df = pd.read_csv(self.csv_file)
        self.entity_df = df.dropna(subset=["Latitude", "Longitude"])

    def initialize_map(self):
        self.map = folium.Map(
            location=[20, 0],
            zoom_start=2,
            tiles="CartoDB positron",
            control_scale=True,
            no_wrap=False,
            max_bounds=True,
            min_zoom=2,
            max_zoom=16
        )
        self.map.fit_bounds([[80, -180], [-80, 180]])

    def add_entity_markers(self):
        for _, row in self.entity_df.iterrows():
            name = row["Name"]
            risk_level = row["Risk Level"]
            risk_score = row["Risk Score"]
            latitude = row["Latitude"]
            longitude = row["Longitude"]
            color = self.color_map.get(risk_level, "blue")

            tooltip = f"{name}<br>Risk Level: {risk_level}<br>Risk Score: {risk_score:.1f}"

            folium.CircleMarker(
                location=[latitude, longitude],
                radius=6,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=tooltip
            ).add_to(self.map)

    def inject_fullscreen_css(self):
        css_template = """
        {% macro html(this, kwargs) %}
        <style>
            html, body {
                height: 100%;
                margin: 0;
            }
            #map {
                position: absolute;
                top: 0;
                bottom: 0;
                width: 100%;
            }
        </style>
        {% endmacro %}
        """
        css_macro = MacroElement()
        css_macro._template = Template(css_template)
        self.map.get_root().add_child(css_macro)

    def save_and_open_map(self):
        self.map.save(self.html_output)
        webbrowser.open(self.html_output)
        print(f"✅ Map saved and opened: {self.html_output}")

    def run(self):
        self.load_and_filter_data()
        self.initialize_map()
        self.add_entity_markers()
        self.inject_fullscreen_css()
        self.save_and_open_map()

if __name__ == "__main__":
    visualizer = RiskMapVisualizer()
    visualizer.run()