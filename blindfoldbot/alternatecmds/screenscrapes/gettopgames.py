import sys 

import alternatecmds.screenscrapes.soup_gettopgames
import alternatecmds.screenscrapes.screenscraper as screenscraper

def get_top_games_info_from_twitch_page():
    return screenscraper.get_info_from_twitch_page('https://www.twitch.tv/directory/game', alternatecmds.screenscrapes.soup_gettopgames)

if __name__ == "__main__":
    print(get_top_games_info_from_twitch_page())

