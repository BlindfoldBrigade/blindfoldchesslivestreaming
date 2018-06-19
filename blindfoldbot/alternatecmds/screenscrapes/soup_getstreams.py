from bs4 import BeautifulSoup

def is_username_element(tag):
    return tag.has_attr('data-test-selector') and tag['data-test-selector'] == 'preview-card-titles__subtitle'

def is_title_element(tag):
    return tag.has_attr('data-test-selector') and tag['data-test-selector'] == 'preview-card-titles__primary-link'

def findhrefmatch(el, matchme):
    descend = list(el.descendants)
    if not descend[-2]['href'].find(matchme) == -1:
        return descend[-1]
    else:
        return None

def findgame(el):
    descend = list(el.descendants)
    if not descend[-2]['href'].find('game') == -1:
        return descend[-1]
    else:
        return 

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')

    title_elements = soup.find_all(is_title_element)
    titles = [item.contents[0]['title'] for item in title_elements]

    username_elements = soup.find_all(is_username_element)
    usernames = [findhrefmatch(el, 'videos') for el in username_elements if not findhrefmatch(el, 'videos') == None]

    game_elements = soup.find_all(is_username_element)
    games = [findhrefmatch(el, '/directory/game') for el in username_elements if not findhrefmatch(el, '/directory/game') == None]

    return list(zip(titles, usernames, games))
    

