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
import discord
from aoe2netAPI import Aoe2netAPI
import sys
import logging
# import pdb
import config

from requests import Response

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
    log.info(f'We have logged in as {client.user}')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    # author.bot verhindern

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

            if args.__len__() == 2:
                if args[1] == '-about':
                    await message.channel.send(F"Hi, <@{message.author.id}>, I am the EloBot. "
                                               F"I'm using the aoe2.net API to query the "
                                               F"*Age of Empires II DE* leaderboard.\n\n"
                                               F"**aoe2net Website** https://aoe2.net "
                                               F"*(This bot is not affiliated with aoe2net, it just uses the "
                                               F"open API they provide)* \n"
                                               F"**Author's Discord:** https://discord.gg/9eCZW4j_ \n"
                                               F"**Steamcommunity group** "
                                               F"https://steamcommunity.com/groups/elostatsbot/announcements/ \n\n"
                                               F"**Usage:** \n`{config.DISCORD_TRIGGER} "
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
            leaderboard: Response = api.leaderboard(search=search)

            if not leaderboard.ok:
                await message.channel.send(F"<@{message.author.id}> "
                                           F'An error occured while trying to query the API. Please try again later. '
                                           F'**(It''s not your fault.)**')
                log.warning(f'API Response was not OK. {leaderboard}')
            else:
                result = leaderboard.json()

                # pdb.set_trace()
                if result["count"] == 1:
                    name = result["leaderboard"][0]["name"]
                    rank = result["leaderboard"][0]["rank"]
                    rating = result["leaderboard"][0]["rating"]
                    # total = result["total"]

                    await message.channel.send(F"<@{message.author.id}> \n"
                                               F'***Age of Empires II DE Leaderboard***\n'
                                               F'**Name:** {name}, '
                                               F'**Rank:** {rank}, '
                                               F'**Rating:** {rating}')
                else:
                    await message.channel.send(F"<@{message.author.id}> "
                                               F'Sorry, there was no result for *{search}*.')

client.run(config.DISCORD_TOKEN)







