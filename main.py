import asyncio
import random
import sys
from datetime import datetime, timedelta

import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from discord_slash.context import ComponentContext
from discord_slash.model import CallbackObject

from objects.Thread import send_reminder
from utilities.constants import DT_TASK_FORMAT
from utilities.constants import TEST_TOKEN, PROD_TOKEN
from utilities.constants import production_server
from utilities.constants import which_guild
from utilities.embed import build_embed
from utilities.mysql import Process_MySQL, sqlRetrieveTasks

client = Bot(
    command_prefix="$",
    case_insensitive=True,
    description="Bot Frost version 3.0! Now with Slash Commands",
    intents=discord.Intents.all()
)

slash = SlashCommand(client, sync_commands=True)  # Sync required


async def change_my_status():
    statuses = (
        "Husker football 24/7",
        "Nebraska beat Florida 62-24",
        "the Huskers give up 400 yards rushing to one guy",
        "a swing pass for -1 yards",
        "a missed field goal"
    )
    try:
        print("### Attempting to change status...")
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=random.choice(statuses)
            )
        )
        print(f"### ~~~ Successfully changed status")
    except (AttributeError, discord.HTTPException) as err:
        print("### ~~~ Unable to change status: " + str(err).replace("\n", " "))
    except:
        print(f"### ~~~ Unknown error!", sys.exc_info()[0])


async def change_my_nickname():
    nicks = (
        "Bot Frost",
        "Mario Verbotzco",
        "Adrian Botinez",
        "Bot Devaney",
        "Mike Rilbot",
        "Robo Pelini",
        "Devine Ozigbot",
        "Mo Botty",
        "Bot Moos",
        "Bot Diaco",
        "Rahmir Botson",
        "I.M. Bott",
        "Linux Phillips",
        "Dicaprio Bottle",
        "Bryce Botheart",
        "Jobot Chamberlain",
        "Bot Bando",
        "Shawn Botson",
        "Zavier Botts",
        "Jimari Botler",
        "Bot Gunnerson",
        "Nash Botmacher",
        "Botger Craig",
        "Dave RAMington",
        "MarLAN Lucky",
        "Rex Bothead",
        "Nbotukong Suh",
        "Grant Bostrom",
        "Ameer Botdullah",
        "Botinic Raiola",
        "Vince Ferraboto",
        "economybot",
        "NotaBot_Human",
        "psybot",
        "2020: the year of the bot",
        "bottech129",
        "deerebot129"
    )

    try:
        print("### Attempting to change nickname...")
        await client.user.edit(
            username=random.choice(nicks)
        )
        print(f"### ~~~ Successfully changed display name")
    except discord.HTTPException as err:
        err_msg = "### ~~~ Unable to change display name: " + str(err).replace("\n", " ")
        print(err_msg)
    except:
        print(f"### ~~~ Unknown error!", sys.exc_info()[0])


async def load_tasks():
    tasks = Process_MySQL(sqlRetrieveTasks, fetch="all")
    guild = client.get_guild(which_guild())

    if tasks is None:
        return

    def convert_duration(value: str):
        imported_datetime = datetime.strptime(value, DT_TASK_FORMAT)
        now = datetime.now()

        if imported_datetime > now:
            duration = imported_datetime - now
            return duration
        return timedelta(seconds=0)

    async def convert_destination(destination_id: int):
        destination_id = int(destination_id)
        try:
            member = guild.get_member(destination_id)
            if member is not None:
                return member
        except:
            pass

        try:
            channel = guild.get_channel(destination_id)
            if channel is not None:
                return channel
        except:
            pass

        return None

    if tasks is None:
        return print("### ;;; No tasks were loaded")

    print(f"### ;;; There are {len(tasks)} to be loaded")

    task_repo = []

    for task in tasks:
        send_when = convert_duration(task["send_when"])
        member_or_chan = await convert_destination(task["send_to"])

        if member_or_chan is None:
            print(f"### ;;; Skipping task because [{member_or_chan}] is None.")
            continue

        if task["author"] is None:
            task["author"] = "N/A"

        if send_when == timedelta(seconds=0):
            print(f"### ;;; Alert time already passed! {task['send_when']}")
            await send_reminder(
                thread_name=None,
                num_seconds=0,
                destination=member_or_chan,
                message=task["message"],
                source=task["author"],
                alert_when=task["send_when"]
            )
            continue

        task_repo.append(
            asyncio.create_task(
                send_reminder(
                    thread_name=str(member_or_chan.id + send_when.total_seconds()),
                    num_seconds=send_when.total_seconds(),
                    destination=member_or_chan,
                    message=task["message"],
                    source=task["author"],
                    alert_when=task["send_when"]
                )
            )
        )

    for index, task in enumerate(task_repo):
        await task


@client.event
async def on_ready():
    await change_my_status()
    await change_my_nickname()
    await load_tasks()

    print(
        f"### Bot Frost version 3.0 ###\n"
        f"### ~~~ Name: {client.user}\n"
        f"### ~~~ ID: {client.user.id}\n"
        f"### The bot is ready! ###"
    )


@client.event
async def on_slash_command_error(ctx, ex):
    embed = build_embed(
        title="Slash Command Error",
        fields=[
            ["Description", ex]
        ]
    )
    await ctx.send(embed=embed, hidden=True)


@client.event
async def on_component(ctx: ComponentContext):
    """ Called when a component is triggered. """
    pass


@client.event
async def on_component_callback(ctx: ComponentContext, callback: CallbackObject):
    pass


token = None

if len(sys.argv) > 0:
    if production_server():
        token = PROD_TOKEN
    else:
        token = TEST_TOKEN

extensions = [
    "commands.croot_bot",
    "commands.admin",
    "commands.text",
    "commands.image",
    "commands.football_stats",
    "commands.reminder",
    "commands.testing"
]
for extension in extensions:
    print(f"### ~~~ Loading extension: {extension} ###")
    client.load_extension(extension)

client.run(token)
