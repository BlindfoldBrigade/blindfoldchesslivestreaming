from bs4 import BeautifulSoup

def is_profile_image_element(tag):
    return tag.has_attr('class') and 'qa-broadcaster-logo' in tag['class'] and tag.has_attr('src')

def perform_parse(html_text_to_parse):
    soup = BeautifulSoup(html_text_to_parse, 'lxml-xml')

    profile_image_elements = soup.find_all(is_profile_image_element)
    profile_images = [item['src'] for item in profile_image_elements]

    return profile_images    
