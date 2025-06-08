# Sayari Risk Analysis Project

This project demonstrates how to use Sayari APIs to identify, enrich, and visualize entity risk data using a multi-step Python application. It includes:

- ✅ **Data Enrichment** via Sayari and Google Maps APIs  
- 📊 **Risk Dashboard** (interactive bar chart + searchable table using Dash)  
- 🗺️ **Geographic Risk Map** (folium-based HTML map)

---

## 📦 Prerequisites

Make sure you have the following installed:

- Python 3.8+ (tested on 3.13)
- `pip` (Python package manager)

### 🔑 Environment Variables

You will need valid API credentials. Create a `.env` file in the root directory with the following keys:

```env
SAYARI_CLIENT_ID=your_sayari_client_id
SAYARI_CLIENT_SECRET=your_sayari_client_secret
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

---

## 🛠️ Setup

1️⃣ Clone the repository:
```
git clone https://github.com/essahijazi/sayari-project.git
cd sayari-project
```
2️⃣ Install dependencies:
```
pip install -r requirements.txt
```

---

## 🚀 How to Run the Apps

1️⃣ Data Enrichment
This script enriches entity data using the Sayari API and geocodes them via Google Maps.
```
python3 app/sayari_runner.py
```
Expected Output:

- Creates data/sayari_results.json – raw enriched entity data

- Creates data/sayari_summary.csv – cleaned summary used by the dashboard and map

- Console logs indicating entity resolution and scoring status

2️⃣ Launch the Risk Dashboard
This runs a Dash app showing an interactive chart and a searchable table.
```
python3 app/risk_dashboard.py
```
Then open your browser to:
👉 http://localhost:8050/

Expected Output:

- Bar chart showing distribution of entities by risk level
- Searchable entity detail table

3️⃣ Generate the Geographic Risk 
```
python3 app/plot_geocoded_map.py
```
Expected Output:

- Opens a full-screen map in your default browser
- Saves the map to static/risk_map.html

---

## 📂 Project Structure
```
sayari-project/
├── app/
│   ├── sayari_runner.py          # API enrichment logic
│   ├── risk_dashboard.py         # Dash-based risk dashboard
│   ├── plot_geocoded_map.py      # Generates folium HTML map
├── data/
│   ├── entities.csv              # Input file
│   ├── sayari_results.json       # Output JSON from enrichment
│   └── sayari_summary.csv        # Output CSV for dashboard/map
├── static/
│   └── risk_map.html             # Output HTML map
├── .env                          # API credentials (excluded from repo)
├── requirements.txt              # Python dependencies
└── README.md
```
