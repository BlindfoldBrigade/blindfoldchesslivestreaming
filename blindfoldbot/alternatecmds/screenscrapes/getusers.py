import sys 

import alternatecmds.screenscrapes.soup_getusers
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_users_info_from_twitch_page(loginname):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/'+loginname, alternatecmds.screenscrapes.soup_getusers)

if __name__ == "__main__":
    print(get_users_info_from_twitch_page(sys.argv[1]))

