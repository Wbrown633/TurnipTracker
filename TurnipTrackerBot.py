# Turniphead's Trunip tracker

import discord
import re
import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dataclasses import dataclass

client = discord.Client()

directory = os.getcwd()
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(directory + '\\client_secret.json', scope)
gclient = gspread.authorize(creds)
list_of_turnip_prices = []
sheet = gclient.open("Turniphead's Turnip Tracker").sheet1

@dataclass
class TurnipPrice:
    '''Class for keeping track of a turnip price.'''
    price: int
    period: str
    date: str
    
    def __init__(self, message):
        self.message = message
        self.string = message.content.lower()
        self.price = self.extract_price()
        self.period = self.extract_period()
        self.date = self.extract_date()
        self.user = message.author.name
        self.flags = self.extract_flags()
    
    # helper method using regex to extract the date from a given string. Date must have a '/' seperating month, date, and year
    def extract_date(self):
        try:
            date = re.findall(r'\d+/\d+/\d+|\d+/\d+', self.string)[0]
            return date
        except:
            return datetime.date.today().strftime("%m/%d/%y")
    
    def extract_price(self):
        try:
            price = re.findall(r'([^\/]\d+[^\/])', self.string)[0]
            return price
        except:
            raise ValueError("Malformed command string")
    
    def extract_period(self):
        if "am" in self.string:
            return "AM"
        elif "pm" in self.string:
            return "PM"
        else:
            return datetime.datetime.today().strftime("%p") # if the user doesn't specify assume the current period

    def extract_flags(self):
        return re.findall(r'--\w+', self.string)
            
    def make_row(self):
        return [str(self.user), str(self.price), str(self.period), str(self.date)]

# This method is triggered when we log in. 
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# Trigger this method every time there is a message posted in the server
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$turnip'):
        await parse_message(message)

# First of a few helper methods to parse messages posted in the server
async def parse_message(message):
    message_str = message.content.lower()
    if 'help' in message_str:
        await message.channel.send('Thanks for asking! Please submit turnip requests using the following format: `$turnip [price] [AM/PM] [OPTIONAL Date: MM/DD/YY]`')
    else:
        t = TurnipPrice(message)
        if "--delete" in t.flags:
            delete_entry(t)
        await save_data_local(t)
        await save_data_google_sheets(t)
        await message.channel.send('Thanks, {}! Your turnip price has been saved! \n**Price** : {} \t**Period**: {} \t**Date**: {}'.format(message.author.name, t.price, t.period, t.date))
        await react_to_complete_message(message)

# After parsing the message use this helper method to save the data to the dictionary which lives in memory and the google sheet
async def save_data_local(turnip_price: TurnipPrice):
    list_of_turnip_prices.append(turnip_price)

# Inserts the data into the 2nd row of the sheet, pushes all other rows down as a result
async def save_data_google_sheets(turnip_price: TurnipPrice):
    open_row = 2
    row = turnip_price.make_row()
    sheet.insert_row(row, open_row)

# Still to be implemented
async def edit_entry(turnip: TurnipPrice):
    # find matching row in sheet
    # edit values
    # raise error if we can't find a match
    find_entry(turnip)

# Still to be implemented
async def delete_entry(turnip: TurnipPrice):
    # find matching row in sheet
    # delete row
    # raise error if we can't find a match
    find_entry(turnip)

def find_entry(turnip: TurnipPrice):
    all_values = sheet.get_all_values()
    for row in all_values:
        if(row[0] == turnip.user and row[1] == turnip.price and row[2] == turnip.period and row[3] == turnip.date):
            print("Found row to match value")


# After we have saved the data given in a user's message, react to it to provide feedback
@client.event
async def react_to_complete_message(message):
    emoji = "\N{White Heavy Check Mark}"
    await message.add_reaction(emoji)

if __name__ == "__main__":
    File_object = open(r"bot_secret.txt","r")
    bot_key = File_object.read()
    client.run(bot_key)