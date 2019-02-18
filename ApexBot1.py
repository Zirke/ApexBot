#!python3.6
import re
import asyncio
import json
import requests
import discord
import sched
import time
from discord.ext import commands

TOKEN = 'MzI1MjY5OTMwNDUyNzEzNDgy.D0r9VA.EyQTiWXoQJQ-yzt11tu0OxTPGCI'

client = commands.Bot(command_prefix = '.')

def inf_from_tracker(name):
	url = 'https://public-api.tracker.gg/apex/v1/standard/profile/5/'+name
	headers = {'TRN-Api-Key': '8b3b6e28-122f-4d9a-8c54-794fca417953'}
	r = requests.get(url, headers=headers)
	return r.text

@client.event
async def on_ready():
	print('Bot online')

@client.command()
async def update(*args):
	errorMsg = None
	lst=[]
	if len(args) is not 2:
		for word in args:
			name = word
		if not name:
			name = 'Dritix'
		stat = 'kills'
	else:
		for word in args:
			lst.append(word)
		name = lst[0]
		if lst[1] == 'kills' or lst[1] == 'Kills':
			statMsg = 'kills'
			stat = 'kills'
		elif lst[1] == 'wins' or lst[1] == 'Wins':
			statMsg = 'wins'
			stat = 'winsWithFullSquad'
		elif lst[1] == 'damage' or lst[1] == 'Damage':
			statMsg = 'damage'
			stat = 'damage'
		else:
			stat = 'kills'
			errorMsg = 'Syntax error: only kills, wins or damage is supported'

	value = []
	legend = 0
	legentlst = []
	output = ""

	try:
		data = json.loads(inf_from_tracker(name))
	except ValueError:
		print ("invalid json")
	else:
		for i in range(0, len(data)):
			if 'value' in data[i][stat]:
				value.append(data[i][stat]['value'])
			if 'legend' in data[i]:
				if 'value' in data[i][stat]:
					legend = data[i]['legend']
					if legend == 1:
						legentlst.append("Wraith")
					elif legend == 2:
						legentlst.append("Bangalore")
					elif legend == 3:
						legentlst.append("Caustic")
					elif legend == 4:
						legentlst.append("Mirage")
					elif legend == 5:
						legentlst.append("Bloodhound")
					elif legend == 6:
						legentlst.append("Gibraltar")
					elif legend == 7:
						legentlst.append("Lifeline")
					elif legend == 8:        
						legentlst.append("Pathfinder")
	if len(args) is not 2: 
		output = 'Could not understand, but '+name+' has '+str(value)+' kills! (Use syntax .update name kills/wins/damage)'
	elif errorMsg is not None:
		output = errorMsg + ', but '+name+' has '+str(value)+' kills! (Use syntax .update name kills/wins/damage)'
	else:
		output = name + " has got a total of:\n"
		for v, l, in zip(value, legentlst):
			output += (str(v) + ' ' + statMsg + ' with ' + str(l) + '\n')
		#output = name+' has got a total of : '+str(value)+ ' ' + statMsg + ' with ' + ' and '.join(legentlst)
	await client.say(output)



def broadcastWins(name):
	value = 0
	try:
		data = json.loads(inf_from_tracker(name))
	except ValueError:
		print ("invalid json")
	else:
		for i in range(0, len(data)):
			if 'value' in data[i]['winsWithFullSquad']:
				#if value < data[i]['kills']['value']:
				value += data[i]['winsWithFullSquad']['value']
	return int(value)

async def background_task_wins(name):
	wins = {}
	newWins = {}
	await client.wait_until_ready()
	channel = discord.Object(id='325296935667761152')
	wins[name] = broadcastWins(name)
	while not client.is_closed:
		newWins[name] = broadcastWins(name)
		if newWins[name] > wins[name]:
			output = name+' has just won '+str(newWins[name]-wins[name])+' game(s)!'
			wins[name] = newWins[name]
			await client.send_message(channel, output)
		await asyncio.sleep(5)

#for name in broadcastNames:
	#client.loop.create_task(background_task_wins(name))

client.run(TOKEN)