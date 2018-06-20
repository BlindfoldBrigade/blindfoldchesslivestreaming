import asyncio
import pyppeteer

from requests_html import HTMLSession

async def get_info_from_twitch_page_async(urlarg, parser):
    twbrowser = await pyppeteer.launcher.launch()
    twpages = await twbrowser.pages()
    twpage = twpages[0]
    await twpage.goto(urlarg)

    #The await for the content() call doesn't seem to really
    #wait for everything to be available so 
    await asyncio.sleep(3)
    channel_content = await twpages[0].content()
    await twbrowser.close()
    return parser.perform_parse(channel_content)

def get_info_from_twitch_page(urlarg, parser):
    return asyncio.get_event_loop().run_until_complete(get_info_from_twitch_page_async(urlarg, parser))

