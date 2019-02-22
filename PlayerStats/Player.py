import requests
import json

from PlayerStats.Legend import Legend
from PlayerStats.Stat import Stat

__all__ = ['Legend', 'Stat']


class Player:
    def __init__(self, playerName, listOfLegends):
        self.playerName = playerName
        self.listOfLegends = listOfLegends


def json_from_tracker(name):
    url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/' + name
    headers = {'TRN-Api-Key': '8b3b6e28-122f-4d9a-8c54-794fca417953'}
    # headers = {'TRN-Api-Key': '1c757697-3ea1-484e-ae03-14790cd3c356'}
    r = requests.get(url, headers=headers)
    return r.json()


def query_api_data(name):
    try:
        data = json_from_tracker(name)
    except ValueError:
        print("Invalid json")
    except KeyError:
        print('\n' + data['errors'][0]['message'])
    return data


def query_legend_id(name):
    data = query_api_data(name)
    legendIdList = []
    for i in range(0, len(data['data']['children'])):
        legendIdList.append(data['data']['children'][i]['id'])
    return legendIdList


def query_legend_stats(data, playerLegendList):
    for i in playerLegendList:
        if data['data']['children'][0]['id'] == i:
            #print(json.dumps(data, indent=4))
            if data['data']['children'][0]['stats'][0]['metadata']['key'] == 'Kills':
                output = data['data']['children'][0]['stats'][0]['metadata']['value']
                #print(json.dumps(data, indent=4))
                print(output)



def initialize_legends(legendIDs):
    legendlist = []
    stat = 0
    for lid in legendIDs:
        if lid == 'legend_1':
            wraith = Legend("Wraith", stat)
            legendlist.append(wraith)
        elif lid == 'legend_2':
            bangalore = Legend("Bangalore", stat)
            legendlist.append(bangalore)
        elif lid == 'legend_3':
            caustic = Legend("Caustic", stat)
            legendlist.append(caustic)
        elif lid == 'legend_4':
            mirage = Legend("Mirage", stat)
            legendlist.append(mirage)
        elif lid == 'legend_5':
            bloodhound = Legend("Bloodhound", stat)
            legendlist.append(bloodhound)
        elif lid == 'legend_6':
            gibraltar = Legend("Gibraltar", stat)
            legendlist.append(gibraltar)
        elif lid == 'legend_7':
            lifeline = Legend("Lifeline", stat)
            legendlist.append(lifeline)
        elif lid == 'legend_8':
            pathfinder = Legend("pathfinder", stat)
            legendlist.append(pathfinder)
    return legendlist


# print(json.dumps(query_api_data('Dritix'), indent=4))


print(query_legend_stats(query_api_data('Dritix'), query_legend_id('Dritix')))
# print(initialize_legends(query_legend_id('Dritix')))
