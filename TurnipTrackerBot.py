# Turniphead's Trunip tracker

import discord
import re
import datetime
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dataclasses import dataclass
import argparse

client = discord.Client()

directory = os.getcwd()
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    directory + "/client_secret.json", scope
)
gclient = gspread.authorize(creds)
list_of_turnip_prices = []
sheet = gclient.open("Turniphead's Turnip Tracker").sheet1


@dataclass
class TurnipPrice:
    """Class for keeping track of a turnip price."""

    message: discord.Message
    channel: discord.TextChannel
    author: str
    string: str
    price: int
    period: str
    date: str
    user: str
    flags: list

    def __init__(self, message):
        self.message = message
        self.channel = message.channel
        self.author = message.author.name
        self.string = message.content.lower()
        self.price = extract_price(self.string)
        self.period = extract_period(self.string)
        self.date = extract_date(self.string)
        self.user = message.author.name

    def make_row(self):
        return [str(self.user), str(self.price), str(self.period), str(self.date)]


# helper method using regex to extract the date from a given string. Date must
# have a '/' seperating month, date, and year
def extract_date(string):
    try:
        date = re.findall(r"\d+/\d+/\d+|\d+/\d+", string)[0]
        return date
    except:
        return datetime.date.today().strftime("%m/%d/%y")


def extract_price(string):
    try:
        price = re.findall(r"( \d+ | \d+$)", string)[0]
        return int(price)
    except:
        return None


def extract_period(string):
    if " am " in string or " am" in string:
        return "AM"
    elif " pm " in string or " pm" in string:
        return "PM"
    else:
        return datetime.datetime.today().strftime(
            "%p"
        )  # if the user doesn't specify assume the current period


# This method is triggered when we log in.
@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


# Trigger this method every time there is a message posted in the server
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$turnip"):
        message.content = message.content.lower().replace("$turnip", "")
        await parse_message(message)


# First of a few helper methods to parse messages posted in the server
async def parse_message(message):
    message_str = message.content.lower()
    t = TurnipPrice(message)
    args = parse_args(message_str.split(" "))
    if "help" in message_str:
        await t.channel.send(
            "Thanks for asking! Please submit turnip requests using the"
            "following format: `$turnip [price] [AM/PM]"
            "[OPTIONAL Date: MM/DD/YY]`"
        )
    elif args.status or args.suh_dude:
        await t.channel.send(
            "Ready and waiting for your Turnip prices, {}!!".format(t.author)
        )
    elif args.delete:
        await delete_entry(t)
    elif args.debug:
        global sheet
        sheet = gclient.open("Turniphead's Turnip Tracker").worksheet("debug")
        await t.channel.send("Sheet set to debug sheet.")
    elif args.master:
        sheet = gclient.open("Turniphead's Turnip Tracker").sheet1
        await t.channel.send("Sheet set to sheet1.")
    elif args.user:
        t.user = args.user
        await save_data(t)
    else:
        await save_data(t)
        return t


# After parsing the message use this helper method to save the data to the
# dictionary which lives in memory and the google sheet
async def save_data_local(turnip_price: TurnipPrice):
    list_of_turnip_prices.append(turnip_price)


async def save_data(t: TurnipPrice):
    if t.price == None:
        break
    await save_data_local(t)
    await save_data_google_sheets(t)
    if t.user != t.author:
        await t.channel.send(
            f"Thanks, {t.author}! Your turnip price has been saved as user\
            {t.user}! \n**Price** : {t.price} \t**Period**: {t.period}\
            \t**Date**: {t.date}"
        )
    else:
        await t.channel.send(
            f"Thanks, {t.author}! Your turnip price has been saved!\
            \n**Price** : {t.price} \t**Period**: {t.period}\
            \t**Date**: {t.date}"
        )
    await react_to_complete_message(t.message)
    return t


def parse_args(message_string):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "price", default=0, nargs="*", help="the price of the turnips as"
    )
    parser.add_argument(
        "--user",
        action="store",
        help="allow turnip prices to be added as a different user",
    )
    parser.add_argument(
        "--log", action="store_true", help="show all the prices entered for a user",
    )
    parser.add_argument(
        "--edit", action="store_true", help="allow user to edit an entry"
    )
    parser.add_argument(
        "--delete", action="store_true", help="allow user to delete an entry"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="set the sheet to the debug\
        sheet",
    )
    parser.add_argument(
        "--master",
        action="store_true",
        help="set the sheet to the master\
        sheet",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="display a status message to the\
        user",
    )
    parser.add_argument(
        "--suh_dude",
        action="store_true",
        help="display a status message to the\
        user",
    )
    return parser.parse_args(message_string)


# Inserts the data into the 2nd row of the sheet, pushes all other rows
# down as a result
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
    print(turnip.user, turnip.price, turnip.period, turnip.date)
    for row in all_values:
        print(row)
        if (
            row[0] == turnip.user
            and row[1] == str(turnip.price)
            and row[2] == turnip.period
            and row[3] == str(turnip.date)
        ):
            print("Found row to match value")


def make_greeting():
    pass


# Remind users to buy Turnips on Sunday
@client.event
async def sunday_reminder(message):
    if datetime.date.day == "Sunday":
        await message.channel.send(
            "@here Good Morning Turnip fans, get out there and buy some\
            Turnips!"
        )


# After we have saved the data given in a user's message, react to it to
# provide feedback
@client.event
async def react_to_complete_message(message):
    emoji = "\N{White Heavy Check Mark}"
    await message.add_reaction(emoji)


async def remind_sunday():
    if datetime.date.today().weekday() == 6:
        await client.wait_until_ready()
        channel = discord.Object(id="animal_crossing")
        await channel.send("@here Wake up and buy some Turnips fam!!!")


if __name__ == "__main__":
    File_object = open(r"bot_secret.txt", "r")
    bot_key = File_object.read()
    client.loop.create_task(remind_sunday())
    client.run(bot_key)
