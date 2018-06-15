from bs4 import BeautifulSoup

#def has_preview_card_class(tag):
#    return tag.has_attr('class') and 'preview-card' in tag.get_attribute_list('class')

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')
    xmlout = open('xmlout.xml', 'w')
    xmlout.write(soup.prettify())
    xmlout.close()
    allanchors = soup.find_all("a")
    return [link.attrs['href'] for link in allanchors if link.attrs['href'].find('https://clips.twitch.tv/') != -1]

