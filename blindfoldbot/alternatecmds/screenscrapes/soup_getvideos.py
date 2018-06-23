from bs4 import BeautifulSoup

def is_title_element(tag):
    return tag.has_attr('class') and 'preview-card-thumbnail__image' in tag['class']

def is_link_element(tag):
    return tag.has_attr('data-a-target') and 'preview-card-image-link' in tag['data-a-target']

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')

    title_elements = soup.find_all(is_title_element)
    titles = [el.contents[0]['alt'] for el in title_elements]

    link_elements = soup.find_all(is_link_element)
    links = ['https://www.twitch.tv'+el['href'] for el in link_elements]

    return list(zip(titles,links))    

