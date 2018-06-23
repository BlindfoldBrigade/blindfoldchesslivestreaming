from __future__ import print_function
import os
import sys 

import urllib.request
import urllib.parse

import collections

import ast

#def twitch_http_get(

#def twitch_http_put(

#def twitch_http_post(

##common header item : Authorization: Bearer <bearertoken>

COMMON_BASE_URL = "https://api.twitch.tv/helix/"

class MissingParameterError(Exception):
    def __init__(self, message):
        self.message = message

class ConflictingParameterError(Exception):
    def __init__(self, message):
        self.message = message


#the twitch approach to list handling is just to repeat in the 
#form param=val&param=val2&param=val3, etc
def listify_keywords(**kwargs):
    arglist = []

    for key in kwargs.keys():
        if isinstance(kwargs[key], str):
            #strings are iterable but don't break them up
            arglist.append([key, kwargs[key]])
        elif isinstance(kwargs[key], collections.Iterable):
            for item in kwargs[key]:
                arglist.append([key, item])
        elif not kwargs[key] == None:
            arglist.append([key, kwargs[key]])

    return arglist

def findvalue(key, seq):
    for keyy, val in seq:
        if keyy == key:
            return val

    return None

def twitchrequest(baseurl, reqargs, optargs, availableargs, methodd):
    args = []
    availablekeys = [key for key,value in availableargs]

    #required arguments
    for item in reqargs:
        if type(item) == list:
            #require one and only one of the list elements
            thingfound = ''
            for thing in item:
                if thing in availablekeys:
                    if not thingfound == '':
                        #more than one mutually exclusive parameter was passed
                        raise ConflictingParameterError(baseurl + ' was passed mutually exclusive parameters ' + thingfound + ' and ' + thing)
                    else:
                        thingfound = thing
                        args.extend([(key, val) for key, val in availableargs if key == thing])
        elif type(item) == tuple:
            #require at least one of the list elements (but more than one is ok too)
            thingfound = ''
            for thing in item:
                if thing in availablekeys:
                    thingfound = thing                    
                    args.extend([(key, val) for key, val in availableargs if key == thing])
            if thingfound == '':
                #needed something, found nothing
                raise MissingParameterError(baseurl + ' needed one or more of ' + str(item) + ' but was given none of them.')
        elif not item in availablekeys:
            raise MissingParameterError(baseurl + ' is missing ' + item + ' parameter.')
        else:
            args.extend([(key, val) for key, val in availableargs if key == item])

    #optional arguments
    for item in optargs:
        args.extend([(key, val) for key, val in availableargs if key == item])

    params = urllib.parse.urlencode(args)
    url = baseurl+'?%s'%params
    req = urllib.request.Request(url,method=methodd)

    #client id and oauth
    if not 'clientid' in availablekeys:
        raise MissingParameterError(baseurl + ' is missing clientid parameter.')
    req.add_header('Client-ID', findvalue('clientid', availableargs))

    if not 'oauth' in availablekeys:
        raise MissingParameterError(baseurl + ' is missing oauth parameter.')
    req.add_header('Authorization', 'Bearer ' + findvalue('oauth', availableargs))

    with urllib.request.urlopen(req) as f:
        results = f.read().decode('utf-8')

    #return results as a dict
    return ast.literal_eval(results)

def twitchget(baseurl, reqargs, optargs, availableargs):
    return twitchrequest(baseurl, reqargs, optargs, availableargs, 'GET')
        
def twitchput(baseurl, reqargs, optargs, availableargs):
    return twitchrequest(baseurl, reqargs, optargs, availableargs, 'PUT')

#Gets a ranked list of Bits leaderboard information for an authorized broadcaster
#Required Scope: bits:read
###specific params
## required
# None
## optional
# count(int) : number of results to be returned.  Maximum 100.  Default 10.
# period(str) : Time period over which data is aggregated. day,week,month,year,all
# started_at(str): timestamp for the period over which the returned data is aggregated.  Default current period.
# user_id(str): ID of the user whose results are returned. If not specified, returns top users.
###
###response fields
# ended_at(str) : end of the date range for returned data
# rank(int) : leaderboard rank of the user
# score(int) : number of bits of the user
# started_at(str) : start of the date range for returned data
# total(int) : total number of users returned
# user_id(str) : ID of the user in the leaderboard entry
###
#@twitchget(COMMON_BASE_URL+'bits/leaderboard', (), ('count', 'period', 'started_at', 'user_id'), **kwargs)
def get_bits_leaderboard(**kwargs):
    return twitchget(COMMON_BASE_URL+'bits/leaderboard', (), ('count', 'period', 'started_at', 'user_id'), listify_keywords(**kwargs))

