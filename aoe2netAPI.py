# aoe2netAPI.py

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

# Project Website:
# https://github.com/Heistergand/elobot

import requests
from requests import Response
import logging

logger = logging.getLogger(__name__)


class Aoe2netAPI(object):
    """
    Class Aoe2netAPI provides a python interface to the aoe2.net API

    Attributes
    ----------
    protocol : str
        The protocol part of the URL used to connect to the API (default 'https')
    host : str
        The hostname used to connect to the API (default 'aoe2.net')
    language : str
        Returns the language that is used as argument for the API (default 'en')
        This value can be overwritten when creating a new instance.
    endpoint :  str
        Returns the URL path which represents the API method of the last request
    query :  str
        Returns the URL parameters used in the last request
    URL : str
        The composed URL that was used in the last request

    Methods
    -------
    fetch(endpoint: str, query: str = None, protocol: str = protocol, host: str = host)
        Sends a get request to the eo2.net API and returns a Response object.
    """

    # instance variables
    protocol: str = 'https'
    host: str = 'aoe2.net'
    language: str = 'en'
    endpoint: str = None
    query: str = None
    URL: str = None

    def __init__(self, language: str = language) -> None:
        self.language = language

    def fetch(self, endpoint: str, query: str = None, protocol: str = protocol,
              host: str = host) -> Response:
        """
        Sends a get request to the eo2.net API and returns a Response object.

        *This internal method is the base method that is used by all other endpoint methods.
        Although it can be used alone, it is originally meant to be used internally by this
        classes endpoint methods.*

        Parameters
        ----------

        :param endpoint:
            the path to the API method

        :param query:
            the query parameters as string (default is None)

        :param protocol:
            the protocol used to create the URL (default is 'https')

        :param host:
            the host used to create the URL (default is 'aoe2.net)
            Note that the port is set dynamically. If you need to set a custom port, attach it to the host name.

        :returns:
            A Response object containing the http response from the API.

        """

        # overwrite the class attributes to custom values provided by the method's arguments
        self.endpoint = endpoint
        self.query = query
        self.protocol = protocol
        self.host = host

        # concatenate arguments to URL and save as attribute
        self.URL = f'{protocol}://{host}{endpoint}{query}'

        logger.debug(f'Fetching from API: {self.URL}')
        ret = requests.get(self.URL)
        logger.debug(f'Returning from API: {ret} {ret.content}')
        return ret

    def strings(self, game: str, language: str = language) -> Response:
        """Request a list of strings used by the API.

        **Endpoint**
            /api/strings

        Request Parameters
        ------------------
        :param game:
            (Required) Game (Age of Empires 2:HD=aoe2hd, Age of Empires 2:Definitive Edition=aoe2de)
        :param language:
            (Optional, defaults to en) Language (en, de, el, es, es-MX, fr, hi, it, ja, ko, ms, nl, pt, ru, tr, vi, zh, zh-TW)
        :returns:
            A Response object containing the http response from the API.
        """

        endpoint = '/api/strings'
        query = f'?game={game}&language={language}'
        return self.fetch(endpoint, query)

    def leaderboard(self, game: str = 'aoe2de', leaderboard_id: int = 3, start: int = 1, count: int = 1,
                    search: str = None, steam_id: int = None, profile_id: str = None) -> Response:
        """Request the current leaderboards

        **Endpoint**
            /api/leaderboard

        Leaderboard IDs
        ---------------
        0 = Unranked \n
        1 = 1v1 Deathmatch \n
        2 = Team Deathmatch \n
        3 = 1v1 Random Map \n
        4 = Team Random Map

        Request Parameters
        ------------------
        :param game: Game (Age of Empires 2:Definitive Edition=aoe2de)
        :param leaderboard_id: Leaderboard ID
        :param start: Starting rank (Ignored if search, steam_id, or profile_id are defined)
        :param count: Number of leaderboard entries to get (Must be 10000 or less))
        :param search: Name Search
        :param steam_id: steamID64 (ex: 76561199003184910)
        :param profile_id: Profile ID (ex: 459658)
        :return: A Response object containing the http response from the API.
        """

        endpoint = '/api/leaderboard'
        query = f'?game={game}&leaderboard_id={leaderboard_id}&start={start}&count={count}'

        if not (search is None):
            query += f'&search={search}'
        if not (steam_id is None):
            query += f'&steam_id={steam_id}'
        if not (profile_id is None):
            query += f'&profile_id={profile_id}'

        return self.fetch(endpoint, query)

    def lobbies(self, game: str = None) -> Response:
        """Request all open lobbies

        **Endpoint**
            /api/lobbies

        Request Parameters
        ------------------
        :param game:
                    (Required) Game (Age of Empires 2:Definitive Edition=aoe2de)
        :return: A Response object containing the http response from the API.
        """

        endpoint = '/api/lobbies'
        if not (game is None):
            query = f'?game={game}'
        else:
            query = None

        return self.fetch(endpoint, query)

    def lastmatch(self, game: str = 'aoe2de', steam_id: int = None, profile_id: str = None) -> Response:
        """
        Request the last match the player started playing.
        This will be the current match if they are still in game.

        **Endpoint**
            /api/lastmatch

        Request Parameters
        ------------------

        Either steam_id or profile_id is required!

        :param game: Game (Age of Empires 2:Definitive Edition=aoe2de)
        :param steam_id: steamID64 (ex: 76561199003184910)
        :param profile_id: Profile ID (ex: 459658)
        :returns: A Response object containing the http response from the API.
        """

        endpoint = '/api/lastmatch'
        query = f'?game={game}&steam_id={steam_id}&profile_id={profile_id}'
        return self.fetch(endpoint, query)

    def matches(self, game: str = 'aoe2de', start: int = 0, count: int = 1,
                steam_id: int = None, profile_id: str = None) -> Response:
        """Request the match history for a player.

        **Endpoint**
            /api/matches

        Request Parameters
        ------------------
        :param game: Game (Age of Empires 2:Definitive Edition=aoe2de)
        :param start: Starting match (0 is the most recent match)
        :param count: Number of matches to get (Must be 1000 or less))
        :param steam_id: steamID64
        :param profile_id: Profile ID
        :returns: A Response object containing the http response from the API.
        """

        endpoint = '/api/matches'
        query = f'?game={game}&start={start}&count={count}'

        if not (steam_id is None):
            query += f'&steam_id={steam_id}'
        if not (profile_id is None):
            query += f'&profile_id={profile_id}'

        return self.fetch(endpoint, query)

    def ratinghistory(self, game: str = 'aoe2de', leaderboard_id: int = 3, start: int = 0, count: int = 1,
                      steam_id: int = None, profile_id: str = None) -> Response:
        """Request the rating history for a player

        **Endpoint**
            /api/ratinghistory

        Leaderboard IDs
        ---------------
        0 = Unranked \n
        1 = 1v1 Deathmatch \n
        2 = Team Deathmatch \n
        3 = 1v1 Random Map \n
        4 = Team Random Map

        Request Parameters
        ------------------
        :param game: Game (Age of Empires 2:Definitive Edition=aoe2de)
        :param leaderboard_id: Leaderboard ID
        :param start: Starting match (0 is the most recent match)
        :param count: Number of matches to get (Must be 1000 or less))
        :param steam_id: steamID64
        :param profile_id: Profile ID
        :returns: A Response object containing the http response from the API.
        """

        endpoint = '/api/ratinghistory'
        query = f'?game={game}&leaderboard_id={leaderboard_id}&start={start}&count={count}'

        if not (steam_id is None):
            query += f'&steam_id={steam_id}'
        if not (profile_id is None):
            query += f'&profile_id={profile_id}'

        return self.fetch(endpoint, query)

    def players(self, game: str) -> Response:
        """Number of Players Online

        **Endpoint**
            /api/stats/players

        Request Parameters
        ------------------
        :param game: Game (Age of Empires 2:HD=aoe2hd, Age of Empires 2:Definitive Edition=aoe2de)
        :returns: A Response object containing the http response from the API.
        """

        endpoint = '/api/players'
        query = f'?game={game}'
        return self.fetch(endpoint, query)
