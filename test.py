#!python3.6
import asyncio
import json
import requests
import discord
from discord.ext import commands


def inf_from_tracker(name):
    url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/' + name
    headers = {'TRN-Api-Key': '8b3b6e28-122f-4d9a-8c54-794fca417953'}
    # headers = {'TRN-Api-Key': '1c757697-3ea1-484e-ae03-14790cd3c356'}
    r = requests.get(url, headers=headers)
    #print(r.text)
    return r.json()


def query_api(name, stat):
    value = 0
    output = ''
    try:
        data = inf_from_tracker(name)
    except ValueError:
        print("Invalid json")
    else:
        try:
            # for i in range(0, len(data)):
            # if 'value' in data['data']['children']['stats']:
            for i in range(0, len(data['data']['children'][0]['stats'])):
                if data['data']['children'][0]['stats'][i]['metadata']['key'] == 'Kills':
                    print(data['data']['children'][0]['stats'][i]['value'])
            output = name + 'has got a total of : ' + str(value) + ' ' + stat + '!'
        except KeyError:
            print('\n'+data['errors'][0]['message'])
    return output


print(query_api('dritix', 'kills'))
