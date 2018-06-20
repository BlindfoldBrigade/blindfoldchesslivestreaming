import sys 

import alternatecmds.screenscrapes.soup_getclips
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_clips_info_from_twitch_page(channel_to_check):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/'+channel_to_check+'/clips', alternatecmds.screenscrapes.soup_getclips)

if __name__ == "__main__":
    print(get_clips_info_from_twitch_page(sys.argv[1]))