#Creates a clip programmatically.  This returns both an ID and an edit URL for the new clip
#Required Scope: clips:edit
###specific params
## required
# broadcaster_id(str) : ID of the stream from which the clip will be made
## optional
# has_delay(bool) : if false clip from when API called, else add delay.  Default false
###
###response fields
# edit_url(str) : URL of the edit page for the clip
# id(str) : ID of the clip that was created
###
def create_clip(**kwargs):
    CREATE_CLIP_BASE_URL = COMMON_BASE_URL + 'clips'    
    return 'create_clip'

#Gets clip information by clip ID (one or more), broadcaster ID (one only), or game ID (one only).
#Required Scope: None
###specific params
## required
# broadcaster_id(str) : ID of the stream for whom clips are returned
# game_id(str) : ID of the game for which clips are returned.
# id(str) : ID of the clip being queried.  Limit 100.
## optional
# after(str) : forward cursor
# before(str) : backward cursor
# first(int) : maximum number of objects to return.  Limit 100, default 20
###
###response fields
# broadcaster_id(str) : user ID of the stream from which the clip was created
# created_at(str) : date when the clip was created.
# creator_id(str) : ID of the user who created the clip
# embed_url(str) : URL to embed the clip
# game_id(str) : ID of the game assigned to the stream when the clip was created.
# id(str) : ID of the clip being queried
# language(str) : Language of the stream from which the clip was created.
# pagination(str) : cursor value, used for subsequent requests to specify starting point
# thumbnail_url(str) : URL of the clip thumbnail
# title(str) : title of the clip
# url(str) : URL where the clip can be viewed.
# video_id(str) : ID of the video from which the clip was created
# view_count(int) : Number of times the clip has been viewed
###
def get_clips(**kwargs):
    return twitchget(COMMON_BASE_URL+'clips', (['broadcaster_id', 'game_id', 'id'],), ('after', 'before', 'first'), listify_keywords(**kwargs))

#Creates a URL where you can upload a manifest file and notify users that they have an entitlement.  See Drops Guide.
#Required Scope: Application access token
###specific params
## required
# manifest_id(str) : unique identifier of the manifest file to be uploaded.  1-64 characters
# type(str) : always "bulk_drops_grant"
## optional
# none
###
###response fields
# url(str) : the URL of the manifest file
###
def create_entitlement_grants_upload_URL(**kwargs):
    CREATE_ENTITLEMENT_GRANTS_UPLOAD_URL = COMMON_BASE_URL + 'entitlements/upload'
    return 'create_entitlement_grants_upload_URL'

#Gets game information by game ID or name.
#Required Scope: None
###specific params
## required
# id(str) : Game ID, at most 100 id values can be specified
#  AND/OR
# name(str) : Game name.  At most 100 name values can be specified
## optional
# None
###
###response fields
# box_art_url(object) : Template URL for the game's box art
# id(str) : Game ID
# name(str) : Game name
###
def get_games(**kwargs):
    return twitchget(COMMON_BASE_URL+'games', (('id', 'name'),), (), listify_keywords(**kwargs))

#Get a URL that game developers can use to download analytics for their games in a CSV format.  The URL is valid for 1 minute.  See Game Developer Analytics guide.
#Required Scope: analytics:read:games
###specific params
## required
# None
## optional
# game_id(str) : game ID.  Get analytics for this game.  If not specified includes separate reports for each of the authenticated user's games
###
###response fields
# game_id(str) : ID of the game whose analytics data is being provided
# URL(str) : URL to the downloadable CSV file containing analytics data.  Valid for 1 minute.
###
def get_game_analytics(**kwargs):
    GET_GAME_ANALYTICS_BASE_URL = COMMON_BASE_URL + 'analytics/games'
    return 'get_game_analytics'

#Gets games sorted by number of current viewers on Twitch, most popular first.
#Required Scope: None
###specific params
## required
# none
## optional
# after(str) : forward cursor
# before(str) : backward cursor
# first(int) : maximum number of objects to return.  Max 100, default 20
###
###response fields
# box_art_url(object) : Template URL for the game's box art
# id(str) : Game ID
# name(str) : Game name
# pagination(str) : cursor value, use as starting point for next set
###
def get_top_games(**kwargs):
    return twitchget(COMMON_BASE_URL+'games/top', (), ('after', 'before', 'first'), listify_keywords(**kwargs))

#Gets information about active streams.
#Required Scope: None
###specific params
## required
# None
## optional
# after(str) : forward cursor
# before(str) : backward cursor
# community_id(str) : returns streams in the specified community ID.  up to 100 IDs.
# first(int) : maximum number of objects to return.  Maximum 100, default 20
# game_id(str) : returns streams broadcasting a specific game ID.  up to 100 IDs.
# language(str) : stream language.  Up to 100
# user_id(str) : returns streams broadcast by one or more specified User IDs.  up to 100.
# user_login(str) : returns streams broadcast by one or more specfied user login names.  Up to 100.
###
###response fields
# community_ids(str) : array of community IDs
# game_id(str) : ID of the game being played on the stream
# id(str) : Stream ID
# language(str) : Stream language
# pagination(str) : cursor, used in a subsequent request to specify the starting point
# started_at(str) : UTC timestamp
# thumbnail_url(str) : Thumbnail URL of the stream.
# title(str) : stream title
# type(str) : "live" or "" if error
# user_id(str) : ID of the user who is streaming
# viewer_count(int) : number of viewers watching the stream at the time of the query.
###
def get_streams(**kwargs):
    return twitchget(COMMON_BASE_URL+'streams', (), ('after', 'before', 'community_id', 'first', 'game_id', 'language', 'user_id', 'user_login'), listify_keywords(**kwargs))

