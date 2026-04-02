[![FMI to Windguru Sync](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml/badge.svg)](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml)

This script adds three weather stations from ilmatieteenlaitos.fi to windguru.cz via the "Other (upload API)" option when registering a station.

This script currently runs every 10min, i.e. as often as ilmatieteenlaitos.fi updates the wind speed and direction. The script triggers via a request from cron-job.org and a personal access token to GitHub.
  
To add your own stations, register a station at windguru and then create your own secrets
WG_UID_1 and WG_PASS_1 etc. matching the stations UID and API PW entered at windguru.

Stations and their associated FMISIDs can be found here: https://en.ilmatieteenlaitos.fi/observation-stations

Data from the stations and a map with their location can be found here: https://en.ilmatieteenlaitos.fi/download-observations

Some reporsitory activity, e.g. a new committ must occur every 60 days for this script to keep running.

I made all of this using Gemini 3.

### Wind Statistics
_Statistics will appear here after data collection begins._
