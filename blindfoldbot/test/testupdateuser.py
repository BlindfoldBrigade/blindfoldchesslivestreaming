import unittest
import subprocess
import ast
import os

import datetime

from test.TwitchEnvVars import TwitchEnvVars
from TwitchPollCommands import update_user


class testupdateuser(TwitchEnvVars):
    def test_updateuser(self):
        #this test needs client id, and bearer
        self.assertTrue(hasattr(self, 'twitch_client_id'))
        self.assertTrue(hasattr(self, 'twitch_bearer'))
        
        currtimestr = str(datetime.datetime.now()).replace(' ', '')

        #get data from API call via python
        args = {}
        args['clientid'] = self.twitch_client_id
        args['oauth'] = self.twitch_bearer
        args['description'] = currtimestr

        python_api_results = update_user(**args)['data']

        #get data from API call with curl
        completion_info = subprocess.run([TwitchEnvVars.bashcmddir + 'updateuser.sh', currtimestr], stdout=subprocess.PIPE)

        results_dict = ast.literal_eval(completion_info.stdout.decode('utf-8'))
        curl_results = results_dict['data']

        #I don't know how to screenscrape this info so no screenscrape test right now

        #python and curl results should match exactly
        for ind, item in enumerate(python_api_results):
            self.assertTrue(curl_results[ind] == item)
