import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import getclips
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_clips


class testgetclips(TwitchEnvVars):
    def test_getclips(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        self.assertTrue(hasattr(self, 'twitch_broadcaster_id'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['broadcaster_id'] = self.twitch_broadcaster_id

        python_api_results = get_clips(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'getclips.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = getclips.get_clips_info_from_twitch_page(self.twitch_broadcaster_name)

        #all three results should match
#        print(type(python_api_results))
#        print(type(curl_results))
#        print(type(screenscrape_results))
        self.assertTrue(python_api_results == curl_results == screenscrape_results)
