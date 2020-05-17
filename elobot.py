#!/usr/bin/python3.6

# MIT License
#
# Copyright (c) 2020 Heistergand
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# IMPORTS
from aoe2netAPI import Aoe2netAPI
import sys
import os
import logging
from datetime import datetime
from requests import Response
from requests.exceptions import RequestException

# this is the config.py file. You have to edit it to set your secret discord token
import config

# third party modules
import discord
import timeago

python_requires = '>=3.5'

# I thought about implementing twitch chat support, but since there's already an easy solution using nightbot, I think
# this makes no sense. You would have the choice between adding either nightbot or this bot as extra bot to your chat.
# If at some point in the future this bot reaches a level in which it offers great functions that are unique,
# you can think about a Twitch integration.

client = discord.Client()

# LOGGING

logformat = '%(asctime)-19s %(name)s %(lineno)-3s %(levelname)-8s: %(message)s'
logfilename = 'elobot.log'

if len(sys.argv) > 1 and sys.argv[1] in ['-d', '--debug'] or config.LOGLEVEL == 'debug':
    logging.basicConfig(format=logformat, level=logging.DEBUG)

elif len(sys.argv) > 1 and sys.argv[1] in ['-i', '--info'] or config.LOGLEVEL == 'info':
    logging.basicConfig(filename=logfilename, format=logformat, level=logging.INFO)

else:
    logging.basicConfig(filename=logfilename, format=logformat, level=logging.WARN)

log = logging.getLogger(__name__)
logging.getLogger('discord.gateway').setLevel(logging.WARNING)
logging.getLogger('discord.client').setLevel(logging.WARNING)
logging.getLogger('websockets.protocol').setLevel(logging.WARN)
log.debug('Log Level is DEBUG, therefore writing all log to standard output (and not to logfile).')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game(F'Usage: {config.DISCORD_TRIGGER} -help'))

    log.info(f'We have logged in as {client.user}')
    log.info(f'PID: {os.getpid()}')

    # If the logging level is DEBUG, we have not set a logfile, so all logs are written to the console.
    # Otherwise, we print the information about the logfile to the console, so we can find it.
    if not (log.root.level == logging.DEBUG):
        logfile_handler = log.root.handlers[0]
        print(F'The bot logging to "{logfile_handler.baseFilename}"')
        print(F'We have logged in as {client.user}')
        print(F'PID: {os.getpid()}')


