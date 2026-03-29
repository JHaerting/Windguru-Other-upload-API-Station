[![FMI to Windguru Sync](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml/badge.svg)](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml)

This script adds two weather stations from ilmatieteenlaitos.fi to windguru.cz via the "Other (upload API)" option when registering a station.

This script currently runs every 10min, i.e. as often as ilmatieteenlaitos.fi updates the wind speed and direction.

  To change the interval change the schedule in the .yml file to whatever you want to use:
  
    schedule:
    #Enter desired time interval in minutes below
    - cron: '*/10 * * * *'

To add your own stations, register a station at windguru and then create your own secrets
WG_UID_1 and WG_PASS_1 as well as WG_UID_2  and WG_PASS_2 matching the stations UID and API PW entered at windguru.

Stations and their associated FMISIDs can be found here: https://en.ilmatieteenlaitos.fi/observation-stations

Data from the stations and a map with their location can be found here: https://en.ilmatieteenlaitos.fi/download-observations

Some reporsitory activity, e.g. a new committ must occur every 60 days for this script to keep running.

I made all of this using Gemini 3.
