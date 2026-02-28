import requests
from app.helper import parse_arcgis_date

BASE_URL = "https://services2.arcgis.com/mJaJSax0KPHoCNB6/ArcGIS/rest/services/DRPComplianceRelProd/FeatureServer/0/query"

def fetch_layer():
    params = {
        "where": "1=1",
        "outFields": "*",
        "f": "json"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("features", [])

def parse_feeders(features):
    parsed = []

    for feature in features:
        attr = feature.get("attributes", {})

        feeder = {
            "redacted": attr.get("reacted"),
            "substation_name": attr.get("substationname"),
            "substation_id": attr.get("substationid"),
            "division": attr.get("division"),
            "voltage_kv": attr.get("voltage_kv"),
            "queued_dg": attr.get("queued_dg"),
            "existing_dg": attr.get("existing_dg"),
            "ungrounded_banks": attr.get("ungroundedbanks"),
            "geometry_x": safe_float(feature.get("geometry").get("x")),
            "geometry_y": safe_float(feature.get("geometry").get("y")),
            "last_update_on_map": parse_arcgis_date(attr.get("last_update_on_map")),
        }

        parsed.append(feeder)

    return parsed


def safe_float(value):
    try:
        return float(value) if value is not None else None
    except:
        return None