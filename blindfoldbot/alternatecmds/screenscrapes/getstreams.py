import asyncio
import pyppeteer

import sys 

import alternatecmds.screenscrapes.soup_getstreams

async def get_streams_info_from_twitch_page_async(community):
    twbrowser = await pyppeteer.launcher.launch()
    twpages = await twbrowser.pages()
    twpage = twpages[0]
    await twpage.goto('https://www.twitch.tv/communities/'+ community)

    #The await for the content() call doesn't seem to really
    #wait for everything to be available so 
    await asyncio.sleep(3)
    channel_content = await twpages[0].content()
    await twbrowser.close()
    return alternatecmds.screenscrapes.soup_getstreams.perform_parse(channel_content)


def get_streams_info_from_twitch_page(community):
    return asyncio.get_event_loop().run_until_complete(get_streams_info_from_twitch_page_async(community))

if __name__ == "__main__":
    print(get_streams_info_from_twitch_page(sys.argv[1]))

