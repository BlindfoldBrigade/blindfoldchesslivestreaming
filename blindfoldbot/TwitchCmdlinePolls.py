from __future__ import print_function
import os
import sys 
import configparser
import argparse

from TwitchPollWrappers import hundredint, hundredlist, datetime_rfc3339, twitchmanifestid
import TwitchPollCommands

config = None
parser = None


TWITCH_SECTION = 'Twitch'
BROADCAST_CHANNEL_NAME = 'broadcast_channel_name'
BROADCAST_CLIENT_ID = 'broadcast_client_id'
BROADCAST_OAUTH = 'broadcast_oauth'

class TwitchConfig:
    broadcast_channel_name = None
    broadcast_client_id = None
    broadcast_oauth = None

    def __init__(self, config):
        self.broadcast_channel_name = config.get(TWITCH_SECTION, BROADCAST_CHANNEL_NAME)
        self.broadcast_client_id = config.get(TWITCH_SECTION, BROADCAST_CLIENT_ID)
        self.broadcast_oauth = config.get(TWITCH_SECTION, BROADCAST_OAUTH)
   
    def __str__(self):
        retstring = 'broadcast channel name: ' + self.broadcast_channel_name + '\n'
        retstring += 'broadcast client id: ' + self.broadcast_client_id + '\n'
        retstring += 'broadcast oauth: ' + self.broadcast_oauth + '\n'

        return retstring


twitch_config = None

def generate_default_config(config_filename):
    config = ConfigParser.ConfigParser()
    config.add_section(TWITCH_SECTION)
    config.set(TWITCH_SECTION, BROADCAST_CHANNEL_NAME, '<channel name goes here>')
    config.set(TWITCH_SECTION, BROADCAST_CLIENT_ID, '<broadcast client id goes here>')
    config.set(TWITCH_SECTION, BROADCAST_OAUTH, '<broadcast oauth goes here>')
   
    with open(config_filename, 'wb') as configfile:
        config.write(configfile)


