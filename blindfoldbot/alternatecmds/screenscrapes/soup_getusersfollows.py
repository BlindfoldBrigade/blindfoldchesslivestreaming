from bs4 import BeautifulSoup, Tag, NavigableString

def is_follower_element(tag):
    return tag.has_attr('class') and 'user-card' in tag['class'] and not 'user-card_' in tag['class']

def follower_from_element(el):
    desc = list(el.descendants)
    return desc[0]['href'][1:]

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')

    follow_elements = soup.find_all(is_follower_element)
    followers = [follower_from_element(el) for el in follow_elements]
    return followers


