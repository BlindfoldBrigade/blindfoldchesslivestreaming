from bs4 import BeautifulSoup

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')
    allmeta = soup.find_all("meta")
    for meta in allmeta:
        if 'name' in meta.attrs and meta.attrs['name'] == 'title':
            name = meta.attrs['content']
            name = name[:name.find(' - Live Streams - Twitch')]
        elif 'name' in meta.attrs and meta.attrs['name'] == 'twitter:image':
            image = meta.attrs['content']
            image = image[:image.find('.jpg')] + '-{width}x{height}.jpg'
    return name, image

