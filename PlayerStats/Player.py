from PlayerStats import Stat

import requests

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


# Returns full json object from API
def query_api_data(name):
    try:
        data = json_from_tracker(name)
    except ValueError:
        print("Invalid json")
    except KeyError:
        print('\n' + data['errors'][0]['message'])
    return data


# Returns a list of all tracked legends (ID) from Player
def query_legend_id(name):
    data = query_api_data(name)
    legendIdList = []
    for i in range(0, len(data['data']['children'])):
        legendIdList.append(data['data']['children'][i]['id'])
    return legendIdList


# Returns the list of Stat objects for requested Legend
def query_legend_stats(data, legendname):
    children = []
    statlist = []

    # Makes a list of all 'children' directories from Json object
    for x in data['data']['children']:
        children.append(x)

    # Iterates through specified 'child' directory and creates Stat object from information
    for x in range(0, len(children)):
        if children[x]['metadata']['legend_name'] == legendname:
            for y in range(0, len(children[x]['stats'])):
                statname = children[x]['stats'][y]['metadata']['key']
                value = children[x]['stats'][y]['value']
                rank = children[x]['stats'][y]['rank']

                temp = Stat(legendname, statname, value, rank)
                statlist.append(temp)
    return statlist


def initialize_legends(inputIDs):
    legendlist = []

    for foo in inputIDs:
        if foo == "legend_1":
            wraith = Legend("Wraith", query_legend_stats(query_api_data("TopZirke"), "Wraith"))
            legendlist.append(wraith)
        elif foo == "legend_2":
            bangalore = Legend("Bangalore", query_legend_stats(query_api_data("TopZirke"), "Bangalore"))
            legendlist.append(bangalore)
        elif foo == "legend_3":
            caustic = Legend("Caustic", query_legend_stats(query_api_data("TopZirke"), "Caustic"))
            legendlist.append(caustic)
        elif foo == "legend_4":
            mirage = Legend("Mirage", query_legend_stats(query_api_data("TopZirke"), "Mirage"))
            legendlist.append(mirage)
        elif foo == "legend_5":
            bloodhound = Legend("Bloodhound", query_legend_stats(query_api_data("TopZirke"), "Bloodhound"))
            legendlist.append(bloodhound)
        elif foo == "legend_6":
            gibraltar = Legend("Gibraltar", query_legend_stats(query_api_data("TopZirke"), "Gibraltar"))
            legendlist.append(gibraltar)
        elif foo == "legend_7":
            lifeline = Legend("Lifeline", query_legend_stats(query_api_data("TopZirke"), "Lifeline"))
            legendlist.append(lifeline)
        elif foo == "legend_8":
            pathfinder = Legend("Pathfinder", query_legend_stats(query_api_data("TopZirke"), "Pathfinder"))
            legendlist.append(pathfinder)
    return legendlist




# print(query_legend_id('TopZirke'))
# print(initialize_legends(query_legend_id('TopZirke')))
# print(json.dumps(query_api_data('TopZirke'), indent=4))
# print(query_legend_stats(query_api_data("TopZirke"), "Caustic"))
# print(initialize_legends(query_legend_id('TopZirke')))
