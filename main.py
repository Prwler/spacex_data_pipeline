from etl.extract import extract_launches, extract_rockets, extract_payloads
from etl.transform import (
    transform_launches,
    transform_payloads,
    transform_rockets
)
from etl.load import load_table

def run():

    # EXTRACT
    launches_raw = extract_launches()
    rockets_raw = extract_rockets()
    payloads_raw = extract_payloads()

    # TRANSFORM
    rockets_clean = transform_rockets(rockets_raw)
    payloads_clean = transform_payloads(payloads_raw)
    launches_clean, launch_payload_map = transform_launches(launches_raw)

    # LOAD
    load_table(rockets_clean, "rockets")
    load_table(payloads_clean, "payloads")
    load_table(launches_clean, "launches")

    # expand mapping into rows (launch_id, payload_id)
    mapping_rows = []
    for _, row in launch_payload_map.iterrows():
        for pid in row["payload_ids"]:
            mapping_rows.append({"launch_id": row["launch_id"], "payload_id": pid})

    import pandas as pd
    mapping_df = pd.DataFrame(mapping_rows)

    load_table(mapping_df, "launch_payloads")

    print("ETL completed successfully.")

if __name__ == "__main__":
    run()
