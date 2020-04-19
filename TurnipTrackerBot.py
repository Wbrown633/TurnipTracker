# Turniphead's Trunip tracker

import discord
import re
import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()

results_dict = {}

# boilerplate code for gettign a connection to the spreadsheets
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
directory = os.getcwd()
creds = ServiceAccountCredentials.from_json_keyfile_name(directory + '\\client_secret.json', scope)
gclient = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = gclient.open("Turniphead's Turnip Tracker").sheet1

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$turnip'):
        await parse_message(message)

async def parse_message(message):
    message_str = message.content.lower()
    if 'help' in message_str:
        await message.channel.send('Thanks for asking! Please submit turnip requests using the following format: `$turnip [price] [AM/PM] [OPTIONAL Date: (MM/DD/YY)]`')
    elif 'am' in message_str:
        timezone = 'am'
        await save_data(timezone, message)
    elif 'pm' in message_str:
        timezone = 'pm'
        await save_data(timezone, message)

async def save_data(timezone, message, date=None):
    if date == None:
        date = datetime.date
    name = message.author.name
    if message.author.nick != None:
        display_name = message.author.nick
    else: 
        display_name = message.author.name
    price = re.findall(" \d+ ", message.content)
    print(message.content)
    date = extract_date(message.content)
    results_dict[name] = [int(price[0]), timezone, date[0]]
    await message.channel.send('Thanks {0}! Your turnip price has been saved!'.format(display_name))
    await react_to_complete_message(message)
    print(results_dict)

@client.event
async def react_to_complete_message(message):
    emoji = "\N{White Heavy Check Mark}"
    await message.add_reaction(emoji)

@client.event
async def check_previous_messages():
    pass

def extract_date(string):
    return re.findall(r'\(\d+/\d+/\d+\)|\(\d+/\d+\)',string)

if __name__ == "__main__":
    client.run('Njk5NzM4NjEwNjUxNjI3NjMy.XpYxuQ.l35XOhWVGqnkznMII2dCxS8sMnY')