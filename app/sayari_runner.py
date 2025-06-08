import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from sayari import Sayari
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut

# === Setup API Clients and Config ===
load_dotenv()
sayari_client = Sayari(
    client_id=os.getenv("SAYARI_CLIENT_ID"),
    client_secret=os.getenv("SAYARI_CLIENT_SECRET")
)
geolocator = GoogleV3(api_key=os.getenv("GOOGLE_MAPS_API_KEY"), timeout=10)

# === Risk Scoring ===
def score_entity_risk(entity):
    score = 0.0
    if getattr(entity, "sanctioned", False):
        score += 4
    if getattr(entity, "pep", False):
        score += 2
    score += 0.5 * len(getattr(entity, "risk", {}))
    if getattr(entity, "psa_count", 0) > 5:
        score += 1
    if getattr(entity, "related_entities_count", 0) > 25:
        score += 1
    return score

def categorize_risk_level(score):
    if score >= 18:
        return "High"
    elif score >= 12:
        return "Medium"
    else:
        return "Low"

# === Geolocation Utility ===
def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        pass
    return None, None

# === Set Base Directory ===
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(base_dir, "..", "data"))

# === Load Input Data ===
input_csv_path = os.path.join(data_dir, "entities.csv")
input_df = pd.read_csv(input_csv_path)

enriched_entities = []
unmatched_entities = []

# === Process Entities ===
for _, row in input_df.iterrows():
    name = row["name"]
    address = row["address"]
    country = row["country"]

    try:
        resolution_response = sayari_client.resolution.resolution(
            name=name, address=address, country=country
        )
        entity_matches = resolution_response.data or []

        if entity_matches:
            entity = entity_matches[0]
            entity_id = entity.entity_id
            print(f"✅ Resolved: {name} → {entity_id}")

            details = sayari_client.entity.get_entity(id=entity_id, relationships_limit=1)
            entity_data = details.model_dump() if hasattr(details, "model_dump") else details.__dict__

            risk_score = score_entity_risk(details)
            risk_level = categorize_risk_level(risk_score)

            address_list = entity_data.get("addresses", [])
            latitude, longitude = geocode_address(address_list[0]) if address_list else (None, None)

            enriched_entities.append({
                "name": name,
                "entity_id": entity_id,
                "label": entity.label,
                "type": entity.type,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
                "resolved_entity": entity_data,
                "psa_count": entity_data.get("psa_count", 0),
                "sanctioned": entity_data.get("sanctioned", False),
                "pep": entity_data.get("pep", False),
                "related_entities_count": entity_data.get("related_entities_count", 0)
            })
        else:
            print(f"⚠️ No match for {name}")
            unmatched_entities.append(name)

    except Exception as e:
        print(f"❌ Error processing {name}: {e}")

    time.sleep(0.5)

# === Save Enriched Results ===
results_path = os.path.join(data_dir, "sayari_results.json")
with open(results_path, "w", encoding="utf-8") as f:
    json.dump(enriched_entities, f, ensure_ascii=False, indent=2)

# === Create Summary CSV ===
summary_data = [
    {
        "Name": entity["name"],
        "PSA Count": entity["psa_count"],
        "Sanctioned": entity["sanctioned"],
        "Politically Exposed Person": entity["pep"],
        "Related Entities Count": entity["related_entities_count"],
        "Risk Score": entity["risk_score"],
        "Risk Level": entity["risk_level"],
        "Country": entity["country"],
        "Latitude": entity["latitude"],
        "Longitude": entity["longitude"]
    }
    for entity in enriched_entities
]

summary_path = os.path.join(data_dir, "sayari_summary.csv")
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(summary_path, index=False)

print(f"✅ Done: Results saved to '{results_path}' and '{summary_path}'")