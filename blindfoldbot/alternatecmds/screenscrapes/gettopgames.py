import asyncio
import pyppeteer

import sys 

import alternatecmds.screenscrapes.soup_gettopgames

async def get_top_games_info_from_twitch_page_async():
    twbrowser = await pyppeteer.launcher.launch()
    twpages = await twbrowser.pages()
    twpage = twpages[0]
    await twpage.goto('https://www.twitch.tv/directory/game')

    #The await for the content() call doesn't seem to really
    #wait for everything to be available so 
    await asyncio.sleep(3)
    channel_content = await twpages[0].content()
    await twbrowser.close()
    return alternatecmds.screenscrapes.soup_gettopgames.perform_parse(channel_content)


def get_top_games_info_from_twitch_page():
    return asyncio.get_event_loop().run_until_complete(get_top_games_info_from_twitch_page_async())

if __name__ == "__main__":
    print(get_top_games_info_from_twitch_page())

