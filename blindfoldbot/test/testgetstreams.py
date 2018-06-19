import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import getstreams
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_streams

def scrapematches(item, scrape):
    return item['title'] == scrape[0] and scrape[1].lower() in item['thumbnail_url'].lower()

class testgetstreams(TwitchEnvVars):
    def test_getstreams(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['community_id'] = '4912794f-4830-470f-8224-a2f793d4e5b6'

        python_api_results = get_streams(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'get_live_lichess_streams.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = getstreams.get_streams_info_from_twitch_page('lichess')
        self.assertTrue(len(python_api_results) == len(curl_results) == len(screenscrape_results))

        #python and curl results should match exactly
        for ind, item in enumerate(python_api_results):
            self.assertTrue(curl_results[ind] == item)
            self.assertTrue(scrapematches(item, screenscrape_results[ind]))
