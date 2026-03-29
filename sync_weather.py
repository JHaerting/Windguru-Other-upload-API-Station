import requests
import xml.etree.ElementTree as ET
import hashlib
import time
import os
import sys

# Configuration: We use FMISID for FMI and environment variables for Windguru
STATIONS = [
    {
        "name": "Inari Kirakkajärvi",
        "fmisid": "102055",
        "wg_uid": os.environ.get('WG_UID_1'),
        "wg_pass": os.environ.get('WG_PASS_1')
    },
    {
        "name": "Inari Seitalaassa",
        "fmisid": "129963",
        "wg_uid": os.environ.get('WG_UID_2'),
        "wg_pass": os.environ.get('WG_PASS_2')
    }
]

def get_fmi_measurements(fmisid):
    """Fetches the latest wind and temp data from FMI WFS."""
    # We ask for the last 30 mins of data to ensure we catch the latest 10-min interval
    url = (
        f"https://opendata.fmi.fi/wfs?request=getFeature"
        f"&storedquery_id=fmi::observations::weather::timevaluepair"
        f"&fmisid={fmisid}&parameters=windspeedms,winddirection,temp"
    )
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        # Namespace mapping for FMI XML
        ns = {'wfs': 'http://www.opengis.net/wfs/2.0', 'om': 'http://www.opengis.net/om/2.0', 'waterml': 'http://www.opengis.net/waterml/2.0'}
        
        data = {}
        # FMI returns a series of 'point' elements. We want the very last value for each parameter.
        for member in root.findall('.//wfs:member', ns):
            # Identify which parameter this member belongs to
            obs_prop = member.find('.//om:observedProperty', ns)
            if obs_prop is None: continue
            param_url = obs_prop.get('{http://www.w3.org/1999/xlink}href')
            
            # Extract the latest value from the time-value pair
            values = member.findall('.//waterml:value', ns)
            if values:
                latest_val = values[-1].text
                if 'windspeedms' in param_url: data['wind_avg'] = float(latest_val)
                elif 'winddirection' in param_url: data['wind_direction'] = float(latest_val)
                elif 'temp' in param_url: data['temperature'] = float(latest_val)
        
        return data
    except Exception as e:
        print(f"Error fetching FMI data for {fmisid}: {e}")
        return None

def upload_to_windguru(uid, password, data):
    """Uploads data to Windguru using their GET API."""
    if not uid or not password:
        print("Missing Windguru credentials in environment variables.")
        return

    # Windguru requires MD5(salt + uid + password)
    salt = str(int(time.time()))
    hash_input = salt + uid + password
    auth_hash = hashlib.md5(hash_input.encode()).hexdigest()

    params = {
        "uid": uid,
        "salt": salt,
        "hash": auth_hash,
        "wind_avg": round(data['wind_avg'] * 1.94384, 1), # m/s to knots
        "wind_direction": int(data['wind_direction']),
        "temperature": round(data['temperature'], 1)
    }

    try:
        api_url = "https://www.windguru.cz/upload/api.php"
        res = requests.get(api_url, params=params, timeout=15)
        print(f"Windguru Response for {uid}: {res.text}")
    except Exception as e:
        print(f"Failed to upload to Windguru: {e}")

if __name__ == "__main__":
    for station in STATIONS:
        print(f"Processing {station['name']}...")
        measurements = get_fmi_measurements(station['fmisid'])
        
        if measurements and 'wind_avg' in measurements:
            upload_to_windguru(station['wg_uid'], station['wg_pass'], measurements)
        else:
            print(f"Skipping {station['name']} due to missing data.")
