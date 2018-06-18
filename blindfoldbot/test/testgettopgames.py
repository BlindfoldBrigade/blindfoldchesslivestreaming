import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import gettopgames
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_top_games
from blindfoldutilities import twitchstrings

def scrapematches(nonscraper, scraper):
    return nonscraper['name'] == scraper[0] and twitchstrings.remove_img_dimensions(nonscraper['box_art_url']) == scraper[1]

class testgettopgames(TwitchEnvVars):
    def test_gettopgames(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer

        python_api_results = get_top_games(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'gettopgames.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = gettopgames.get_top_games_info_from_twitch_page()

        self.assertTrue(len(python_api_results) == len(curl_results))

        screenscrape_results = screenscrape_results[:len(python_api_results)]

        #python and curl results should match exactly, including ranking order
        for ind, item in enumerate(python_api_results):
            self.assertTrue(curl_results[ind] == item)
            self.assertTrue(scrapematches(item, screenscrape_results[ind]))
