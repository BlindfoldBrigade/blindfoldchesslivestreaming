import sys 

import alternatecmds.screenscrapes.soup_getstreams
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_streams_info_from_twitch_page(community):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/communities/'+community, alternatecmds.screenscrapes.soup_getstreams)

if __name__ == "__main__":
    print(get_streams_info_from_twitch_page(sys.argv[1]))

