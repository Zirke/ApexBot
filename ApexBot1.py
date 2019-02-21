#!python3.6
import re
import asyncio
from bs4 import BeautifulSoup
import json
import requests
import discord
import sched
import time
from discord.ext import commands

TOKEN = 'MzI1MjY5OTMwNDUyNzEzNDgy.D0r9VA.EyQTiWXoQJQ-yzt11tu0OxTPGCI'

client = commands.Bot(command_prefix = '.')

async def inf_from_tracker():
	url = 'https://apex.tracker.gg/profile/pc/'+name
	page = requests.get(url).content
	soup = BeautifulSoup(page, "html.parser")
	pattern = re.compile(r"var imp_careerStats = \[([^]]+)\]")
	script = str(soup.find("script", text=pattern))
	s = re.match(r"[^[]*\[([^]]*)\]", script).groups()[0]
	s = "[" + s + "]"
	return str(s)

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
		data = json.loads(inf_from_tracker())
	except ValueError:
		print ("invalid json")
	else:
		for i in range(0, len(data)):
			if 'value' in data[i][stat]:
				value.append(data[i][stat]['value'])
			if 'legend' in data[i]:
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

async def dritixWins():
	value = 0
	url = 'https://apex.tracker.gg/profile/pc/Dritix'
	page = requests.get(url).content
	soup = BeautifulSoup(page, "html.parser")
	pattern = re.compile(r"var imp_careerStats = \[([^]]+)\]")
	script = str(soup.find("script", text=pattern))
	s = re.match(r"[^[]*\[([^]]*)\]", script).groups()[0]
	s = "[" + s + "]"

	try:
		data = json.loads(s)
	except ValueError:
		print ("invalid json")
	else:
		for i in range(0, len(data)):
			if 'value' in data[i]['winsWithFullSquad']:
				#if value < data[i]['kills']['value']:
				value += data[i]['winsWithFullSquad']['value']
	return int(value)

client.run(TOKEN)