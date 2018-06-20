import sys 

import alternatecmds.screenscrapes.soup_getusersfollows
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_users_follows_info_from_twitch_page(loginname):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/'+loginname+'/followers', alternatecmds.screenscrapes.soup_getusersfollows)

if __name__ == "__main__":
    print(get_users_follows_info_from_twitch_page(sys.argv[1]))

