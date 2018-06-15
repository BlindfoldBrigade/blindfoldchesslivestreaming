import asyncio
import pyppeteer

import sys 

#import alternatecmds.screenscrapes.html_getclips
import alternatecmds.screenscrapes.soup_getclips


async def get_clips_info_from_twitch_page_async(channel_to_check):
    twbrowser = await pyppeteer.launcher.launch()
    twpages = await twbrowser.pages()
    twpage = twpages[0]
    await twpage.goto('https://www.twitch.tv/'+ channel_to_check + '/clips')

    #The await for the content() call doesn't seem to really
    #wait for everything to be available so 
    await asyncio.sleep(3)
    channel_content = await twpages[0].content()
    await twbrowser.close()
#    return alternatecmds.screenscrapes.html_getclips.perform_parse(channel_content)
    return alternatecmds.screenscrapes.soup_getclips.perform_parse(channel_content)


def get_clips_info_from_twitch_page(channel_to_check):
    return asyncio.get_event_loop().run_until_complete(get_clips_info_from_twitch_page_async(channel_to_check))

if __name__ == "__main__":
    print(get_clips_info_from_twitch_page(sys.argv[1]))

