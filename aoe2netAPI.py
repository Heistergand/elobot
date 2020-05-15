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

import requests
from requests import Response
import logging

logger = logging.getLogger(__name__)

class Aoe2netAPI(object):
    # instance variables
    __defaultProtocol__: str = 'https'
    __defaultHost__: str = 'aoe2.net'
    __defaultLanguage__: str = 'en'
    protocol: str = __defaultProtocol__
    host: str = __defaultHost__
    language: str = __defaultLanguage__
    endpoint: str
    query: str
    request: str

    def __init__(self, language: str = __defaultLanguage__) -> None:
        self.language = language

    def fetch(self, endpoint: str, query: str = None, protocol: str = __defaultProtocol__,
              host: str = __defaultHost__) -> Response:
        self.endpoint = endpoint
        self.query = query
        self.protocol = protocol
        self.host = host
        self.request = f'{protocol}://{host}{endpoint}{query}'
        logger.debug(f'Fetching from API: {self.request}')
        ret = requests.get(self.request)
        logger.debug(f'Returning from API: {ret} {ret.content}')
        return ret

    def strings(self, game: str, language: str = language) -> Response:
        endpoint = '/api/strings'
        query = f'?game={game}&language={language}'
        return self.fetch(endpoint, query)

    def leaderboard(self, game: str = 'aoe2de', leaderboard_id: int = 3, start: int = 1, count: int = 1,
                    search: str = None, steam_id: int = None, profile_id: str = None) -> Response:
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
        endpoint = '/api/lobbies'
        if not (game is None):
            query = f'?game={game}'
        else:
            query = None

        return self.fetch(endpoint, query)

    def lastmatch(self, game: str = 'aoe2de', steam_id: int = None, profile_id: str = None) -> Response:
        endpoint = '/api/lastmatch'
        query = f'?game={game}&steam_id={steam_id}&profile_id={profile_id}'
        return self.fetch(endpoint, query)

    def matches(self, game: str = 'aoe2de', start: int = 1, count: int = 1,
                steam_id: int = None, profile_id: str = None) -> Response:

        endpoint = '/api/matches'
        query = f'?game={game}&start={start}&count={count}'

        if not (steam_id is None):
            query += f'&steam_id={steam_id}'
        if not (profile_id is None):
            query += f'&profile_id={profile_id}'

        return self.fetch(endpoint, query)

    def ratinghistory(self, game: str = 'aoe2de', leaderboard_id: int = 3, start: int = 1, count: int = 1,
                      steam_id: int = None, profile_id: str = None) -> Response:
        endpoint = '/api/ratinghistory'
        query = f'?game={game}&leaderboard_id={leaderboard_id}&start={start}&count={count}'

        if not (steam_id is None):
            query += f'&steam_id={steam_id}'
        if not (profile_id is None):
            query += f'&profile_id={profile_id}'

        return self.fetch(endpoint, query)

    def players(self, game: str) -> Response:
        endpoint = '/api/players'
        query = f'?game={game}'
        return self.fetch(endpoint, query)
