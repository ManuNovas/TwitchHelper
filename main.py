import json
import requests
import sys
import datetime
from slugify import slugify

filePath = "./"
type = sys.argv[1]
if type == "--rpg":
    filePath += "rpg-games.json"
elif type == "--adventure":
    filePath += "adventure-games.json"
elif type == "--goty":
    filePath += "goty-games.json"
else:
    filePath += "casual-games.json"
    url = "https://api.twitch.tv/helix/games/top"
    header = {
        "Client-Id": "suqpiw18pur0nrcd5f3c2yihhcadsf",
        "Authorization": "Bearer 5dczso8pjxxj1crqheccqohir13vpo"
    }
    response = requests.get(url, headers = header)
    file = open(filePath, "w+")
    file.write('{"games":[')
    data = response.json()["data"]
    dataLength = len(data)
    i = 1
    i = 1
    for d in data:
        line = '{"slug":"' + slugify(d["name"]) + '","categoryID":"' + d["id"] + '"}'
        if i < dataLength:
            line += ','
        file.write(line)
        i += 1
    weekday = int(datetime.datetime.today().weekday())
    if weekday == 7:
        weekday = 0
    hour = datetime.datetime.now().hour
    print(weekday)
    file.write('],"daysOfWeek": [4, 5, 6], "hoursOfDay": [22, 23]}')
    file.close()
file = open(filePath)
json = json.load(file)
file.close()
games = json["games"]
url = 'https://gql.twitch.tv/gql'
daysOfWeek = json["daysOfWeek"]
hoursOfDay = json["hoursOfDay"]
research = []
for game in games:
    request = [
       {
          "operationName": "Directory_DirectoryBanner",
          "variables": {
             "slug": game["slug"]
          },
          "extensions": {
             "persistedQuery": {
                "version": 1,
                "sha256Hash": "822ecf40c2a77568d2b223fd5bc4dfdc9c863f081dd1ca7611803a5330e88277"
             }
          }
       },
       {
          "operationName": "getHourlyViewersHeatmapQuery",
          "variables": {
             "input": {
                "channelID": "533973826",
                "categoryID": game["categoryID"],
                "timeZoneOffset": -6,
                "languageTag": "es",
                "region": "ANY",
                "daysAggregated": 28,
                "includesTopStreamers": False
             }
          },
          "extensions": {
             "persistedQuery": {
                "version": 1,
                "sha256Hash": "72e6e927c64e6ce67afe1cc35812a46c360dc93297996b938c725defeda3d0f3"
             }
          }
       }
    ]
    header = {
        "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
        "Authorization": "OAuth sv8z4otwhs98q3hw5spbcs81rg4n6w"
    }
    response = requests.post(url, json = request, headers = header)
    g = response.json()
    averageConcurrentUsers = 0
    count = 0
    for hourlyHeatMap in g[1]["data"]["hourlyViewers"]["hourlyHeatMap"]:
        if hourlyHeatMap["dayOfWeek"] in daysOfWeek and hourlyHeatMap["hourOfDay"] in hoursOfDay:
            averageConcurrentUsers += hourlyHeatMap["averageConcurrentUsers"]
            count += 1
    average = round(averageConcurrentUsers / count, 2)
    if g[0]["data"]["game"]:
        research.append({"game": g[0]["data"]["game"]["name"], "average": average})
research = sorted(research, key = lambda r: r["average"], reverse = True)
for r in research:
    print(r)
