import sys 

import alternatecmds.screenscrapes.html_bitleader
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_bitleader_info_from_twitch_page(channel_to_check):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/'+channel_to_check, alternatecmds.screenscrapes.html_bitleader)

if __name__ == "__main__":
    print(get_bitleader_info_from_twitch_page(sys.argv[1]))