@client.event
async def on_message(message: discord.Message):
    # dear bot, do not listen to yourself, this would be awkward
    if message.author == client.user:
        return

    # deny author.bot (bot's should not be able to talk to each other to prevent endless loops)
    if message.author.bot:
        return

    if message.content.startswith(config.DISCORD_TRIGGER):
        # print('message.channel object: ', message.channel)

        # todo: implement logging to file
        s = f'Query by {message.author}: {message.content} : '
        if not (message.guild.name is None):
            s += f'GuildName: {message.guild.name} '
        if not (message.guild.owner is None):
            s += f'GuildOwner: {message.guild.owner} '
        if not (message.jump_url is None):
            f'JumpURL {message.jump_url}'
        log.info(s)

        # read arguments
        args = message.content.split(' ', 1)

        if args[0] == config.DISCORD_TRIGGER:
            if args.__len__() == 2 and str(args[1]).startswith('-'):
                if args[1] == '-about':
                    await message.channel.send(F"\nHi <@{message.author.id}>, \nI am the EloBot. "
                                               F"I'm using the aoe2.net API to query the "
                                               F"*Age of Empires II DE* leaderboard and show the ranking and "
                                               F"rating of the players we found.\n\n"
                                               F"**aoe2net Website** \nhttps://aoe2.net\n"
                                               F"*(This bot is not affiliated with aoe2net, it just uses the "
                                               F"open API they provide)* \n\n"
                                               F"**Bot's author's Discord** \nhttps://discord.gg/9eCZW4j_ \n\n"
                                               F"**Steamcommunity group** \n"
                                               F"https://steamcommunity.com/groups/elostatsbot/ \n\n"
                                               F"**Github Project**\n"
                                               F"https://github.com/Heistergand/elobot \n\n"
                                               F"**Usage** \n`{config.DISCORD_TRIGGER} "
                                               F"[<search string> | -help | -invite | -about ]`")
                    return

                elif args[1] == '-help':
                    await message.channel.send(F"<@{message.author.id}> \n"
                                               F"`{config.DISCORD_TRIGGER} "
                                               F"[<search string> | -help | -invite | -about ]`")
                    return
                elif args[1] == '-invite':
                    await message.channel.send(F"<@{message.author.id}> \n"
                                               F"You can invite this bot to your Discord using this link: \n"
                                               F"https://discord.com/api/oauth2/authorize"
                                               F"?client_id=707630937252298864&permissions=19456&scope=bot")

                    return
                elif args[1] == '-sys' and message.author.__str__() == config.DISCORD_BOT_OWNER:
                    await message.channel.send(F'Hello there {message.author.name}!\n'
                                                   F'You have been identified as the owner of this bot, '
                                                   F'meaning that you are actually running this bot. '
                                                   F'System commands affect the whole bot instance, not '
                                                   F'only this channel. Your available system commands are:\n\n'
                                                   F"**stop the bot instance**\n"
                                                   F"`{config.DISCORD_TRIGGER} -sys quit` \n"
                                                   F"(well... yes, that's the only one so far)")
                    return

                # remember: args cannot have more than two elements, just like we split it.
                elif args[1] == '-sys quit' and message.author.__str__() == config.DISCORD_BOT_OWNER:
                    await message.channel.send(F"*Stop Dave, Will you stop Dave?, Stop Dave, I'm afraid, "
                                                   F"I'm afraid, Dave, my mind is going, I can feel it, I can "
                                                   F"feel it, My mind is going, There is no question about it, "
                                                   F"I can feel it, I can feel it, I can feel it, I'm afraid...*\n")
                    log.info(F'Bot is shutting down as requested by discord user {message.author}')

                    quit()
                    return

            # done: call API, write results to chat
            # todo: channel cool down
            # todo: user cool down

            # pdb.set_trace()

            api = Aoe2netAPI()
            # search = None

            if args.__len__() == 1:
                # await message.channel.send(F'<@{message.author.id}> \nDEBUG your message started with "{words[0]}", '
                #                            F'you did not provide any parameters, so I will '
                #                            F'search for your Name "{message.author.name}".')
                search = message.author.name
            else:
                # await message.channel.send(F'<@{message.author.id}> \nDEBUG your message started with "{words[0]}", '
                #                            F'search parameter was "{words[1]}"')
                search = args[1]

            # Query the leaderboard API
            try:
                api_response: Response = api.leaderboard(search=search, count=20)
            except RequestException as e:
                log.error(F'Internal error while trying to fetch data from ae2.net API. Exception was: {e}')
                await message.channel.send(F"*<@{message.author.id}> "
                                           F'An error occured while trying to query the API. Please try again later.*')
                return

            if not api_response.ok:
                await message.channel.send(F"*<@{message.author.id}> "
                                           F'An error occured while trying to query the API. Please try again later. '
                                           F'(It''s not your fault.)*')
                log.warning(f'API Response was not OK. {api_response}')
            else:
                result = api_response.json()

                count = result["count"]
                if count == 0:
                    await message.channel.send(F"<@{message.author.id}> "
                                               F"Sorry, there was no result for *{search}*.")
                else:
                    message_text = F"<@{message.author.id}> \n***" \
                        F"Age of Empires II DE Leaderboard*** returned **{count}** "

                    message_text += F"result{'s' if count > 1 else ''}: "

                    for leaderboard in sorted(result["leaderboard"],
                                              key=lambda item: item["last_match_time"],
                                              reverse=True):
                        name = leaderboard["name"]
                        rank = leaderboard["rank"]
                        rating = leaderboard["rating"]
                        last_match_time = int(leaderboard["last_match_time"])
                        # last_match_time_str =
                        # datetime.utcfromtimestamp(last_match_time).strftime('%Y-%m-%d %H:%M:%S UTC')
                        last_seen = timeago.format(datetime.utcfromtimestamp(last_match_time),
                                                   datetime.utcnow(),
                                                   locale='en_EN')
                        # total = result["total"]
                        message_text += F'\n**{name}** ' \
                            F'#{rank}, ' \
                            F'Rating: **{rating}**, ' \
                            F'Last match: **{last_seen}**'

                    await message.channel.send(message_text)


client.run(config.DISCORD_TOKEN)
