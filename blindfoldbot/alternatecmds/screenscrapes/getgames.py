import sys 

import alternatecmds.screenscrapes.soup_getgames
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_games_info_from_twitch_page(gamename):
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/directory/game/'+gamename, alternatecmds.screenscrapes.soup_getgames)

if __name__ == "__main__":
    print(get_games_info_from_twitch_page(sys.argv[1]))

