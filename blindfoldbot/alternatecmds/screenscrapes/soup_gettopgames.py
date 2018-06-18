from bs4 import BeautifulSoup
from blindfoldutilities import twitchstrings

def is_gametitle_element(tag):
    return tag.has_attr('class') and 'tw-box-art-card__title' in tag['class']

def is_boxart_element(tag):
    return tag.has_attr('class') and 'tw-card-img' in tag['class']

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')
 
    games_name_and_boxart = []

    title_elements = soup.find_all(is_gametitle_element)
    boxart_elements = soup.find_all(is_boxart_element)
    title_and_boxart_elements = list(zip(title_elements, boxart_elements))    
    for item in title_and_boxart_elements:
        games_name_and_boxart.append([item[0]['title'], twitchstrings.remove_img_dimensions(item[1].contents[0].contents[0]['src'])])
                   
    return games_name_and_boxart

