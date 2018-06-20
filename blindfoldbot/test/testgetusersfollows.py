import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import getusersfollows
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_users_follows, get_users
from blindfoldutilities.mappings import user_id_from_name

class testgetusersfollows(TwitchEnvVars):
    def test_getusersfollows(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        self.assertTrue(hasattr(self, 'twitch_broadcaster_id'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['to_id'] = [self.twitch_broadcaster_id]
        args['first'] = 100

        python_api_results = get_users_follows(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'gethundredfollowerstest.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = getusersfollows.get_users_follows_info_from_twitch_page(self.twitch_broadcaster_name)

        self.assertTrue(len(python_api_results) == len(curl_results) == len(screenscrape_results))

        #python and curl results should match exactly
        for ind, item in enumerate(python_api_results):
            self.assertTrue(item in curl_results)
            self.assertTrue(item['from_id'] == user_id_from_name(self.twitch_client_id, self.twitch_bearer, screenscrape_results[ind]))

