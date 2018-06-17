import asyncio
import pyppeteer

import sys 

import alternatecmds.screenscrapes.soup_getgames

async def get_games_info_from_twitch_page_async(gamename):
    twbrowser = await pyppeteer.launcher.launch()
    twpages = await twbrowser.pages()
    twpage = twpages[0]
    await twpage.goto('https://www.twitch.tv/directory/game/'+ gamename)

    #The await for the content() call doesn't seem to really
    #wait for everything to be available so 
    await asyncio.sleep(3)
    channel_content = await twpages[0].content()
    await twbrowser.close()
    return alternatecmds.screenscrapes.soup_getgames.perform_parse(channel_content)


def get_games_info_from_twitch_page(gamename):
    return asyncio.get_event_loop().run_until_complete(get_games_info_from_twitch_page_async(gamename))

if __name__ == "__main__":
    print(get_games_info_from_twitch_page(sys.argv[1]))