#Gets metadata about active streams playing Overwatch or Hearthstone.
# Someone who cares about Hearthstone and/or Overwatch can properly implement this function.
def get_streams_metadata(**kwargs):
    GET_STREAMS_METADATA_BASE_URL = COMMON_BASE_URL + 'streams/metadata'
    return "get_streams_metadata yawn"

#Gets information about one or more specified Twitch users.
#Required Scope: None
#Optional Scope (to get user email address) : user:read:email
###specific params
## required
# none
## optional
# id(str) : User ID , limit 100
# login(str) : User login name , limit 100
###
###response fields
# broadcaster_type(str) : User's broadcaster type.  options "partner", "affiliate", ""
# description(str) : User's channel description
# display_name(str) : User's display name
# email(str) : User's email address.  Requires user:read:email scope
# id(str) : User's ID
# login(str) : User's login name
# offline_image_url(str) : URL of the user's offline image
# profile_image_url(str) : URL of the user's profile image
# type(str) : User's type.  Options "staff", "admin", "global_mod", or ""
# view_count(int) : Total number of views of the user's channel.
###
def get_users(**kwargs):
    return twitchget(COMMON_BASE_URL+'users', (), ('id','login'), listify_keywords(**kwargs))

#Gets information on follow relationships between two Twitch users.  Eg "Who is Lirik following", "Who is following Lirik", "is user X following user Y"
#Required Scope : None
###specific params
## required
# None
## optional
# after(str) : forward cursor
# first(int) : maximum number of objects to return.  Max 100, default 20
#
# from_id(str) : User ID.  aka, who is this user following?
#   OR
# to_id(str) : User ID.  aka, who is following this user? 
###
###response fields
# followed_at(str) : Date and time when from_id followed to_id
# from_id(str) : ID of the user following the to_id user
# pagination(string) : cursor, use for subsequent requests for next values
# to_id(object) : ID of the user being followed by from_id
# total(int) : total number of items returned
###
def get_users_follows(**kwargs):
    return twitchget(COMMON_BASE_URL+'users/follows', (['from_id', 'to_id'],), ('after', 'first'), listify_keywords(**kwargs))

#Updates the description of a user specified by a Bearer token
#Required Scope : user:edit
###specific params
## required
# description(str) : new description for the user
## optional
# None
###
###response fields
# same as for Get Users
###
def update_user(**kwargs):    
    return twitchput(COMMON_BASE_URL+'users', ('description',), (), listify_keywords(**kwargs))

#Gets video information by video ID (one or more), user ID (one only), or game ID (one only)
#Required Scope : None
###specific params
## required
# id(str) : ID of the video being queried, limit 100, no optional parameters can be used if you use this
#   OR
# user_id(str) : ID of the user who owns the video, limit 1
#   OR
# game_id(str) : ID of the game the video is of, limit 1
##optional
# after(str) : forward cursor
# before(str) : backward cursor
# first(str) : Number of values to be returned when getting videos by user or game ID.  limit 100, default 20
# language(str) : Language of the video being queried, limit 1
# period(str) : Period during which the video was created.  Options "all", "day", "week", "month".  Default "all"
# sort(str) : Sort order of the videos.  Options "time", "trending", "views".  Default "time"
# type(str) : Type of video.  Options "all", "upload", "archive", "highlight".  Default "all"
###
###response fields
# created_at(str) : Date when the video was created
# description(str) : Description of the video
# duration(str) : Length of the video
# id(str) : ID of the video
# language(str) : Language of the video
# pagination(str) : cursor, use for subsequent next data
# published_at(str) : Date when the video was published
# thumbnail_url(object) : Template URL for the thumbnail of the video
# title(str) : Title of the video
# type(str) : Type of video.  options "upload", "archive", "highlight"
# url(str) : URL of the video
# user_id(str) : ID of the user who owns the video
# view_count(int) : Number of times the video had been viewed
# viewable(str) : Indicates whether the video is publicly viewable.  Options "public", "private"
###
def get_videos(**kwargs):
    return twitchget(COMMON_BASE_URL+'videos', (['id', 'user_id', 'game_id'],), ('after', 'before', 'first', 'language', 'period', 'sort', 'type'), listify_keywords(**kwargs))

