from TwitchPollCommands import get_users

def user_id_from_name(clientid, oauth, username):
    args = {'clientid': clientid, 'oauth': oauth, 'login': username}
    user_info = get_users(**args)['data']
    return user_info[0]['id']

