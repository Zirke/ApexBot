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


def query_api(name):
    try:
        data = json_from_tracker(name)
    except ValueError:
        print("Invalid json")
    except KeyError:
        print('\n' + data['errors'][0]['message'])
    return data


def receive_legends(name):
    data = query_api(name)
    legendlist = []
    for i in range(0, len(data['data']['children'][0]['id'])):
        legendlist.append(i)
    return legendlist


print(receive_legends('Dritix'))
s1 = Stat("Kills", 434, 42342)

leg1 = Legend("Mirage", s1)
