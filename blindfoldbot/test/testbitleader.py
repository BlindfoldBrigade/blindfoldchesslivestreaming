import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import bitsinfo
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_bits_leaderboard


class testbitleader(TwitchEnvVars):
    def test_bitleader(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['count'] = 2
        args['period'] = 'week'
        python_api_results = get_bits_leaderboard(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'bitleadertest.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = bitsinfo.get_bitleader_info_from_twitch_page(self.twitch_broadcaster_name)

        #all three results should match
        self.assertTrue(python_api_results == curl_results == screenscrape_results)
