import requests
import json
from collections import namedtuple

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


def query_legend_stats(data):
    children = []
    statlist = []

    for x in data['data']['children']:
        children.append(x)

    for x in range(0, len(children[0]['stats'])):
        for y in range(0, len(children[x]['stats'])):
            legendname = children[x]['metadata']['legend_name']
            statname = children[x]['stats'][y]['metadata']['key']
            value = children[x]['stats'][y]['value']
            rank = children[x]['stats'][y]['rank']
            temp = Stat(legendname, statname, value, rank)
            statlist.append(temp)
    return statlist


def initialize_legends(legendIDs, statlist):
    legendlist = []
    stats = []
    for lid in legendIDs:
        if lid == 'legend_1':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Wraith':
                    stats.append(stat)
            wraith = Legend("Wraith", stats)
            legendlist.append(wraith)
        elif lid == 'legend_2':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Bangalore':
                    stats.append(stat)
            bangalore = Legend("Bangalore", stats)
            legendlist.append(bangalore)
        elif lid == 'legend_3':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Caustic':
                    stats.append(stat)
            caustic = Legend("Caustic", stats)
            legendlist.append(caustic)
        elif lid == 'legend_4':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Mirage':
                    stats.append(stat)
            mirage = Legend("Mirage", stats)
            legendlist.append(mirage)
        elif lid == 'legend_5':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Bloodhound':
                    stats.append(stat)
            bloodhound = Legend("Bloodhound", stats)
            legendlist.append(bloodhound)
        elif lid == 'legend_6':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Gibraltar':
                    stats.append(stat)
            gibraltar = Legend("Gibraltar", stats)
            legendlist.append(gibraltar)
        elif lid == 'legend_7':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Lifeline':
                    stats.append(stat)
            lifeline = Legend("Lifeline", stats)
            legendlist.append(lifeline)
        elif lid == 'legend_8':
            del stats[:]
            for stat in statlist:
                if stat.legendName == 'Pathfinder':
                    stats.append(stat)
            pathfinder = Legend("pathfinder", stats)
            legendlist.append(pathfinder)
    return legendlist


print(initialize_legends(query_legend_id('Dritix'), query_legend_stats('Dritix')))

# print(json.dumps(query_api_data('Dritix'), indent=4))

# print(query_legend_stats(query_api_data('Dritix')))

#print(initialize_legends(query_legend_id('Dritix')), query_legend_stats(query_api_data('Dritix')))
