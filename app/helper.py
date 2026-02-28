import datetime

def parse_arcgis_date(value):
    if value is None:
        return None

    # If it's already datetime
    if isinstance(value, datetime.datetime):
        return value

    # ArcGIS often uses milliseconds
    try:
        return datetime.datetime.utcfromtimestamp(value / 1000)
    except:
        return None