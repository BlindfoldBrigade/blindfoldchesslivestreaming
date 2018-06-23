import sys 

import alternatecmds.screenscrapes.soup_getvideos
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_videos_info_from_twitch_page(broadcaster_name):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/'+broadcaster_name+'/videos/all/', alternatecmds.screenscrapes.soup_getvideos)

if __name__ == "__main__":
    print(get_videos_info_from_twitch_page(sys.argv[1]))

