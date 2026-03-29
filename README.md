[![FMI to Windguru Sync](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml/badge.svg)](https://github.com/JHaerting/Windguru-Other-upload-API-Station/actions/workflows/sync.yml)

This script adds two weather stations from ilmatieteenlaitos.fi to windguru.cz via the "Other (upload API)" option when registering a station.

This script currently runs every 10min, i.e. as often as ilmatieteenlaitos.fi updates the wind speed and direction.

  To change the interval change the schedule in the .yml file to whatever you want to use:
  
    schedule:
    - cron: '*/10 * * * *' #Enter desired time interval here.

Stations and their associated FMISIDs can be found here: https://en.ilmatieteenlaitos.fi/observation-stations
Data from the stations and a map with their location can be found here: https://en.ilmatieteenlaitos.fi/download-observations

I made all of this using Gemini 3.
