import unittest
import subprocess
import ast
import os

from alternatecmds.screenscrapes import getusers
from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import get_users


class testgetusers(TwitchEnvVars):
    def test_getusers(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        self.assertTrue(hasattr(self, 'twitch_broadcaster_name'))
        
        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['login'] = [self.twitch_broadcaster_name]

        python_api_results = get_users(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'getusers.sh'], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #get data from screen scraping
        screenscrape_results = getusers.get_users_info_from_twitch_page(self.twitch_broadcaster_name)

        self.assertTrue(len(python_api_results) == len(curl_results))

        #python and curl results should match exactly
        for ind, item in enumerate(python_api_results):
            self.assertTrue(item in curl_results)

            #All I could find to scrape was the profile image.  
            #view count, offline image, and description didn't seem to be on the page
            self.assertTrue(item['profile_image_url'] == screenscrape_results[ind])