def setup_argument_parsers(progname):
    parser = argparse.ArgumentParser(description='common parameters for all commands', add_help=False)
    parser.add_argument('-c', '--config', help="Config file with data to use to either fully or partially run the command.  You don't need to specify this if you're manually setting all values with command line arguments.", required=False)
    parser.add_argument('-a', '--oauth', help='Twitch broadcaster oauth.  If unspecified it needs to be present in the specified config file.', required=True)
    parser.add_argument('-i', '--clientid', help='Twitch client id.  If unspecified it needs to be present in the specified config file.', required=True)

    #parsers that use after/first cursoring
    afterfirstparser = argparse.ArgumentParser(description='commands that use after/first cursoring', add_help=False)
    afterfirstparser.add_argument('--after', required=False, help='cursor for forward pagination. Tells the server where to start fetching the next set of results.  Matches pagination response field from a prior query.')
    afterfirstparser.add_argument('--first', type=hundredint, required=False, help='maximum number of objects to return.  Maximum 100, default 20', default=20)

    #parsers that use after/first cursoring and also a before cursor
    alsobeforeparser = argparse.ArgumentParser(description='commands that use after/first/before cursoring', parents=[afterfirstparser], add_help=False)
    alsobeforeparser.add_argument('--before', required=False, help='cursor for backward pagination. Tells the server where to start fetching the next set of results.  Matches pagination response field from a prior query.')

    #parsers that optionally specify language
    languageparser = argparse.ArgumentParser(description='commands that use language', add_help=False)
    languageparser.add_argument('--language', required=False, help='language, up to 100 values', type=hundredlist)

    OPTIONAL_CAVEAT="Remember that 'Optional Arguments' means what the options are.  See syntax above for which ones are required"

    #parser for get bits leaderboard
    argparser_bits = argparse.ArgumentParser(prog=progname + ' get_bits_leaderboard', description='get bits leaderboard information for the specified channel. ' + OPTIONAL_CAVEAT, parents=[parser])
    argparser_bits.add_argument('--count', type=hundredint, required=False, help='Number of results to be returned.  Maximum 100, default 10', default=10)
    argparser_bits.add_argument('--period', required=False, help='Time period over which data is aggregated.  Options day, week, month, year, all', choices=['day', 'week', 'month', 'year', 'all'], default='all')
    argparser_bits.add_argument('--started_at', type=datetime_rfc3339, required=False, help="start of time period.  Python's dateutil.parser used to translate the string.")
    argparser_bits.add_argument('--user_id', required=False, help='ID of the user whose results are returned')
    command_functions['get_bits_leaderboard'].append(argparser_bits)

    #parser for create clip
    argparser_createclip = argparse.ArgumentParser(prog=progname + ' create_clip', description='get a clip edit url for a particular video. ' + OPTIONAL_CAVEAT, parents=[parser])
    argparser_createclip.add_argument('--broadcasterid', required=True, help='Twitch broadcaster name associated with the command.')
    argparser_createclip.add_argument('--has_delay', type=bool, default=False, required=False, help='True if delay should be added before the clip is captured.  Default False.')
    command_functions['create_clip'].append(argparser_createclip)

    #parser for get clips
    argparser_getclips = argparse.ArgumentParser(prog=progname + ' get_clips', description='get clips for a particular video. ' + OPTIONAL_CAVEAT, parents=[parser, alsobeforeparser])
    id_to_use_group = argparser_getclips.add_mutually_exclusive_group(required=True)    
    id_to_use_group.add_argument('--id', help='id of a single clip to return')
    id_to_use_group.add_argument('--broadcasterid', help='Twitch broadcaster name associated with the command.')
    id_to_use_group.add_argument('--gameid', help='Game ID for which clips are returned.')
    command_functions['get_clips'].append(argparser_getclips)

    #parser for create entitlement upload URL
    argparser_grants = argparse.ArgumentParser(prog=progname + ' create_entitlement_grants_upload_URL', description='get a url to upload an entitlement grant to. ' + OPTIONAL_CAVEAT, parents=[parser])
    argparser_grants.add_argument('--manifestid', type=twitchmanifestid, help='unique identifier of the manifest file, string length 1-64')
    argparser_grants.add_argument('--type', help='type of entitlement being granted, must be bulk_drops_grant', choices=['bulk_drops_grant'])
    command_functions['create_entitlement_grants_upload_URL'].append(argparser_grants)

    #parser for get games
    argparser_getgames = argparse.ArgumentParser(prog=progname + ' get_games', description='get specified game information. ' + OPTIONAL_CAVEAT, parents=[parser])

        ###ONE OR MORE OF OPTIONS BELOW, CAN DO BOTH
    argparser_getgames.add_argument('--id', type=hundredlist, help='game id, at most 100 values')
    argparser_getgames.add_argument('--name', type=hundredlist, help='game name, at most 100 values')        
        ###ONE OR MORE OF OPTIONS ABOVE, CAN DO BOTH
    command_functions['get_games'].append(argparser_getgames)
    
    #parser for get game analytics
    argparser_analytics = argparse.ArgumentParser(prog=progname + ' get_game_analytics', description='get analytics for a particular game. ' + OPTIONAL_CAVEAT, parents=[parser])
    argparser_analytics.add_argument('--gameid', help='game id to get analytics for.  If not specified, response returns multiple URLs', required=False)
    command_functions['get_game_analytics'].append(argparser_analytics)

    #parser for get top games
    argparser_topgames = argparse.ArgumentParser(prog=progname + ' get_top_games', description='get information on the top games. ' + OPTIONAL_CAVEAT, parents=[parser, alsobeforeparser])
    command_functions['get_top_games'].append(argparser_topgames) 

    #parser for get streams
    argparser_streams = argparse.ArgumentParser(prog=progname + ' get_streams', description='get streams matching particular criteria. ' + OPTIONAL_CAVEAT, parents=[parser, alsobeforeparser, languageparser])
    argparser_streams.add_argument('--communityid', type=hundredlist, required=False, help='returns streams in a specific community id, up to 100 values')
    argparser_streams.add_argument('--gameid', type=hundredlist, required=False, help='returns streams for a specific game id, up to 100 values')
    argparser_streams.add_argument('--userid', type=hundredlist, required=False, help='return streams broadcast by one or more of the specified IDs, up to 100 values')
    argparser_streams.add_argument('--userlogin', type=hundredlist, required=False, help='return streams broadcast by one or more of the specified logins, up to 100 values')
    command_functions['get_streams'].append(argparser_streams)

    #parser for get streams metadata
    argparser_streams_metadata = argparse.ArgumentParser(prog=progname + ' get_streams_metadata', description='get stream metadata, specific to hearthstone or overwatch. ' + OPTIONAL_CAVEAT, parents=[parser, alsobeforeparser, languageparser])
    argparser_streams_metadata.add_argument('--communityid', type=hundredlist, required=False, help='returns streams in a specific community id, up to 100 values')
    argparser_streams_metadata.add_argument('--gameid', type=hundredlist, required=False, help='returns streams for a specific game id, up to 100 values')
    argparser_streams_metadata.add_argument('--userid', type=hundredlist, required=False, help='return streams broadcast by one or more of the specified IDs, up to 100 values')
    argparser_streams_metadata.add_argument('--userlogin', type=hundredlist, required=False, help='return streams broadcast by one or more of the specified logins, up to 100 values')
    command_functions['get_streams_metadata'].append(argparser_streams_metadata)

    #parser for get users
    argparser_users = argparse.ArgumentParser(prog=progname + ' get_users', description='get users matching criteria. ' + OPTIONAL_CAVEAT, parents=[parser])
    argparser_users.add_argument('--id', required=False, type=hundredlist, help='id(s) to retrieve, up to 100 values')
    argparser_users.add_argument('--login', required=False, type=hundredlist, help='user login name(s), up to 100 values')
    command_functions['get_users'].append(argparser_users)

    #parser for get users follows
    argparser_userfollows = argparse.ArgumentParser(prog=progname + ' get_users_follows', description='get who a user follows, or who is following a user. ' + OPTIONAL_CAVEAT, parents=[parser, afterfirstparser])
    to_or_from_group = argparser_userfollows.add_mutually_exclusive_group(required=True)
    to_or_from_group.add_argument('--fromid', help='user id, users who are being followed by fromid')
    to_or_from_group.add_argument('--toid', help='user id, which users are following toid')
    command_functions['get_users_follows'].append(argparser_userfollows)

    #parser for update user
    argparser_updateuser = argparse.ArgumentParser(prog=progname + ' update_user', description='update the description for a user. ' + OPTIONAL_CAVEAT, parents=[parser])
    argparser_updateuser.add_argument('--description', required=True, help='new description for the user')    
    command_functions['update_user'].append(argparser_updateuser)

    #parser for get videos
    argparser_getvideos = argparse.ArgumentParser(prog=progname + ' get_videos', description='Get videos for a channel. ' + OPTIONAL_CAVEAT, parents=[parser, alsobeforeparser, languageparser])
    id_group = argparser_getvideos.add_mutually_exclusive_group(required=True)
    id_group.add_argument('--id', type=hundredlist, help='get videos from id(s), limit 100')
    id_group.add_argument('--userid', help='get videos from userid')
    id_group.add_argument('--gameid', help='get videos from gameid')
    argparser_getvideos.add_argument('--period', required=False, help='period during which the video was created.  Options all, day, week, month.  Default all.', choices=['all', 'day', 'week', 'month'], default='all')
    argparser_getvideos.add_argument('--sort', required=False, help='sort order of the videos.  Options time, trending, views.  Default time.', choices=['time', 'trending', 'views'], default='time')
    argparser_getvideos.add_argument('--type', required=False, help='type of video.  Options all, upload, archive, highlight.  Default all.', choices=['all', 'upload', 'archive', 'highlight'], default='all')
    command_functions['get_videos'].append(argparser_getvideos)

    return parser

