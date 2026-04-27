[![FMI to Windguru Sync](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml/badge.svg)](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml)

This script adds three weather stations from ilmatieteenlaitos.fi to windguru.cz via the "Other (upload API)" option when registering a station. I hope to discover some kiting spots in Finland that way.

This script currently runs every 10min, i.e. as often as ilmatieteenlaitos.fi updates the wind speed and direction. The script triggers via a request from cron-job.org and a personal access token to GitHub.
  
To add your own stations, register a station at windguru and then create your own secrets
WG_UID_1 and WG_PASS_1 etc. matching the stations UID and API PW entered at windguru. Modify the sync_weather.py and sync.yml accordingly.
In the sync_weather.py you can find the only lines that need modifying under line 9 and in the sync.yml below line 29.

Stations and their associated FMISIDs can be found here: https://en.ilmatieteenlaitos.fi/observation-stations

Data from the stations and a map with their location can be found here: https://en.ilmatieteenlaitos.fi/download-observations

The script keeps running despite the 60 day GitHub limit because it automatically makes new commits via the read me.

I made all of this using Gemini 3.

### Wind Statistics

## 🌬️ Windy Days Tracker (Last 30 Days)
> Days where wind was **>14 knots** for at least **2 hours** (08:00 - 20:00).

**Hanko Tulliniemi**:
`2026-04-26` ✅ `2026-04-25` ✅ `2026-04-24` ✅ `2026-04-23` ✅ `2026-04-22` ✅ `2026-04-21` ✅ `2026-04-19` ✅ `2026-04-18` ✅ `2026-04-15` ✅ `2026-04-14` ✅ `2026-04-13` ✅ `2026-04-12` ✅ `2026-04-11` ✅ `2026-04-10` ✅ `2026-04-07` ✅ `2026-04-06` ✅ `2026-04-05` ✅ `2026-04-04` ✅

**Inari Kirakkajärvi**:
_No windy days tracked yet._

**Kalajoki Ulkokalla**:
`2026-04-27` ✅ `2026-04-26` ✅ `2026-04-25` ✅ `2026-04-23` ✅ `2026-04-22` ✅ `2026-04-21` ✅ `2026-04-18` ✅ `2026-04-14` ✅ `2026-04-08` ✅ `2026-04-07` ✅ `2026-04-05` ✅

**Kemi Ajos**:
`2026-04-27` ✅ `2026-04-25` ✅ `2026-04-24` ✅ `2026-04-22` ✅ `2026-04-21` ✅ `2026-04-07` ✅ `2026-04-06` ✅

**Lake Inari**:
`2026-04-27` ✅ `2026-04-26` ✅ `2026-04-24` ✅ `2026-04-23` ✅ `2026-04-22` ✅ `2026-04-21` ✅ `2026-04-16` ✅ `2026-04-10` ✅ `2026-04-09` ✅ `2026-04-08` ✅ `2026-04-07` ✅

**Yyteri**:
`2026-04-27` ✅ `2026-04-26` ✅ `2026-04-25` ✅ `2026-04-24` ✅ `2026-04-22` ✅ `2026-04-20` ✅ `2026-04-19` ✅ `2026-04-17` ✅ `2026-04-15` ✅ `2026-04-07` ✅ `2026-04-06` ✅ `2026-04-05` ✅ `2026-04-04` ✅

