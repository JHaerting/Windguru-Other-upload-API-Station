import requests
import xml.etree.ElementTree as ET
import hashlib
import time
import os

STATIONS = [
    {"name": "Inari Kirakkajärvi", "fmisid": "102055", "wg_uid": os.environ.get('WG_UID_1'), "wg_pass": os.environ.get('WG_PASS_1')},
    {"name": "Inari Seitalaassa", "fmisid": "129963", "wg_uid": os.environ.get('WG_UID_2'), "wg_pass": os.environ.get('WG_PASS_2')}
]

def get_fmi_measurements(fmisid):
    # Official FMI Parameter names: 
    # ws_10min = Wind Speed, wd_10min = Wind Direction, t2m = Temperature
    url = "https://opendata.fmi.fi/wfs"
    params = {
        "request": "getFeature",
        "storedquery_id": "fmi::observations::weather::timevaluepair",
        "fmisid": fmisid,
        "parameters": "ws_10min,wd_10min,t2m"
    }
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        ns = {'wfs': 'http://www.opengis.net/wfs/2.0', 'om': 'http://www.opengis.net/om/2.0', 'waterml': 'http://www.opengis.net/waterml/2.0'}
        
        data = {}
        for member in root.findall('.//wfs:member', ns):
            obs_prop = member.find('.//om:observedProperty', ns)
            if obs_prop is None: continue
            param_url = obs_prop.get('{http://www.w3.org/1999/xlink}href', '').lower()
            
            values = member.findall('.//waterml:value', ns)
            if values:
                # Get the last non-NaN value
                latest_val = values[-1].text
                if latest_val and latest_val.lower() != 'nan':
                    val = float(latest_val)
                    if 'ws_10min' in param_url: data['wind_avg'] = val
                    elif 'wd_10min' in param_url: data['wind_direction'] = val
                    elif 't2m' in param_url: data['temperature'] = val
        return data
    except Exception as e:
        print(f"Error for {fmisid}: {e}")
        return None

def upload_to_windguru(uid, password, data):
    if not all([uid, password, 'wind_avg' in data]): return
    salt = str(int(time.time()))
    auth_hash = hashlib.md5((salt + uid + password).encode()).hexdigest()
    
    wg_params = {
        "uid": uid, "salt": salt, "hash": auth_hash,
        "wind_avg": round(data['wind_avg'] * 1.94384, 1), # m/s to knots
        "wind_direction": int(data.get('wind_direction', 0)),
        "temperature": round(data.get('temperature', 0), 1)
    }
    try:
        res = requests.get("https://www.windguru.cz/upload/api.php", params=wg_params, timeout=15)
        print(f"Windguru ({uid}): {res.text}")
    except Exception as e:
        print(f"Upload failed: {e}")

if __name__ == "__main__":
    for s in STATIONS:
        print(f"Checking {s['name']}...")
        obs = get_fmi_measurements(s['fmisid'])
        if obs:
            upload_to_windguru(s['wg_uid'], s['wg_pass'], obs)
        else:
            print(f"No data for {s['name']}")
