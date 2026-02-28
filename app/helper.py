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
    
def feeder_to_text(feeder):
    return (
        f"Substation {feeder.substation_name} "
        f"with voltage {feeder.voltage_kv} kV, "
        f"existing DG {feeder.existing_dg}, "
        f"queued DG {feeder.queued_dg}, "
        f"division {feeder.division}."
    )