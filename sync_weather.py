import requests
import xml.etree.ElementTree as ET
import hashlib
import time
import os
import json
from datetime import datetime, timedelta

STATIONS = [ # make modifications below to add or remove weather stations.
    {"name": "Inari Kirakkajärvi", "fmisid": "102055", "wg_uid": os.environ.get('WG_UID_1'), "wg_pass": os.environ.get('WG_PASS_1')},
    {"name": "Lake Inari", "fmisid": "129963", "wg_uid": os.environ.get('WG_UID_2'), "wg_pass": os.environ.get('WG_PASS_2')},
    {"name": "Yyteri", "fmisid": "101267", "wg_uid": os.environ.get('WG_UID_3'), "wg_pass": os.environ.get('WG_PASS_3')},
    {"name": "Hanko Tulliniemi", "fmisid": "100946", "wg_uid": os.environ.get('WG_UID_4'), "wg_pass": os.environ.get('WG_PASS_4')},
    {"name": "Kemi Ajos", "fmisid": "101846", "wg_uid": os.environ.get('WG_UID_5'), "wg_pass": os.environ.get('WG_PASS_5')}, # Make sure there is a comma after this line.
]

LOG_FILE = "wind_history.json"

def get_fmi_measurements(fmisid):
    url = "https://opendata.fmi.fi/wfs"
    params = {
        "request": "getFeature",
        "storedquery_id": "fmi::observations::weather::timevaluepair",
        "fmisid": fmisid,
        "parameters": "ws_10min,wg_10min,wd_10min,t2m,p_sea,rh"
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
                latest_val = values[-1].text
                if latest_val and latest_val.lower() != 'nan':
                    val = float(latest_val)
                    if 'ws_10min' in param_url: data['wind_avg'] = val
                    elif 'wg_10min' in param_url: data['wind_max'] = val
                    elif 'wd_10min' in param_url: data['wind_direction'] = val
                    elif 't2m' in param_url: data['temperature'] = val
                    elif 'p_sea' in param_url: data['mslp'] = val
                    elif 'rh' in param_url: data['rh'] = val
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
        "wind_avg": round(data['wind_avg'] * 1.94384, 1),
        "wind_max": round(data.get('wind_max', data['wind_avg']) * 1.94384, 1),
        "wind_direction": int(data.get('wind_direction', 0)),
        "temperature": round(data.get('temperature', 0), 1),
        "mslp": data.get('mslp'),
        "rh": data.get('rh')
    }
    try:
        res = requests.get("https://www.windguru.cz/upload/api.php", params=wg_params, timeout=15)
        print(f"Windguru ({uid}): {res.text}")
    except Exception as e:
        print(f"Upload failed: {e}")

def update_logs_and_readme(all_observations):
    history = {}
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = {}

    now = datetime.now()
    for name, obs in all_observations.items():
        if name not in history: history[name] = []
        if 'wind_avg' in obs:
            history[name].append({
                "ts": now.isoformat(),
                "ws_knots": round(obs['wind_avg'] * 1.94384, 1)
            })
        
        cutoff = now - timedelta(days=31)
        history[name] = [e for e in history[name] if datetime.fromisoformat(e['ts']) > cutoff]

    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f)

    table = "\n\n## 🌬️ Windy Days Tracker (Last 30 Days)\n"
    table += "> Days where wind was **>14 knots** for at least **2 hours** (08:00 - 20:00).\n\n"
    
    for name in sorted(history.keys()):
        table += f"**{name}**:\n"
        day_stats = {}
        for e in history[name]:
            dt = datetime.fromisoformat(e['ts'])
            d_str = dt.strftime("%Y-%m-%d")
            if 8 <= dt.hour <= 20:
                if d_str not in day_stats: day_stats[d_str] = 0
                if e.get('ws_knots', 0) >= 14.0: day_stats[d_str] += 1
        
        windy_days = [d for d, count in day_stats.items() if count >= 12]
        if windy_days:
            table += " ".join([f"`{d}` ✅" for d in sorted(windy_days, reverse=True)]) + "\n\n"
        else:
            table += "_No windy days tracked yet._\n\n"

    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        marker = "### Wind Statistics"
        if marker in content:
            static_part = content.split(marker)[0]
            new_content = static_part + marker + table
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(new_content)
        else:
            print(f"Warning: Marker '{marker}' not found in README.md.")
    else:
        print("Error: README.md not found.")

if __name__ == "__main__":
    current_runs = {}
    for s in STATIONS:
        print(f"Checking {s['name']}...")
        obs = get_fmi_measurements(s['fmisid'])
        if obs:
            upload_to_windguru(s['wg_uid'], s['wg_pass'], obs)
            current_runs[s['name']] = obs
    
    if current_runs:
        update_logs_and_readme(current_runs)
