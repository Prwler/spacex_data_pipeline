import pandas as pd


def transform_rockets(raw_rockets):
    df = pd.json_normalize(raw_rockets)

    cleaned = df.loc[:, [
        "id", "name", "type", "active",
        "stages", "boosters", "company", "country"
    ]].rename(columns={"id": "rocket_id"})

    return cleaned


def transform_payloads(raw_payloads):
    df = pd.json_normalize(raw_payloads)

    cleaned = df.loc[:, [
        "id", "name", "type", "mass_kg",
        "orbit", "customers", "manufacturers"
    ]].rename(columns={"id": "payload_id"})

    return cleaned


def transform_launches(raw_launches):
    df = pd.json_normalize(raw_launches)

    cleaned = df.loc[:, [
        "id", "name", "date_utc",
        "rocket", "success", "upcoming", "flight_number",
        "payloads"
    ]].rename(columns={
        "id": "launch_id",
        "rocket": "rocket_id",
        "payloads": "payload_ids"
    })

    # convert to timestamp
    cleaned.loc[:, "date_utc"] = pd.to_datetime(cleaned["date_utc"])

    # fillna and ensure boolean dtype
    cleaned.loc[:, "success"] = cleaned["success"].fillna(False).astype(bool)

    # For table join
    payload_mapping = cleaned.loc[:, ["launch_id", "payload_ids"]].copy()

    return cleaned.drop(columns=["payload_ids"]), payload_mapping