command_functions = {
    'get_bits_leaderboard' : [TwitchPollCommands.get_bits_leaderboard],
    'create_clip' : [TwitchPollCommands.create_clip],
    'get_clips' : [TwitchPollCommands.get_clips],
    'create_entitlement_grants_upload_URL' : [TwitchPollCommands.create_entitlement_grants_upload_URL],
    'get_games' : [TwitchPollCommands.get_games],
    'get_game_analytics' : [TwitchPollCommands.get_game_analytics],
    'get_top_games' : [TwitchPollCommands.get_top_games],
    'get_streams' : [TwitchPollCommands.get_streams],
    'get_streams_metadata' : [TwitchPollCommands.get_streams_metadata],
    'get_users' : [TwitchPollCommands.get_users],
    'get_users_follows' : [TwitchPollCommands.get_users_follows],
    'update_user' : [TwitchPollCommands.update_user],
    'get_videos' : [TwitchPollCommands.get_videos],
}

def print_known_commands():
    print('known commands are: ')
    for key in command_functions:
        print('\t' + key)

#this is used to allow another python program to use this functionality without having to do a command shell execution
#def twitch_command_programmatic():

if __name__ == "__main__":
    parser = setup_argument_parsers(sys.argv[0])
    if len(sys.argv) < 2:
        print_known_commands()
        sys.exit()

#    parsed_arguments = parser.parse_args(sys.argv[1:])

    command_name = sys.argv[1]

    if not command_name in command_functions.keys():
        print(command_name + ' is not a known command.\n')
        print_known_commands()
        sys.exit()

    args = command_functions[command_name][1].parse_args(sys.argv[2:])
    print(command_functions[command_name][0](**vars(args)))


#    print(command_functions[command_name][0](command_functions[command_name][1], sys.argv))

#    config_filename = sys.argv[2]

#    config = ConfigParser.ConfigParser()

#    parsed_list = config.read(config_filename)

#    if len(parsed_list) > 0:
#        twitch_config = TwitchConfig(config)
#    else:
        #generate a new default values config file
#        print("No config file found for ", config_filename, ", generating default config in that file")
#        generate_default_config(config_filename)


