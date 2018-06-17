import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import getgames
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_games


class testgetgames(TwitchEnvVars):
    def test_getgames(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['name'] = ['Chess', 'Hearthstone']

        python_api_results = get_games(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'getgames.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = [getgames.get_games_info_from_twitch_page('Chess'),getgames.get_games_info_from_twitch_page('Hearthstone')]

        self.assertTrue(len(python_api_results) == len(curl_results) == len(screenscrape_results))

        #python and curl results should match exactly
        for item in python_api_results:
            self.assertTrue(item in curl_results)
        
        #the screenscrape results lack id, but the name and boxart portions should match\
        for name, boxart in screenscrape_results:
            foundcurrent = False
            for item in python_api_results:
                if item['name'] == name:
                    self.assertTrue(item['box_art_url'] == boxart)
                    foundcurrent = True
                    break                    
                    
            self.assertTrue(foundcurrent)
