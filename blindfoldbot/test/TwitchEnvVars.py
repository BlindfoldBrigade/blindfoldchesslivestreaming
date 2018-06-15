import unittest
import os

class TwitchEnvVars(unittest.TestCase):
    bashcmddir = 'alternatecmds/bashcurl/'

    def setUp(self):
        #These four are from environment variables instead of config because 
        #the curl tests expect them to be, and it's also nice not to reference
        #any files for them because they're sensitive anyway.
        if 'TWITCH_BEARER' in os.environ.keys():
            self.twitch_bearer = os.environ['TWITCH_BEARER']

        if 'TWITCH_CLIENT_ID' in os.environ.keys():
            self.twitch_client_id = os.environ['TWITCH_CLIENT_ID']

        if 'TWITCH_BROADCASTER_NAME' in os.environ.keys():
            self.twitch_broadcaster_name = os.environ['TWITCH_BROADCASTER_NAME']

        if 'TWITCH_BROADCASTER_ID' in os.environ.keys():
            self.twitch_broadcaster_id = os.environ['TWITCH_BROADCASTER_ID']


