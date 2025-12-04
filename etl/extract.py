import requests

BASE_URL = "https://api.spacexdata.com/v4"

def extract_launches():
    r = requests.get(f"{BASE_URL}/launches")
    r.raise_for_status()
    return r.json()

def extract_rockets():
    r = requests.get(f"{BASE_URL}/rockets")
    r.raise_for_status()
    return r.json()

def extract_payloads():
    r = requests.get(f"{BASE_URL}/payloads")
    r.raise_for_status()
    return r.json()
