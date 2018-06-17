from bs4 import BeautifulSoup

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')
    allanchors = soup.find_all("a")
    return [link.attrs['href'] for link in allanchors if link.attrs['href'].find('https://clips.twitch.tv/') != -1]

