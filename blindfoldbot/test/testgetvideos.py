import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import getvideos
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_videos

def scrapematches(item, scrape):
    return item['title'] == scrape[0] and item['url'] == scrape[1]

class testgetvideos(TwitchEnvVars):
    def test_getvideos(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        self.assertTrue(hasattr(self, 'twitch_broadcaster_id'))
        self.assertTrue(hasattr(self, 'twitch_broadcaster_name'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['user_id'] = self.twitch_broadcaster_id
        args['first'] = 20

        python_api_results = get_videos(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'getvideos.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = getvideos.get_videos_info_from_twitch_page(self.twitch_broadcaster_name)
        if len(screenscrape_results) > 20:
            screenscrape_results = screenscrape_results[:20]

        self.assertTrue(len(python_api_results) == len(curl_results) == len(screenscrape_results))

        #python and curl results should match exactly
        for ind, item in enumerate(python_api_results):
            self.assertTrue(curl_results[ind] == item)
            self.assertTrue(scrapematches(item, screenscrape_results[ind]))
